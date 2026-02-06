"""
Database module for Secret Hitler Web Game.
Provides SQLAlchemy models and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional
import os

Base = declarative_base()

# Database URL configuration
DATABASE_URL: Optional[str] = None
engine = None
SessionLocal = None

def init_db(database_url: str = None, echo: bool = False):
    """
    Initialize database connection.

    Args:
        database_url: Database URL (e.g., 'postgresql://user:password@localhost/dbname')
                     If None, uses SQLite by default
        echo: If True, log all SQL statements
    """
    global DATABASE_URL, engine, SessionLocal

    if database_url is None:
        # Use SQLite as default for development
        db_path = os.path.join(os.path.dirname(__file__), 'app.db')
        database_url = f'sqlite:///{db_path}'

    DATABASE_URL = database_url
    engine = create_engine(database_url, echo=echo, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    from WebsiteEasiest.logger import logger
    logger.info(f"Database initialized: {database_url}")

def get_session():
    """Get a new database session."""
    global SessionLocal
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return SessionLocal()


