"""HTTP boundary: the website talks to the API, never directly to SQLite."""
import os
import httpx

API_URL = os.environ.get("TAKEAWAY_API_URL", "http://127.0.0.1:8000").rstrip("/")


class APIError(Exception):
    """A message suitable for displaying beside the form."""


def request_api(method, path, **kwargs):
    try:
        response = httpx.request(method, API_URL + path, timeout=10, **kwargs)
    except httpx.RequestError as error:
        # Never retry POST automatically: the server may have saved the order.
        raise APIError("Could not reach the ordering service. If you submitted an order, check saved orders before trying again.") from error
    if response.is_error:
        try:
            detail = response.json().get("detail")
        except ValueError:
            detail = None
        message = detail if isinstance(detail, str) else "The service could not accept this request."
        raise APIError(message)
    return response.json()
