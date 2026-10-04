import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Resolve and load root .env
ROOT_DIR = Path(__file__).resolve().parent.parent
root_env = ROOT_DIR / ".env"
backend_env = Path(__file__).resolve().parent / ".env"

if root_env.exists():
    load_dotenv(dotenv_path=root_env)
elif backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
else:
    load_dotenv()

def normalize_supabase_url(url: str | None) -> str | None:
    """Ensures Supabase URL is a valid full https URL."""
    if not url:
        return url
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        if "." in url:
            return f"https://{url}"
        return f"https://{url}.supabase.co"
    return url

SUPABASE_URL = normalize_supabase_url(os.environ.get("SUPABASE_URL"))
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

_supabase_client: Client | None = None

def get_supabase_client() -> Client:
    """
    Returns a reusable Supabase client instance initialized with
    SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from root .env.
    """
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            raise ValueError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing from environment.")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _supabase_client

# Export reusable client instance
supabase: Client | None = None
try:
    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
        supabase = get_supabase_client()
except Exception:
    supabase = None
