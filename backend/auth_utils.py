import os
import re
from datetime import datetime, timezone
from supabase_client import get_supabase_client

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEFAULT_STARTING_CREDITS = 500

def extract_bearer_token(auth_header: str | None) -> str | None:
    """Extracts raw JWT token from Authorization header."""
    if not auth_header:
        return None
    auth_header = auth_header.strip()
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return auth_header

def verify_token(token: str | None) -> dict | None:
    """
    Verifies a Supabase JWT access token on the server using Supabase Auth.
    Returns user dict on success, None if invalid or expired.
    """
    if not token:
        return None
    raw_token = extract_bearer_token(token)
    if not raw_token:
        return None

    try:
        client = get_supabase_client()
        user_response = client.auth.get_user(raw_token)
        if user_response and user_response.user:
            user = user_response.user
            return {
                "id": str(user.id),
                "email": user.email or "",
                "user_metadata": user.user_metadata or {},
                "created_at": getattr(user, "created_at", None),
            }
    except Exception as e:
        print(f"[AUTH] Token verification failed: {e}", flush=True)
        return None
    return None

def get_user_profile(user_id: str, email: str = "", default_meta: dict | None = None) -> dict:
    """
    Retrieves user profile and credit balance.
    Checks public.profiles table first; falls back gracefully to auth.users metadata.
    """
    client = get_supabase_client()
    meta = default_meta or {}
    credits_val = int(meta.get("credits", DEFAULT_STARTING_CREDITS))
    full_name = meta.get("full_name", "")

    # 1. Try public.profiles database table
    try:
        res = client.table("profiles").select("*").eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            row = res.data[0]
            return {
                "id": str(row.get("id", user_id)),
                "email": row.get("email", email),
                "full_name": row.get("full_name", full_name),
                "credits": int(row.get("credits", DEFAULT_STARTING_CREDITS)),
                "created_at": row.get("created_at"),
            }
        else:
            # Table exists but row not created yet -> insert it
            try:
                new_row = {
                    "id": user_id,
                    "email": email,
                    "full_name": full_name,
                    "credits": credits_val,
                }
                insert_res = client.table("profiles").insert(new_row).execute()
                if insert_res.data:
                    return {
                        "id": str(insert_res.data[0].get("id", user_id)),
                        "email": insert_res.data[0].get("email", email),
                        "full_name": insert_res.data[0].get("full_name", full_name),
                        "credits": int(insert_res.data[0].get("credits", credits_val)),
                    }
            except Exception as ins_err:
                print(f"[AUTH] Profile insert note: {ins_err}", flush=True)
    except Exception as table_err:
        # Table might not exist yet (PGRST205)
        # Fetch from Supabase auth admin metadata as reliable fallback
        pass

    # 2. Fallback to Supabase Auth user metadata
    if "credits" not in meta:
        try:
            user_record = client.auth.admin.get_user_by_id(user_id)
            if user_record and user_record.user:
                u_meta = user_record.user.user_metadata or {}
                credits_val = int(u_meta.get("credits", DEFAULT_STARTING_CREDITS))
                full_name = u_meta.get("full_name", full_name)
                email = user_record.user.email or email
        except Exception:
            pass

    return {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "credits": credits_val,
    }

