"""
Database migration script for initial schema creation.
This script initializes the database with all tables.
"""

import os
from WebsiteEasiest.data.database import Base, init_db
from WebsiteEasiest.data.database.models import (
    Player, Game, GamePlayer, GameLog, GameResult, IPLog
)
from WebsiteEasiest.logger import logger

def migrate_init_db(database_url: str = None, echo: bool = False):
    """
    Initialize database with all tables.

    Args:
        database_url: Database URL. If None, uses SQLite
        echo: If True, logs all SQL statements
    """
    try:
        logger.info("Starting database migration...")
        init_db(database_url, echo=echo)
        logger.info("Database migration completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Database migration failed: {repr(e)}")
        return False

if __name__ == '__main__':
    # For local development, use SQLite
    migrate_init_db(echo=True)

