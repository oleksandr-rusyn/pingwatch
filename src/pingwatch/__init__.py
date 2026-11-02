import time

import httpx


def check_url(url: str) -> dict:
    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=5, follow_redirects=True)
    except httpx.RequestError:
        return {
            "url": url,
            "status_code": None,
            "response_time_ms": None,
            "is-up": False,
        }

    end = time.perf_counter()

    return {
        "url":url,
        "status_code":response.status_code,
        "response_time_ms":(end-start) * 1000,
        "is-up":response.status_code < 400,
    }


def main() -> None:
    urls = [
        "https://google.com",
        "https://httpbin.org/status/500",
        "https://no-such-site.invalid",
    ]
    for url in urls:
        print(check_url(url))