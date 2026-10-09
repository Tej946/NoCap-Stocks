import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
import time

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import (
    app,
    call_gemini,
    parse_retry_after,
    sanitize_secret_text,
    extract_gemini_error_details,
    TRANSIENT_STATUS_CODES,
    NON_RETRYABLE_STATUS_CODES
)

class TestGeminiRetryLogic(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()

    def test_parse_retry_after(self):
        # Numeric seconds
        self.assertEqual(parse_retry_after("5"), 5.0)
        self.assertEqual(parse_retry_after("2.5"), 2.5)
        # Cap at 30 seconds
        self.assertEqual(parse_retry_after("120"), 30.0)
        # None / empty / invalid
        self.assertIsNone(parse_retry_after(None))
        self.assertIsNone(parse_retry_after(""))
        self.assertIsNone(parse_retry_after("invalid_header"))

    def test_sanitize_secret_text(self):
        raw = "Error with API key AIzaSyABC12345678901234567890 and key=AIzaSyXYZ1234567890"
        sanitized = sanitize_secret_text(raw)
        self.assertNotIn("AIzaSyABC12345678901234567890", sanitized)
        self.assertNotIn("AIzaSyXYZ1234567890", sanitized)
        self.assertIn("[REDACTED]", sanitized)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_retry_503_eventual_success(self, mock_exec, mock_sleep, mock_key):
        """HTTP 503 fails twice, succeeds on 3rd attempt."""
        mock_exec.side_effect = [
            {"success": False, "status_code": 503, "error": "Gemini API HTTP 503: model experiencing high demand"},
            {"success": False, "status_code": 503, "error": "Gemini API HTTP 503: model experiencing high demand"},
            {"success": True, "reply": "Apple has demonstrated strong recovery historically.", "model": "gemini-2.5-flash"}
        ]

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertTrue(result["success"])
        self.assertEqual(result["reply"], "Apple has demonstrated strong recovery historically.")
        self.assertEqual(mock_exec.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_retry_503_exhausted_retries(self, mock_exec, mock_sleep, mock_key):
        """HTTP 503 fails continuously; retries up to 3 times (4 attempts total), then returns friendly error."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 503,
            "error": "Gemini API HTTP 503: model is currently experiencing high demand (UNAVAILABLE)"
        }

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 503)
        self.assertTrue(result["is_transient"])
        self.assertEqual(result["attempts"], 4)
        self.assertEqual(mock_exec.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)
        self.assertEqual(result["error"], "NoCap AI is temporarily busy. Please try again shortly.")

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_retry_429_respects_retry_after(self, mock_exec, mock_sleep, mock_key):
        """HTTP 429 rate limit with Retry-After header: respects header value."""
        mock_exec.side_effect = [
            {"success": False, "status_code": 429, "error": "Resource Exhausted", "retry_after": 2.0},
            {"success": True, "reply": "Analysis completed successfully after rate limit backoff.", "model": "gemini-2.5-flash"}
        ]

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertTrue(result["success"])
        self.assertEqual(mock_exec.call_count, 2)
        # Verify sleep was called with exactly 2.0 seconds from Retry-After
        mock_sleep.assert_called_once_with(2.0)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_non_retryable_401(self, mock_exec, mock_sleep, mock_key):
        """HTTP 401 Unauthorized: does not retry, aborts immediately."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 401,
            "error": "API key invalid"
        }

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 401)
        self.assertFalse(result["is_transient"])
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_exec.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_non_retryable_403(self, mock_exec, mock_sleep, mock_key):
        """HTTP 403 Forbidden: does not retry, aborts immediately."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 403,
            "error": "Permission denied"
        }

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 403)
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_exec.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_non_retryable_404(self, mock_exec, mock_sleep, mock_key):
        """HTTP 404 Model Not Found: does not retry, aborts immediately."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 404,
            "error": "Model not found"
        }

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 404)
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_exec.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_non_retryable_400(self, mock_exec, mock_sleep, mock_key):
        """HTTP 400 Bad Request: does not retry, aborts immediately."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 400,
            "error": "Invalid argument"
        }

        result = call_gemini("sys prompt", "user prompt", max_retries=3)

        self.assertFalse(result["success"])
        self.assertEqual(result["status_code"], 400)
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_exec.call_count, 1)
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("app.get_gemini_api_key", return_value="fake_api_key")
    @patch("app.time.sleep", return_value=None)
    @patch("app._execute_gemini_single_attempt")
    def test_overall_deadline_stops_retries(self, mock_exec, mock_sleep, mock_key):
        """Setting deadline_seconds enforces deadline cutoff so retries cannot exceed timeout."""
        mock_exec.return_value = {
            "success": False,
            "status_code": 503,
            "error": "Gemini API HTTP 503: high demand"
        }

        # deadline_seconds=0.0 forces immediate deadline exceeded after first attempt
        result = call_gemini("sys prompt", "user prompt", max_retries=3, deadline_seconds=0.0)

        self.assertFalse(result["success"])
        self.assertTrue(result.get("deadline_exceeded"))
        self.assertEqual(result["attempts"], 1)
        self.assertEqual(mock_sleep.call_count, 0)

    @patch("app.get_company_info")
    @patch("app.analyze_stock_drops")
    @patch("app.ask_ai")
    def test_api_chat_503_graceful_analysis_fallback(self, mock_ask, mock_analyze, mock_info):
        """
        When Gemini is 503 unavailable for an analysis query (e.g. 'Analyze AAPL'),
        the endpoint returns HTTP 200 with verified historical analysis, card_data,
        clearly labels AI explanation as temporarily unavailable, and deducts 0 credits.
        """
        mock_info.return_value = {
            "company_name": "Apple Inc.",
            "ticker": "AAPL",
            "exchange": "NASDAQ",
            "country": "United States"
        }
        mock_analyze.return_value = {
            "total_events_found": 12,
            "summary_statistics": {
                "30_days": {"count": 12, "average_return": 4.5, "win_rate": 85.0},
                "90_days": {"count": 12, "average_return": 8.2, "win_rate": 90.0},
                "180_days": {"count": 12, "average_return": 14.1, "win_rate": 91.7}
            },
            "historical_stakes": {"stakes": "HIGH", "reason": "High volatility post-drop recovery"}
        }
        mock_ask.return_value = {
            "success": False,
            "status_code": 503,
            "is_transient": True,
            "error": "NoCap AI is temporarily busy. Please try again shortly."
        }

        res = self.client.post("/api/chat", json={
            "message": "Analyze AAPL",
            "credits": 500
        })

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertTrue(data.get("ai_unavailable"))
        self.assertEqual(data["credits_deducted"], 0)
        self.assertEqual(data["credits_remaining"], 500)
        self.assertIsNotNone(data.get("card_data"))
        self.assertIsNotNone(data.get("analysis_data"))
        self.assertIn("temporarily unavailable", data["reply"])
        self.assertIn("NoCap AI is temporarily busy", data["reply"])

    @patch("app.ask_ai")
    def test_api_chat_503_conversational_structured_error(self, mock_ask):
        """
        When Gemini is 503 unavailable for a conversational query without historical data,
        returns HTTP 503 with structured JSON and friendly message, deducting 0 credits.
        """
        mock_ask.return_value = {
            "success": False,
            "status_code": 503,
            "is_transient": True,
            "error": "NoCap AI is temporarily busy. Please try again shortly."
        }

        res = self.client.post("/api/chat", json={
            "message": "Hello NoCap AI!",
            "credits": 500
        })

        self.assertEqual(res.status_code, 503)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "NoCap AI is temporarily busy. Please try again shortly.")
        self.assertEqual(data["credits_deducted"], 0)
        self.assertEqual(data["credits_remaining"], 500)

if __name__ == "__main__":
    unittest.main()
