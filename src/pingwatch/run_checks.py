from pingwatch.core.checker import check_url
from pingwatch.core.db import SessionLocal
from pingwatch.core.models import Check


def main() -> None:
    urls = [
        "https://google.com",
        "https://httpbin.org/status/500",
        "https://no-such-site.invalid",
    ]
    with SessionLocal() as session:
        for url in urls:
            result = check_url(url)
            print(result)
            session.add(Check(**result))
        session.commit()
