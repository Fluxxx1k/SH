from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from Players.abstract_player import AbstractPlayer
    from InfoLog import InfoLog
    from GameLog import GameLog

INFO_LOGS: list[InfoLog] = []
GAME_LOGS: list[GameLog] = []
# noinspection PyTypeChecker
COUNT_PLAYERS:int = None
PLAYERS: list[AbstractPlayer] = []
ROLES: list[str] = []
HITLER:int|None = None
STALIN:int|None = None
PURGED: set[AbstractPlayer] = set()
GULAG: int|None = None
KILLED: int|None = None
CARDS: dict[str, int] = {"BLACK":0, "RED":0}
BOTS: list[int] = []