def deduct_user_credits(user_id: str, amount: int) -> tuple[bool, int, str]:
    """
    Securely deducts credits for an authenticated user on the server.
    Returns (success, remaining_credits, message).
    """
    if amount <= 0:
        profile = get_user_profile(user_id)
        return True, profile["credits"], ""

    profile = get_user_profile(user_id)
    current_credits = profile["credits"]

    if current_credits < amount:
        return False, current_credits, f"Insufficient AI credits. (Required: {amount}, Available: {current_credits})"

    new_credits = max(0, current_credits - amount)
    client = get_supabase_client()

    # 1. Update public.profiles if table exists
    try:
        client.table("profiles").update({
            "credits": new_credits,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", user_id).execute()
    except Exception as table_err:
        pass

    # 2. Always sync user_metadata in Supabase Auth
    try:
        existing_meta = {}
        try:
            curr_u = client.auth.admin.get_user_by_id(user_id)
            if curr_u and curr_u.user:
                existing_meta = curr_u.user.user_metadata or {}
        except Exception:
            pass
        existing_meta["credits"] = new_credits
        client.auth.admin.update_user_by_id(user_id, {"user_metadata": existing_meta})
    except Exception as admin_err:
        print(f"[AUTH] Failed to update user metadata credits: {admin_err}", flush=True)

    return True, new_credits, ""

def reset_user_credits(user_id: str, amount: int = DEFAULT_STARTING_CREDITS) -> tuple[bool, int]:
    """Resets user credit balance back to starting allocation."""
    client = get_supabase_client()
    try:
        client.table("profiles").update({
            "credits": amount,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", user_id).execute()
    except Exception:
        pass

    try:
        existing_meta = {}
        try:
            curr_u = client.auth.admin.get_user_by_id(user_id)
            if curr_u and curr_u.user:
                existing_meta = curr_u.user.user_metadata or {}
        except Exception:
            pass
        existing_meta["credits"] = amount
        client.auth.admin.update_user_by_id(user_id, {"user_metadata": existing_meta})
    except Exception as admin_err:
        print(f"[AUTH] Failed to reset user metadata credits: {admin_err}", flush=True)

    return True, amount

def signup_user(email: str, password: str, full_name: str) -> tuple[bool, dict, str]:
    """
    Registers a new user in Supabase Auth with server-side validation.
    Auto-confirms user to avoid Supabase mailer rate limit pitfalls.
    Returns (success, response_dict, error_message).
    """
    email = (email or "").strip().lower()
    full_name = (full_name or "").strip()
    password = password or ""

    if not email or not EMAIL_REGEX.match(email):
        return False, {}, "Please provide a valid email address."
    if not password or len(password) < 6:
        return False, {}, "Password must be at least 6 characters long."
    if not full_name:
        return False, {}, "Please provide your full name."

    client = get_supabase_client()

    try:
        # Create user via admin API with email_confirm: True to prevent SMTP rate-limiting
        created_resp = client.auth.admin.create_user({
            "email": email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {
                "full_name": full_name,
                "credits": DEFAULT_STARTING_CREDITS,
            }
        })
        user = created_resp.user
        if not user:
            return False, {}, "Failed to create user account."

        # Immediately sign the user in to issue JWT access and refresh tokens
        login_resp = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        session = login_resp.session
        access_token = session.access_token if session else ""
        refresh_token = session.refresh_token if session else ""

        # Ensure profiles table record
        profile = get_user_profile(str(user.id), email=email, default_meta={"full_name": full_name, "credits": DEFAULT_STARTING_CREDITS})

        return True, {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": full_name,
            },
            "profile": profile,
        }, ""

    except Exception as e:
        err_str = str(e)
        if "already registered" in err_str.lower() or "unique" in err_str.lower() or "already exists" in err_str.lower():
            return False, {}, "An account with this email already exists. Please log in."
        return False, {}, f"Sign up failed: {err_str}"

def login_user(email: str, password: str) -> tuple[bool, dict, str]:
    """
    Logs in user with email and password via Supabase Auth.
    Returns (success, session_dict, error_message).
    """
    email = (email or "").strip().lower()
    password = password or ""

    if not email or not EMAIL_REGEX.match(email):
        return False, {}, "Please enter a valid email address."
    if not password:
        return False, {}, "Password is required."

    client = get_supabase_client()

    try:
        login_resp = client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        session = login_resp.session
        user = login_resp.user

        if not session or not session.access_token or not user:
            return False, {}, "Authentication failed. Please verify your credentials."

        profile = get_user_profile(str(user.id), email=user.email, default_meta=user.user_metadata)

        return True, {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": profile.get("full_name", user.user_metadata.get("full_name", "")),
            },
            "profile": profile,
        }, ""

    except Exception as e:
        err_str = str(e)
        if "invalid login credentials" in err_str.lower() or "invalid_credentials" in err_str.lower():
            return False, {}, "Invalid email or password. Please try again."
        if "email not confirmed" in err_str.lower():
            return False, {}, "Please confirm your email address before logging in."
        return False, {}, f"Login failed: {err_str}"

def request_password_reset(email: str) -> tuple[bool, str]:
    """Requests a password recovery email via Supabase Auth."""
    email = (email or "").strip().lower()
    if not email or not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address."

    client = get_supabase_client()
    try:
        client.auth.reset_password_for_email(email)
        return True, "If an account exists for this email, password reset instructions have been dispatched."
    except Exception as e:
        # Avoid user enumeration while giving friendly message
        print(f"[AUTH] Password reset note: {e}", flush=True)
        return True, "If an account exists for this email, password reset instructions have been dispatched."
