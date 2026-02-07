"""
Data Access Objects (Repositories) for database operations.
Provides abstraction layer for database queries.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from WebsiteEasiest.data.database.models import (
    Player, Game, GamePlayer, GameLog, GameResult, GameStatus, IPLog
)
from WebsiteEasiest.logger import logger


class PlayerRepository:
    """Repository for Player operations."""

    @staticmethod
    def create(session: Session, username: str, password: str, email: str = None) -> tuple[bool, Optional[str], Optional[Player]]:
        """
        Create a new player.

        Returns:
            (success, error_message, player)
        """
        try:
            if len(username) < 3:
                return False, "Username must be at least 3 characters", None
            if len(password) < 3:
                return False, "Password must be at least 3 characters", None

            # Check if player already exists
            existing = session.query(Player).filter(Player.username == username).first()
            if existing:
                return False, f"Player '{username}' already exists", None

            # Create new player
            player = Player(
                username=username,
                password_hash=generate_password_hash(password),
                email=email,
                is_active=True
            )
            session.add(player)
            session.commit()
            logger.info(f"Created new player: {username}")
            return True, None, player
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating player {username}: {repr(e)}")
            return False, str(e), None

    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[Player]:
        """Get player by username."""
        try:
            return session.query(Player).filter(Player.username == username).first()
        except Exception as e:
            logger.error(f"Error getting player {username}: {repr(e)}")
            return None

    @staticmethod
    def get_by_id(session: Session, player_id: int) -> Optional[Player]:
        """Get player by ID."""
        try:
            return session.query(Player).filter(Player.id == player_id).first()
        except Exception as e:
            logger.error(f"Error getting player {player_id}: {repr(e)}")
            return None

    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> tuple[bool, Optional[str], Optional[Player]]:
        """
        Authenticate player with username and password.

        Returns:
            (success, error_message, player)
        """
        try:
            player = PlayerRepository.get_by_username(session, username)
            if not player:
                return False, f"Player '{username}' not found", None

            if not check_password_hash(player.password_hash, password):
                return False, "Invalid password", None

            # Update last login
            player.last_login = datetime.utcnow()
            session.commit()
            logger.info(f"Player authenticated: {username}")
            return True, None, player
        except Exception as e:
            session.rollback()
            logger.error(f"Error authenticating player {username}: {repr(e)}")
            return False, str(e), None

    @staticmethod
    def update_stats(session: Session, player_id: int, won: bool = False):
        """Update player statistics."""
        try:
            player = PlayerRepository.get_by_id(session, player_id)
            if player:
                player.games_played += 1
                if won:
                    player.games_won += 1
                session.commit()
                logger.debug(f"Updated stats for player {player_id}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating stats for player {player_id}: {repr(e)}")

    @staticmethod
    def count_all(session: Session) -> int:
        """Count total players."""
        try:
            return session.query(Player).count()
        except Exception as e:
            logger.error(f"Error counting players: {repr(e)}")
            return 0


class GameRepository:
    """Repository for Game operations."""

    @staticmethod
    def create(session: Session, name: str, created_by_id: int,
               password: str = None, settings: dict = None) -> tuple[bool, Optional[str], Optional[Game]]:
        """
        Create a new game.

        Returns:
            (success, error_message, game)
        """
        try:
            if len(name) < 3:
                return False, "Game name must be at least 3 characters", None

            # Check if game already exists
            existing = session.query(Game).filter(Game.name == name).first()
            if existing:
                return False, f"Game '{name}' already exists", None

            # Create new game
            game = Game(
                name=name,
                created_by_id=created_by_id,
                password=generate_password_hash(password) if password else None,
                settings=settings or {},
                status=GameStatus.CREATED
            )
            session.add(game)
            session.commit()
            logger.info(f"Created new game: {name} by player {created_by_id}")
            return True, None, game
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating game {name}: {repr(e)}")
            return False, str(e), None

    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Game]:
        """Get game by name."""
        try:
            return session.query(Game).filter(Game.name == name).first()
        except Exception as e:
            logger.error(f"Error getting game {name}: {repr(e)}")
            return None

    @staticmethod
    def get_by_id(session: Session, game_id: int) -> Optional[Game]:
        """Get game by ID."""
        try:
            return session.query(Game).filter(Game.id == game_id).first()
        except Exception as e:
            logger.error(f"Error getting game {game_id}: {repr(e)}")
            return None

    @staticmethod
    def get_active_games(session: Session) -> List[Game]:
        """Get all active games."""
        try:
            return session.query(Game).filter(
                Game.status.in_([GameStatus.CREATED, GameStatus.WAITING_FOR_START, GameStatus.PLAYING])
            ).all()
        except Exception as e:
            logger.error(f"Error getting active games: {repr(e)}")
            return []

    @staticmethod
    def get_finished_games(session: Session) -> List[Game]:
        """Get all finished games."""
        try:
            return session.query(Game).filter(Game.status == GameStatus.FINISHED).all()
        except Exception as e:
            logger.error(f"Error getting finished games: {repr(e)}")
            return []

    @staticmethod
    def add_player(session: Session, game_id: int, player_id: int) -> tuple[bool, Optional[str]]:
        """Add player to game."""
        try:
            # Check if player already in game
            existing = session.query(GamePlayer).filter(
                and_(GamePlayer.game_id == game_id, GamePlayer.player_id == player_id)
            ).first()
            if existing:
                return False, "Player already in this game"

            game_player = GamePlayer(game_id=game_id, player_id=player_id)
            session.add(game_player)
            session.commit()
            logger.debug(f"Added player {player_id} to game {game_id}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error adding player {player_id} to game {game_id}: {repr(e)}")
            return False, str(e)

    @staticmethod
    def remove_player(session: Session, game_id: int, player_id: int) -> tuple[bool, Optional[str]]:
        """Remove player from game."""
        try:
            game_player = session.query(GamePlayer).filter(
                and_(GamePlayer.game_id == game_id, GamePlayer.player_id == player_id)
            ).first()
            if not game_player:
                return False, "Player not in this game"

            session.delete(game_player)
            session.commit()
            logger.debug(f"Removed player {player_id} from game {game_id}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error removing player {player_id} from game {game_id}: {repr(e)}")
            return False, str(e)

    @staticmethod
    def update_status(session: Session, game_id: int, status: GameStatus) -> tuple[bool, Optional[str]]:
        """Update game status."""
        try:
            game = GameRepository.get_by_id(session, game_id)
            if not game:
                return False, "Game not found"

            game.status = status
            if status == GameStatus.PLAYING:
                game.started_at = datetime.utcnow()
            elif status == GameStatus.FINISHED:
                game.finished_at = datetime.utcnow()

            session.commit()
            logger.debug(f"Updated game {game_id} status to {status}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating game {game_id} status: {repr(e)}")
            return False, str(e)

    @staticmethod
    def update_state(session: Session, game_id: int, state: dict) -> tuple[bool, Optional[str]]:
        """Update game current state."""
        try:
            game = GameRepository.get_by_id(session, game_id)
            if not game:
                return False, "Game not found"

            game.current_state = state
            session.commit()
            logger.debug(f"Updated game {game_id} state")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating game {game_id} state: {repr(e)}")
            return False, str(e)

    @staticmethod
    def count_active(session: Session) -> int:
        """Count active games."""
        try:
            return session.query(Game).filter(
                Game.status.in_([GameStatus.CREATED, GameStatus.WAITING_FOR_START, GameStatus.PLAYING])
            ).count()
        except Exception as e:
            logger.error(f"Error counting active games: {repr(e)}")
            return 0

    @staticmethod
    def count_finished(session: Session) -> int:
        """Count finished games."""
        try:
            return session.query(Game).filter(Game.status == GameStatus.FINISHED).count()
        except Exception as e:
            logger.error(f"Error counting finished games: {repr(e)}")
            return 0


class GameLogRepository:
    """Repository for GameLog operations."""

    @staticmethod
    def create(session: Session, game_id: int, log_type: str,
               data: dict = None, message: str = None, player_id: int = None) -> tuple[bool, Optional[str]]:
        """Create a new game log entry."""
        try:
            log_entry = GameLog(
                game_id=game_id,
                log_type=log_type,
                player_id=player_id,
                data=data,
                message=message
            )
            session.add(log_entry)
            session.commit()
            logger.debug(f"Created log entry for game {game_id}: {log_type}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating log for game {game_id}: {repr(e)}")
            return False, str(e)

    @staticmethod
    def get_game_logs(session: Session, game_id: int) -> List[GameLog]:
        """Get all logs for a game."""
        try:
            return session.query(GameLog).filter(GameLog.game_id == game_id).order_by(GameLog.timestamp).all()
        except Exception as e:
            logger.error(f"Error getting logs for game {game_id}: {repr(e)}")
            return []


class GameResultRepository:
    """Repository for GameResult operations."""

    @staticmethod
    def create(session: Session, game_id: int, winning_side: str,
               winner_name: str = None, details: dict = None) -> tuple[bool, Optional[str]]:
        """Create a new game result."""
        try:
            result = GameResult(
                game_id=game_id,
                winning_side=winning_side,
                winner_name=winner_name,
                details=details
            )
            session.add(result)
            session.commit()
            logger.info(f"Created result for game {game_id}: {winning_side}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating result for game {game_id}: {repr(e)}")
            return False, str(e)

    @staticmethod
    def get_by_game_id(session: Session, game_id: int) -> Optional[GameResult]:
        """Get result for a game."""
        try:
            return session.query(GameResult).filter(GameResult.game_id == game_id).first()
        except Exception as e:
            logger.error(f"Error getting result for game {game_id}: {repr(e)}")
            return None


class IPLogRepository:
    """Repository for IP log operations."""

    @staticmethod
    def log_ip(session: Session, player_id: int, ip_address: str, is_creation: bool = False) -> tuple[bool, Optional[str]]:
        """Log IP address for a player."""
        try:
            ip_log = IPLog(
                player_id=player_id,
                ip_address=ip_address,
                is_creation=is_creation
            )
            session.add(ip_log)
            session.commit()
            logger.debug(f"Logged IP {ip_address} for player {player_id}")
            return True, None
        except Exception as e:
            session.rollback()
            logger.error(f"Error logging IP for player {player_id}: {repr(e)}")
            return False, str(e)

