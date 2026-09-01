import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()


POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


def _create_engine(database_url: str):
    return create_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False} if database_url.startswith("sqlite") else {},
    )


postgres_url = (
    f"postgresql+psycopg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
) if POSTGRES_DB and POSTGRES_USER and POSTGRES_PASSWORD else None
DATABASE_URL = postgres_url or "sqlite:///./bengkel.db"


engine = _create_engine(DATABASE_URL)

try:
    if postgres_url:
        with engine.connect() as connection:
            connection.execute(__import__("sqlalchemy").text("SELECT 1"))
except Exception:
    DATABASE_URL = "sqlite:///./bengkel.db"
    engine = _create_engine(DATABASE_URL)
    print("PostgreSQL not available, falling back to SQLite for local development.")


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass