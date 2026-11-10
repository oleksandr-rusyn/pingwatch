import sys

from sqlalchemy.exc import SQLAlchemyError

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
            try:
                session.commit()
            except SQLAlchemyError as exc:
                session.rollback()
                print(f"Failed to save check for {url}: {exc}", file=sys.stderr)
