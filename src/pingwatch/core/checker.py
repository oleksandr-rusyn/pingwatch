import time

import httpx


def check_url(url: str) -> dict:
    """Check a URL and return its status, response time and availability."""
    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=5, follow_redirects=True)
    except httpx.RequestError:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "is_up": False,
        }

    end = time.perf_counter()

    return {
        "url": url,
        "status_code": response.status_code,
        "response_time_ms": round((end - start) * 1000, 1),
        "is_up": response.status_code < 400,
    }
