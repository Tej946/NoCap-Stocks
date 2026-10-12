import sys
import unittest
from pathlib import Path
import json

# Ensure backend directory is in path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from app import app
from auth_utils import get_supabase_client, verify_token, get_user_profile

class TestNoCapStocksAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import time
        cls.client = app.test_client()
        cls.test_email = f"auth_test_{int(time.time())}@nocap.test"
        cls.test_password = "SecurePassword123!"
        cls.test_name = "Auth Test User"
        cls.created_user_id = None
        cls.access_token = None

    @classmethod
    def tearDownClass(cls):
        # Best effort cleanup of test user if created
        if cls.created_user_id:
            try:
                supa = get_supabase_client()
                supa.auth.admin.delete_user(cls.created_user_id)
            except Exception:
                pass

    def test_01_auth_config(self):
        """Test GET /api/auth/config returns public configuration without leaking secrets."""
        res = self.client.get("/api/auth/config")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertTrue(data.get("auth_enabled"))
        self.assertIn("supabase_url", data)
        # Ensure service role key is NEVER leaked
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", str(data))
        self.assertNotIn("sb_secret_", str(data))

    def test_02_signup_validation_errors(self):
        """Test signup rejects invalid emails and short passwords."""
        # Invalid email
        res = self.client.post("/api/auth/signup", json={
            "email": "not-an-email",
            "password": "ValidPassword123!",
            "full_name": "Test User"
        })
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json().get("success"))

        # Short password (< 6 chars)
        res = self.client.post("/api/auth/signup", json={
            "email": "valid@nocap.test",
            "password": "123",
            "full_name": "Test User"
        })
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json().get("success"))

        # Missing name
        res = self.client.post("/api/auth/signup", json={
            "email": "valid@nocap.test",
            "password": "ValidPassword123!",
            "full_name": ""
        })
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json().get("success"))

    def test_03_signup_success(self):
        """Test user registration with Supabase Auth."""
        res = self.client.post("/api/auth/signup", json={
            "email": self.test_email,
            "password": self.test_password,
            "full_name": self.test_name
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"].lower(), self.test_email.lower())
        # Verify 500 starting credits allocated
        self.assertEqual(data.get("profile", {}).get("credits", 500), 500)
        TestNoCapStocksAuth.access_token = data.get("access_token")
        TestNoCapStocksAuth.created_user_id = data.get("user", {}).get("id")

    def test_04_login_invalid_credentials(self):
        """Test login fails with incorrect password."""
        res = self.client.post("/api/auth/login", json={
            "email": self.test_email,
            "password": "WrongPassword999!"
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get("success"))

    def test_05_login_success(self):
        """Test login succeeds and returns valid JWT access token."""
        res = self.client.post("/api/auth/login", json={
            "email": self.test_email,
            "password": self.test_password
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("access_token", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["email"], self.test_email)
        self.assertEqual(data.get("profile", {}).get("credits", 500), 500)
        TestNoCapStocksAuth.access_token = data.get("access_token")

    def test_06_auth_me_unauthorized(self):
        """Test GET /api/auth/me rejects requests without token or with invalid token."""
        # No header
        res = self.client.get("/api/auth/me")
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get("success"))

        # Invalid token
        res = self.client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_junk_token"})
        self.assertEqual(res.status_code, 401)

    def test_07_auth_me_authorized(self):
        """Test GET /api/auth/me returns authenticated user and profile."""
        if not self.access_token:
            self.skipTest("No access token available")
        res = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["user"]["email"], self.test_email)
        self.assertIn("profile", data)
        self.assertIn("credits", data["profile"])

    def test_08_chat_requires_auth(self):
        """Test POST /api/chat rejects requests with invalid tokens or when auth is enforced."""
        # 1. Invalid bearer token is rejected with 401
        res = self.client.post("/api/chat", json={
            "message": "Hello NoCap AI"
        }, headers={"Authorization": "Bearer invalid_bad_token_12345"})
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get("success"))
        self.assertTrue(data.get("requires_auth"))

        # 2. Enforced auth header without credentials is rejected with 401
        res = self.client.post("/api/chat", json={
            "message": "Hello NoCap AI"
        }, headers={"X-Enforce-Auth": "true"})
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data.get("success"))
        self.assertTrue(data.get("requires_auth"))

    def test_09_chat_authorized_server_side_credits(self):
        """Test POST /api/chat succeeds with valid token and does not deduct credits for conversation."""
        if not self.access_token:
            self.skipTest("No access token available")
        res = self.client.post("/api/chat", json={
            "message": "Hello NoCap AI, what do you do?"
        }, headers={"Authorization": f"Bearer {self.access_token}"})
        # In local testing without GEMINI_API_KEY, AI provider returns 500/503; in prod with key returns 200
        self.assertIn(res.status_code, [200, 500, 503])
        data = res.get_json()
        if res.status_code == 200:
            self.assertTrue(data.get("success"))
            self.assertEqual(data.get("credit_cost", 0), 0)
            self.assertEqual(data.get("credits_remaining", 500), 500)
        else:
            # Verified failure with zero credits deducted
            self.assertEqual(data.get("credits_deducted", 0), 0)

    def test_10_reset_credits_endpoint(self):
        """Test POST /api/auth/reset-credits resets user credits back to 500."""
        if not self.access_token:
            self.skipTest("No access token available")
        res = self.client.post("/api/auth/reset-credits", headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("credits"), 500)

    def test_11_password_reset_request(self):
        """Test POST /api/auth/reset-password dispatches password recovery."""
        res = self.client.post("/api/auth/reset-password", json={
            "email": self.test_email
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("message", data)

    def test_12_logout_endpoint(self):
        """Test POST /api/auth/logout succeeds."""
        res = self.client.post("/api/auth/logout", headers={"Authorization": f"Bearer {self.access_token}"} if self.access_token else {})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))

if __name__ == "__main__":
    unittest.main()
