"""
Player management module using SQLAlchemy.
Replaces JSON-based player storage with database operations.
Provides compatibility layer with existing code.
"""

from typing import Optional, Tuple
from flask import request

from WebsiteEasiest.logger import logger
from WebsiteEasiest.data.database import get_session
from WebsiteEasiest.data.database.repositories import PlayerRepository, IPLogRepository
from WebsiteEasiest.settings.web_config import denied_literals


def create_player_db(player_name: str, player_password: str) -> Tuple[bool, Optional[str]]:
    """
    Create a new player in the database.

    Args:
        player_name: Username
        player_password: Password (will be hashed)

    Returns:
        (success, error_message)
    """
    session = get_session()
    try:
        # Validate input
        if len(player_name) < 3:
            return False, "Player name cannot be less than 3 characters"
        if len(player_password) < 3:
            return False, "Player password cannot be less than 3 characters"
        if any(char in player_name for char in denied_literals):
            return False, f"Player name cannot contain special characters"

        # Create player
        success, error, player = PlayerRepository.create(session, player_name, player_password)
        if not success:
            return False, error

        # Log IP on account creation
        ip_address = get_client_ip()
        if ip_address:
            IPLogRepository.log_ip(session, player.id, ip_address, is_creation=True)

        logger.info(f"Player created: {player_name}")
        return True, None
    except Exception as e:
        logger.error(f"Error creating player {player_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def get_data_of_player_db(player_name: str) -> Tuple[bool, dict | str]:
    """
    Get player data from database.

    Returns:
        (success, player_data_dict or error_message)
    """
    session = get_session()
    try:
        player = PlayerRepository.get_by_username(session, player_name)
        if not player:
            return False, f"Player '{player_name}' not found"

        player_data = {
            'id': player.id,
            'player_name': player.username,
            'email': player.email,
            'created_at': player.created_at.isoformat() if player.created_at else None,
            'last_login': player.last_login.isoformat() if player.last_login else None,
            'is_active': player.is_active,
            'games_played': player.games_played,
            'games_won': player.games_won,
        }
        return True, player_data
    except Exception as e:
        logger.error(f"Error getting player data for {player_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def login_player_db(player_name: str, player_password: str) -> Tuple[bool, Optional[str]]:
    """
    Authenticate player with username and password.

    Returns:
        (success, error_message)
    """
    session = get_session()
    try:
        if len(player_name) < 3:
            return False, "Player name cannot be less than 3 characters"

        # Authenticate
        success, error, player = PlayerRepository.authenticate(session, player_name, player_password)
        if not success:
            return False, error

        # Log IP on successful login
        ip_address = get_client_ip()
        if ip_address:
            IPLogRepository.log_ip(session, player.id, ip_address, is_creation=False)

        logger.info(f"Player logged in: {player_name}")
        return True, None
    except Exception as e:
        logger.error(f"Error logging in player {player_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def exists_player_db(player_name: str) -> bool:
    """Check if player exists in database."""
    session = get_session()
    try:
        player = PlayerRepository.get_by_username(session, player_name)
        return player is not None
    except Exception as e:
        logger.error(f"Error checking if player exists {player_name}: {repr(e)}")
        return False
    finally:
        session.close()


def count_players_db() -> int:
    """Count total players in database."""
    session = get_session()
    try:
        return PlayerRepository.count_all(session)
    except Exception as e:
        logger.error(f"Error counting players: {repr(e)}")
        return 0
    finally:
        session.close()


def get_client_ip() -> Optional[str]:
    """Get client IP address from request."""
    try:
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr
    except Exception as e:
        logger.warning(f"Error getting client IP: {repr(e)}")
        return None


def add_game_to_player_db(player_name: str, game_id: str) -> Tuple[bool, Optional[str]]:
    """
    Add or update player's current game.
    Note: This is a simplified version. In full implementation,
    use GameRepository.add_player() to add player to game_players table.
    """
    logger.debug(f"Game association for player {player_name} updated to game {game_id}")
    return True, None


def save_ip_db(player_name: str, creator: bool = False, success: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Log IP address for a player.
    This is a compatibility wrapper for existing code.
    """
    session = get_session()
    try:
        player = PlayerRepository.get_by_username(session, player_name)
        if not player:
            return False, f"Player '{player_name}' not found"

        ip_address = get_client_ip()
        if not ip_address:
            return False, "Could not determine client IP"

        IPLogRepository.log_ip(session, player.id, ip_address, is_creation=creator)
        return True, None
    except Exception as e:
        logger.error(f"Error saving IP for player {player_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()

