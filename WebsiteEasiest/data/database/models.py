"""
SQLAlchemy models for Secret Hitler Web Game.
Defines database schema for players, games, and game states.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Table, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from WebsiteEasiest.data.database import Base


# Association table for many-to-many relationship between games and players
game_players = Table(
    'game_players',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('game.id'), primary_key=True),
    Column('player_id', Integer, ForeignKey('player.id'), primary_key=True)
)


class GameStatus(str, enum.Enum):
    """Game status enumeration."""
    CREATED = "created"
    WAITING_FOR_START = "waiting_for_start"
    PLAYING = "playing"
    FINISHED = "finished"


class Player(Base):
    """Player model."""
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Statistics
    games_played = Column(Integer, default=0, nullable=False)
    games_won = Column(Integer, default=0, nullable=False)

    # Relationships
    games = relationship("Game", secondary=game_players, back_populates="players")
    created_games = relationship("Game", foreign_keys="Game.created_by_id", back_populates="creator")
    game_players = relationship("GamePlayer", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, username='{self.username}')>"


class Game(Base):
    """Game model."""
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    status = Column(Enum(GameStatus), default=GameStatus.CREATED, nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey('player.id'), nullable=False)
    password = Column(String(255), nullable=True)  # Hashed password if game is private
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    # Game settings (stored as JSON)
    settings = Column(JSON, nullable=True)

    # Current game state (stored as JSON)
    current_state = Column(JSON, nullable=True)

    # Relationships
    creator = relationship("Player", foreign_keys=[created_by_id], back_populates="created_games")
    players = relationship("Player", secondary=game_players, back_populates="games")
    game_players = relationship("GamePlayer", back_populates="game", cascade="all, delete-orphan")
    logs = relationship("GameLog", back_populates="game", cascade="all, delete-orphan")
    result = relationship("GameResult", uselist=False, back_populates="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Game(id={self.id}, name='{self.name}', status={self.status})>"


class GamePlayer(Base):
    """Association model for player participation in games with role information."""
    __tablename__ = 'game_player'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False, index=True)

    # Game role (e.g., "hitler", "communist", "liberal", etc.)
    role = Column(String(50), nullable=True)

    # Player status in game
    is_alive = Column(Boolean, default=True, nullable=False)
    is_president = Column(Boolean, default=False, nullable=False)
    is_chancellor = Column(Boolean, default=False, nullable=False)

    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)

    # Player actions and votes (stored as JSON)
    votes = Column(JSON, nullable=True)  # {"vote_type": "yes/no", "target": "...", "timestamp": "..."}
    actions = Column(JSON, nullable=True)

    # Relationships
    game = relationship("Game", back_populates="game_players")
    player = relationship("Player", back_populates="game_players")

    def __repr__(self):
        return f"<GamePlayer(game_id={self.game_id}, player_id={self.player_id}, role='{self.role}')>"


class GameLog(Base):
    """Game event log."""
    __tablename__ = 'game_log'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'), nullable=False, index=True)

    # Log type: action, vote, result, state_change, etc.
    log_type = Column(String(50), nullable=False, index=True)

    # Player involved (optional)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=True)

    # Detailed log data
    data = Column(JSON, nullable=True)

    # Message for display
    message = Column(Text, nullable=True)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    game = relationship("Game", back_populates="logs")

    def __repr__(self):
        return f"<GameLog(id={self.id}, game_id={self.game_id}, log_type='{self.log_type}')>"


class GameResult(Base):
    """Game result/outcome."""
    __tablename__ = 'game_result'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('game.id'), unique=True, nullable=False)

    # Winning side: "red" (liberals) or "black" (communists/fascists)
    winning_side = Column(String(20), nullable=False)

    # Winner details
    winner_name = Column(String(50), nullable=True)  # For special roles like "hitler" or "stalin"

    # Game duration
    finished_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration_seconds = Column(Integer, nullable=True)

    # Result details (stored as JSON)
    details = Column(JSON, nullable=True)

    # Relationships
    game = relationship("Game", back_populates="result")

    def __repr__(self):
        return f"<GameResult(id={self.id}, game_id={self.game_id}, winning_side='{self.winning_side}')>"


class IPLog(Base):
    """IP address log for security."""
    __tablename__ = 'ip_log'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('player.id'), nullable=False, index=True)
    ip_address = Column(String(45), nullable=False)  # IPv4 or IPv6
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    is_creation = Column(Boolean, default=False, nullable=False)  # True if account creation IP

    def __repr__(self):
        return f"<IPLog(player_id={self.player_id}, ip='{self.ip_address}')>"

