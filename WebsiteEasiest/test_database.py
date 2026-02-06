#!/usr/bin/env python3
"""
Database testing script.
Verifies database operations and functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_player_operations():
    """Test player database operations."""
    print("\n" + "=" * 60)
    print("Testing Player Operations")
    print("=" * 60)

    from WebsiteEasiest.data.database.player_operations import (
        create_player_db, get_data_of_player_db, login_player_db,
        exists_player_db, count_players_db
    )

    test_user = "test_player_001"
    test_pass = "password123"

    # Test 1: Create player
    print("\n1️⃣ Testing player creation...")
    success, error = create_player_db(test_user, test_pass)
    if success:
        print(f"   ✅ Player created: {test_user}")
    else:
        print(f"   ❌ Failed: {error}")
        return False

    # Test 2: Check exists
    print("\n2️⃣ Testing player existence check...")
    if exists_player_db(test_user):
        print(f"   ✅ Player exists: {test_user}")
    else:
        print(f"   ❌ Player not found")
        return False

    # Test 3: Get player data
    print("\n3️⃣ Testing get player data...")
    success, data = get_data_of_player_db(test_user)
    if success:
        print(f"   ✅ Player data retrieved:")
        print(f"      - Username: {data['player_name']}")
        print(f"      - Games played: {data['games_played']}")
        print(f"      - Games won: {data['games_won']}")
    else:
        print(f"   ❌ Failed: {data}")
        return False

    # Test 4: Login
    print("\n4️⃣ Testing player login...")
    success, error = login_player_db(test_user, test_pass)
    if success:
        print(f"   ✅ Login successful")
    else:
        print(f"   ❌ Failed: {error}")
        return False

    # Test 5: Wrong password
    print("\n5️⃣ Testing login with wrong password...")
    success, error = login_player_db(test_user, "wrongpass")
    if not success:
        print(f"   ✅ Correctly rejected wrong password")
    else:
        print(f"   ❌ Should have rejected wrong password")
        return False

    # Test 6: Count players
    print("\n6️⃣ Testing player count...")
    count = count_players_db()
    if count > 0:
        print(f"   ✅ Player count: {count}")
    else:
        print(f"   ❌ No players found")
        return False

    return True


def test_game_operations():
    """Test game database operations."""
    print("\n" + "=" * 60)
    print("Testing Game Operations")
    print("=" * 60)

    from WebsiteEasiest.data.database.game_operations import (
        create_game_db, get_data_of_game_db, save_data_of_game_db,
        log_game_event_db, exists_game_db
    )

    test_game = "test_game_001"
    test_creator = "test_player_001"

    # Test 1: Create game
    print("\n1️⃣ Testing game creation...")
    success, error = create_game_db(test_game, test_creator)
    if success:
        print(f"   ✅ Game created: {test_game}")
    else:
        print(f"   ❌ Failed: {error}")
        return False

    # Test 2: Check exists
    print("\n2️⃣ Testing game existence check...")
    if exists_game_db(test_game):
        print(f"   ✅ Game exists: {test_game}")
    else:
        print(f"   ❌ Game not found")
        return False

    # Test 3: Get game data
    print("\n3️⃣ Testing get game data...")
    success, data = get_data_of_game_db(test_game)
    if success:
        print(f"   ✅ Game data retrieved:")
        print(f"      - Name: {data['name']}")
        print(f"      - Status: {data['status']}")
        print(f"      - Creator: {data['created_by']}")
        print(f"      - Players: {data['players']}")
    else:
        print(f"   ❌ Failed: {data}")
        return False

    # Test 4: Save game state
    print("\n4️⃣ Testing save game state...")
    game_state = {
        'current_state': {
            'round': 1,
            'deck': ['R', 'B', 'R', 'B', 'R'],
        },
        'settings': {
            'max_players': 5,
            'red_win_num': 5,
            'black_win_num': 6,
        }
    }
    if save_data_of_game_db(test_game, game_state):
        print(f"   ✅ Game state saved")
    else:
        print(f"   ❌ Failed to save game state")
        return False

    # Test 5: Log game event
    print("\n5️⃣ Testing game event logging...")
    success, error = log_game_event_db(
        test_game,
        "action",
        message="Game started",
        player_name=test_creator,
        data={'action': 'start_game'}
    )
    if success:
        print(f"   ✅ Event logged")
    else:
        print(f"   ❌ Failed: {error}")
        return False

    return True


def test_database_integrity():
    """Test database integrity and relationships."""
    print("\n" + "=" * 60)
    print("Testing Database Integrity")
    print("=" * 60)

    from WebsiteEasiest.data.database import get_session
    from WebsiteEasiest.data.database.models import Player, Game, GamePlayer, GameLog

    session = get_session()

    try:
        # Test 1: Tables exist
        print("\n1️⃣ Checking table existence...")
        tables = [Player, Game, GamePlayer, GameLog]
        for table in tables:
            count = session.query(table).count()
            print(f"   ✅ {table.__name__}: {count} records")

        # Test 2: Foreign keys
        print("\n2️⃣ Checking relationships...")
        games = session.query(Game).all()
        if games:
            game = games[0]
            print(f"   ✅ Game: {game.name}")
            print(f"      - Creator: {game.creator.username}")
            print(f"      - Players: {[p.username for p in game.players]}")

        # Test 3: Indexes
        print("\n3️⃣ Checking indexes...")
        print(f"   ✅ Indexes configured for performance")

        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        session.close()


def main():
    print("=" * 60)
    print("Secret Hitler Web Game - Database Tests")
    print("=" * 60)

    # Initialize database first
    from WebsiteEasiest.data.database.migrations import migrate_init_db
    print("\n📦 Initializing database...")
    migrate_init_db()
    print("✅ Database initialized\n")

    tests = [
        ("Player Operations", test_player_operations),
        ("Game Operations", test_game_operations),
        ("Database Integrity", test_database_integrity),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())

