"""HTTP boundary: the website talks to the API, never directly to SQLite."""
import os
import time
import httpx

API_URL = os.environ.get("TAKEAWAY_API_URL", "http://127.0.0.1:8000").rstrip("/")
READ_ATTEMPTS = 12
READ_RETRY_SECONDS = 5
TEMPORARY_STATUS_CODES = {502, 503, 504}


class APIError(Exception):
    """A message suitable for displaying beside the form."""


def request_api(method, path, **kwargs):
    method = method.upper()
    attempts = READ_ATTEMPTS if method == "GET" else 1

    for attempt in range(attempts):
        try:
            response = httpx.request(method, API_URL + path, timeout=10, **kwargs)
        except httpx.RequestError as error:
            if method == "GET" and attempt < attempts - 1:
                time.sleep(READ_RETRY_SECONDS)
                continue
            if method == "GET":
                raise APIError(
                    "The free ordering service is still waking up. Please try again shortly."
                ) from error
            # Never retry a write: the server may have completed it before the connection failed.
            raise APIError(
                "Could not reach the ordering service. If you submitted an order, "
                "check saved orders before trying again."
            ) from error

        if (
            method == "GET"
            and response.status_code in TEMPORARY_STATUS_CODES
            and attempt < attempts - 1
        ):
            time.sleep(READ_RETRY_SECONDS)
            continue
        break

    if response.is_error:
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = None
        message = detail if isinstance(detail, str) else "The service could not accept this request."
        raise APIError(message)
    return response.json()
