import time
from datetime import UTC, datetime

import httpx

TIMEOUT_SECONDS = 5


def check_url(url: str) -> dict:
    """Check a URL and return its status, response time and availability."""
    checked_at = datetime.now(UTC)
    start = time.perf_counter()
    try:
        with httpx.stream(
            "GET", url, timeout=TIMEOUT_SECONDS, follow_redirects=True
        ) as response:
            elapsed = time.perf_counter() - start
            status_code = response.status_code
    except httpx.RequestError as exc:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
            "error": type(exc).__name__,
            "checked_at": checked_at,
        }

    return {
        "url": url,
        "status_code": status_code,
        "response_time_ms": round(elapsed * 1000, 1),
        "is_up": status_code < 400,
        "error": None,
        "checked_at": checked_at,
    }
