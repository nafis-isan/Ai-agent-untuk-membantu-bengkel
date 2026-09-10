"""Database Initialization Script"""

from sqlalchemy import inspect, text

from .connection import Base, engine
from . import models


def init_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    columns = {column["name"] for column in inspect(engine).get_columns("service_orders")}
    if "completed_at" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE service_orders ADD COLUMN completed_at TIMESTAMP NULL"))
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    init_database()
