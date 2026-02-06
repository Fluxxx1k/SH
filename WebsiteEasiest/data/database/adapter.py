"""
Compatibility adapter to migrate from JSON file storage to database.
This module provides wrapper functions that redirect calls from
database_py module to new database implementation.
"""

from WebsiteEasiest.data.database.player_operations import (
    create_player_db, get_data_of_player_db, login_player_db,
    exists_player_db, count_players_db, add_game_to_player_db, save_ip_db
)
from WebsiteEasiest.data.database.game_operations import (
    create_game_db, get_data_of_game_db, get_logs_of_game_db,
    save_data_of_game_db, end_game_db, exists_game_db,
    count_games_db, add_game_to_player_db as add_game_to_player_db_game,
    log_game_event_db
)
from WebsiteEasiest.logger import logger


# Re-export functions with original names for compatibility

__all__ = [
    # Player functions
    'create_player',
    'get_data_of_player',
    'login_player',
    'exists_player',
    'count_players',
    'add_game_to_player',
    'save_ip',

    # Game functions
    'create_game_db',
    'get_data_of_game',
    'get_logs_of_game',
    'save_data_of_game',
    'end_game_db',
    'exists_game',
    'count_games',
    'log_game_event',
]


def create_player(player_name: str, player_password: str) -> tuple:
    """Create player (wrapper)."""
    logger.debug(f"create_player called: {player_name}")
    return create_player_db(player_name, player_password)


def get_data_of_player(player_name: str) -> tuple:
    """Get player data (wrapper)."""
    return get_data_of_player_db(player_name)


def login_player(player_name: str, player_password: str) -> tuple:
    """Login player (wrapper)."""
    return login_player_db(player_name, player_password)


def exists_player(player_name: str, default_on_error: bool = True) -> bool:
    """Check if player exists (wrapper)."""
    result = exists_player_db(player_name)
    if result is None:
        return default_on_error
    return result


def count_players(default_on_error: int = 0) -> int:
    """Count players (wrapper)."""
    result = count_players_db()
    if result is None:
        return default_on_error
    return result


def add_game_to_player(player_name: str, game_id: str) -> tuple:
    """Add game to player (wrapper)."""
    return add_game_to_player_db(player_name, game_id)


def save_ip(player_name: str, creator: bool = False, success: bool = False) -> tuple:
    """Save IP (wrapper)."""
    return save_ip_db(player_name, creator=creator, success=success)


def get_data_of_game(game_name: str) -> tuple:
    """Get game data (wrapper)."""
    return get_data_of_game_db(game_name)


def get_logs_of_game(game_name: str) -> tuple:
    """Get game logs (wrapper)."""
    return get_logs_of_game_db(game_name)


def save_data_of_game(game_name: str, game_data: dict) -> bool:
    """Save game data (wrapper)."""
    return save_data_of_game_db(game_name, game_data)


def exists_game(game_name: str, default_on_error: bool = True) -> bool:
    """Check if game exists (wrapper)."""
    result = exists_game_db(game_name)
    if result is None:
        return default_on_error
    return result


def count_games(active: bool = True, default_on_error: int = 0) -> int:
    """Count games (wrapper)."""
    result = count_games_db(active=active)
    if result is None:
        return default_on_error
    return result


def log_game_event(game_name: str, log_type: str, message: str = None,
                   player_name: str = None, data: dict = None) -> tuple:
    """Log game event (wrapper)."""
    return log_game_event_db(game_name, log_type, message=message,
                            player_name=player_name, data=data)

