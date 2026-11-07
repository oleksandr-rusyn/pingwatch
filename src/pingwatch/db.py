import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://pingwatch:pingwatch@localhost:5432/pingwatch",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
