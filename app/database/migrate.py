"""Small, idempotent migration runner for deployments without Alembic installed."""

from sqlalchemy import text

from .connection import engine
from .init_db import init_database


def migrate() -> None:
    init_database()
    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations "
                "(version VARCHAR(50) PRIMARY KEY, applied_at TIMESTAMP NOT NULL)"
            )
        )
        connection.execute(
            text(
                "INSERT INTO schema_migrations(version, applied_at) "
                "SELECT '20260910_core', CURRENT_TIMESTAMP "
                "WHERE NOT EXISTS (SELECT 1 FROM schema_migrations WHERE version = '20260910_core')"
            )
        )


if __name__ == "__main__":
    migrate()