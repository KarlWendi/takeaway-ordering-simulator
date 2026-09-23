import unittest
from unittest.mock import Mock, patch

import httpx

import web_client


class WebClientRetryTests(unittest.TestCase):
    @patch("web_client.time.sleep")
    @patch("web_client.httpx.request")
    def test_get_retries_while_service_wakes(self, request, sleep):
        waking = Mock(status_code=503, is_error=True)
        ready = Mock(status_code=200, is_error=False)
        ready.json.return_value = {"status": "ready"}
        request.side_effect = [waking, ready]

        result = web_client.request_api("GET", "/")

        self.assertEqual(result, {"status": "ready"})
        self.assertEqual(request.call_count, 2)
        sleep.assert_called_once_with(web_client.READ_RETRY_SECONDS)

    @patch("web_client.time.sleep")
    @patch("web_client.httpx.request")
    def test_post_is_never_retried(self, request, sleep):
        request.side_effect = httpx.ConnectError("connection lost")

        with self.assertRaises(web_client.APIError):
            web_client.request_api("POST", "/checkout", json={"items": []})

        request.assert_called_once()
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
