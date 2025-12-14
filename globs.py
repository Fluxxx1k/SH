from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from InfoLog import InfoLog
    from player import Player

LOGS: list[InfoLog] = []
COUNT_PLAYERS:int = None
PLAYERS: list[Player] = []
ROLES: list[str] = []
HITLER:int = None
STALIN:int = None
PURGED: set[Player] = set()
