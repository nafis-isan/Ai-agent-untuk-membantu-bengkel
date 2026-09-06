"""Database Initialization Script"""

from .connection import Base, engine
from . import models


def init_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    init_database()
