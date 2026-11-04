from pingwatch.checker import check_url


def main() -> None:
    urls = [
        "https://google.com",
        "https://httpbin.org/status/500",
        "https://no-such-site.invalid",
    ]
    for url in urls:
        print(check_url(url))
