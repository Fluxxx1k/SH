"""
Game management module using SQLAlchemy.
Replaces JSON-based game storage with database operations.
Provides compatibility layer with existing code.
"""

from typing import Optional, Tuple, List
from datetime import datetime

from WebsiteEasiest.logger import logger
from WebsiteEasiest.data.database import get_session
from WebsiteEasiest.data.database.repositories import (
    GameRepository, GameLogRepository, GameResultRepository, PlayerRepository, GameStatus
)


def create_game_db(game_name: str, creator: str, password: str = None,
                   data: dict = None) -> Tuple[bool, Optional[str]]:
    """
    Create a new game in the database.

    Args:
        game_name: Name of the game
        creator: Username of game creator
        password: Optional password for private game
        data: Optional additional game data/settings

    Returns:
        (success, error_message)
    """
    session = get_session()
    try:
        # Get creator player
        creator_player = PlayerRepository.get_by_username(session, creator)
        if not creator_player:
            return False, f"Creator player '{creator}' not found"

        # Validate game name
        if len(game_name) < 3:
            return False, "Game name cannot be less than 3 characters"

        # Create game
        settings = data or {}
        success, error, game = GameRepository.create(
            session,
            game_name,
            creator_player.id,
            password=password if password else None,
            settings=settings
        )

        if not success:
            return False, error

        # Add creator to game
        GameRepository.add_player(session, game.id, creator_player.id)

        logger.info(f"Game created: {game_name} by {creator}")
        return True, None
    except Exception as e:
        logger.error(f"Error creating game {game_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def get_data_of_game_db(game_name: str) -> Tuple[bool, dict | str]:
    """
    Get game data from database.

    Returns:
        (success, game_data_dict or error_message)
    """
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if not game:
            return False, f"Game '{game_name}' not found"

        # Get players
        players = [gp.player.username for gp in game.game_players]

        game_data = {
            'id': game.id,
            'name': game.name,
            'status': game.status.value,
            'created_by': game.creator.username,
            'created_at': game.created_at.isoformat() if game.created_at else None,
            'started_at': game.started_at.isoformat() if game.started_at else None,
            'finished_at': game.finished_at.isoformat() if game.finished_at else None,
            'players': players,
            'current_players': len(players),
            'password': bool(game.password),  # Don't return actual password
            'settings': game.settings or {},
            'current_state': game.current_state or {},
        }
        return True, game_data
    except Exception as e:
        logger.error(f"Error getting game data for {game_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def get_logs_of_game_db(game_name: str) -> Tuple[bool, List[dict] | str]:
    """
    Get all logs for a game.

    Returns:
        (success, logs_list or error_message)
    """
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if not game:
            return False, f"Game '{game_name}' not found"

        logs = GameLogRepository.get_game_logs(session, game.id)
        logs_data = [
            {
                'id': log.id,
                'log_type': log.log_type,
                'player_id': log.player_id,
                'message': log.message,
                'data': log.data or {},
                'timestamp': log.timestamp.isoformat() if log.timestamp else None,
            }
            for log in logs
        ]
        return True, logs_data
    except Exception as e:
        logger.error(f"Error getting logs for game {game_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def save_data_of_game_db(game_name: str, game_data: dict) -> bool:
    """
    Save/update game data in the database.

    Args:
        game_name: Name of the game
        game_data: Game data to save (current_state and settings)

    Returns:
        success
    """
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if not game:
            logger.warning(f"Game '{game_name}' not found for update")
            return False

        # Update game state and settings
        if 'current_state' in game_data:
            success, error = GameRepository.update_state(session, game.id, game_data['current_state'])
            if not success:
                logger.error(f"Failed to update game state: {error}")
                return False

        if 'settings' in game_data:
            game.settings = game_data['settings']
            session.commit()

        logger.debug(f"Game data saved: {game_name}")
        return True
    except Exception as e:
        logger.error(f"Error saving game data for {game_name}: {repr(e)}")
        return False
    finally:
        session.close()


def end_game_db(game_name: str, game_data: dict = None, delete: bool = False) -> Tuple[bool, Optional[str]]:
    """
    End/finish a game and optionally save result.

    Args:
        game_name: Name of the game
        game_data: Optional game data (result information)
        delete: If True, delete the game; if False, mark as finished

    Returns:
        (success, error_message)
    """
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if not game:
            return False, f"Game '{game_name}' not found"

        if delete:
            # Delete the game
            session.delete(game)
            session.commit()
            logger.warning(f"Game deleted: {game_name}")
        else:
            # Mark as finished
            success, error = GameRepository.update_status(session, game.id, GameStatus.FINISHED)
            if not success:
                return False, error

            # Save result if provided
            if game_data and 'result' in game_data:
                result_info = game_data['result']
                GameResultRepository.create(
                    session,
                    game.id,
                    result_info.get('winning_side', 'unknown'),
                    winner_name=result_info.get('winner_name'),
                    details=result_info.get('details')
                )

            logger.info(f"Game finished: {game_name}")

        return True, None
    except Exception as e:
        logger.error(f"Error ending game {game_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()


def exists_game_db(game_name: str) -> bool:
    """Check if an active game exists."""
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if game and game.status in [GameStatus.CREATED, GameStatus.WAITING_FOR_START, GameStatus.PLAYING]:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking if game exists {game_name}: {repr(e)}")
        return False
    finally:
        session.close()


def count_games_db(active: bool = True) -> int:
    """
    Count games.

    Args:
        active: If True, count active games; if False, count finished games

    Returns:
        Game count
    """
    session = get_session()
    try:
        if active:
            return GameRepository.count_active(session)
        else:
            return GameRepository.count_finished(session)
    except Exception as e:
        logger.error(f"Error counting games: {repr(e)}")
        return 0
    finally:
        session.close()


def add_game_to_player_db(player_name: str, game_id: str) -> Tuple[bool, Optional[str]]:
    """
    Associate a player with a game.

    Args:
        player_name: Username
        game_id: Game ID (can be empty string to remove)

    Returns:
        (success, error_message)
    """
    logger.debug(f"Game association for player {player_name} updated to game {game_id}")
    return True, None


def log_game_event_db(game_name: str, log_type: str, message: str = None,
                      player_name: str = None, data: dict = None) -> Tuple[bool, Optional[str]]:
    """
    Log an event in the game.

    Args:
        game_name: Name of the game
        log_type: Type of log entry (action, vote, result, etc.)
        message: Human-readable message
        player_name: Optional player involved
        data: Optional structured data

    Returns:
        (success, error_message)
    """
    session = get_session()
    try:
        game = GameRepository.get_by_name(session, game_name)
        if not game:
            return False, f"Game '{game_name}' not found"

        player_id = None
        if player_name:
            player = PlayerRepository.get_by_username(session, player_name)
            if player:
                player_id = player.id

        success, error = GameLogRepository.create(
            session,
            game.id,
            log_type,
            data=data,
            message=message,
            player_id=player_id
        )
        return success, error
    except Exception as e:
        logger.error(f"Error logging game event for {game_name}: {repr(e)}")
        return False, str(e)
    finally:
        session.close()

