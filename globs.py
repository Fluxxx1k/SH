from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Players.abstract_player import AbstractPlayer
    from InfoLog import InfoLog
    from GameLog import GameLog

INFO_LOGS: list[InfoLog] = []
GAME_LOGS: list[GameLog] = []
COUNT_PLAYERS:int = None
PLAYERS: list[AbstractPlayer] = []
ROLES: list[str] = []
HITLER:int = None
STALIN:int = None
PURGED: set[AbstractPlayer] = set()
GULAG: int = None
KILLED: int = None
CARDS: dict[str, int] = {"BLACK":0, "RED":0}
BOTS: list[int] = []
