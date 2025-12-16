from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from InfoLog import InfoLog
    from player import Player
    from GameLog import GameLog

INFO_LOGS: list[InfoLog] = []
GAME_LOGS: list[GameLog] = []
COUNT_PLAYERS:int = None
PLAYERS: list[Player] = []
ROLES: list[str] = []
HITLER:int = None
STALIN:int = None
PURGED: set[Player] = set()
GULAG: int = None
KILLED: int = None
cards: dict[str, int] = {"BLACK":0,}
