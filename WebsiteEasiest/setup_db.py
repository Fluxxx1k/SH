#!/usr/bin/env python3
"""
Setup script for Secret Hitler Web Game Database.
Initializes database and performs basic checks.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def main():
    print("=" * 60)
    print("Secret Hitler Web Game - Database Setup")
    print("=" * 60)

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    print("✅ Python version OK")

    # Check if .env exists
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print(f"\n⚠️  .env file not found at {env_file}")
        print("   Using default SQLite database")
        print("   To use PostgreSQL, create .env with DATABASE_URL")
    else:
        print(f"✅ .env file found")

    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, continuing anyway")

    # Initialize database
    print("\n📦 Initializing database...")
    try:
        from WebsiteEasiest.data.database.migrations import migrate_init_db
        if migrate_init_db():
            print("✅ Database initialized successfully")
        else:
            print("❌ Database initialization failed")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

    # Verify database
    print("\n🔍 Verifying database...")
    try:
        from WebsiteEasiest.data.database import get_session
        from WebsiteEasiest.data.database.models import Player, Game

        session = get_session()
        player_count = session.query(Player).count()
        game_count = session.query(Game).count()
        session.close()

        print(f"✅ Players in database: {player_count}")
        print(f"✅ Games in database: {game_count}")
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        sys.exit(1)

    # Test player creation
    print("\n🧪 Testing player creation...")
    try:
        from WebsiteEasiest.data.database.player_operations import (
            create_player_db, exists_player_db
        )

        test_username = "test_user_setup"
        test_password = "test_password_123"

        # Clean up if exists
        if exists_player_db(test_username):
            print(f"   Found existing test user, skipping creation")
        else:
            success, error = create_player_db(test_username, test_password)
            if success:
                print(f"✅ Test player created: {test_username}")
            else:
                print(f"❌ Failed to create test player: {error}")
    except Exception as e:
        print(f"⚠️  Could not test player creation: {e}")

    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nYou can now run:")
    print("  python WebsiteEasiest/app2.py")
    print("\nOr for development:")
    print("  flask --app WebsiteEasiest.app_globs run")
    print("\nSee DATABASE_GUIDE.md for more information")

if __name__ == '__main__':
    main()

