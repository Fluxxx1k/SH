from __future__ import annotations

import atexit
from typing import Optional, TYPE_CHECKING, List
from abc import ABC, abstractmethod

from core.globalstorage import GlobalStorage
from user_settings import BLACK_WIN_NUM, RED_WIN_NUM
import random as rnd
if TYPE_CHECKING:
    from io import TextIOWrapper
    from core.players.abstract_player import AbstractPlayer
    from core.logs.gamelog import GameLog
    from core.logs.infolog import InfoLog



class AbstractGame(ABC):
    def __init__(self, id: int, name: str, players: list[AbstractPlayer], description: str, image: str):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.globs = GlobalStorage(name)
        self.players: List[AbstractPlayer] = players
        self.game_log_file: Optional[TextIOWrapper|str] = None
        self.info_log_file: Optional[TextIOWrapper|str] = None
        self.prs: AbstractPlayer = None
        self.skips: int = 0
        self.previous_president: AbstractPlayer = None
        self.previous_chancellor: AbstractPlayer = None
        self.definitely_not_hitter = set()
        self.saved_cards: Optional[list[str]] = None
        self.deck: list[str]
        self.globs.ACTIVE_GAME = True
        self.globs.COUNT_PLAYERS = len(players)
        if self.globs.COUNT_PLAYERS == 6:
            self.red_start = 5
            self.black_start = 11
        else:
            self.red_start = 6
            self.black_start = 11
        self.deck = ['R'] * self.red_start + ['B'] * self.black_start
        rnd.shuffle(self.deck)
        self.checks = 1
        self.cnc: Optional[AbstractPlayer] = None
        self.out_of_queue_president: Optional[AbstractPlayer] = None

    @abstractmethod
    def take_move(self):
        ...


    def take_random(self, c: int) -> list[str]:
        if self.saved_cards:
            x = self.saved_cards.copy()
            self.saved_cards = None
            return x
        try:
            chosen = rnd.sample(self.deck, k=c)
        except ValueError:
            self.globs.GAME_LOGS.append(
                GameLog(special=f"self.deck resetting<br>RED: {self.red_start - self.red}<br>BLACK: {self.black_start - self.black}",
                        is_cards=False))
            self.deck = ["R"] * (self.red_start - self.red) + ["B"] * (self.black_start - self.black)
            chosen = rnd.sample(self.deck, k=c)
        for card in chosen:
            self.deck.remove(card)
        return sorted(chosen)


    def __str__(self):
        return f"{self.__name__}(id={self.id}, name='{self.name}', description='{self.description}', image='{self.image}')"

    def __repr__(self):
        return f"{self.__name__}({', '.join(f'{i}= {j}' for i, j in self.__dict__.items())})"

    def __eq__(self, other):
        if not isinstance(other, AbstractGame):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.image == other.image
        )

    def __hash__(self):
        return hash((self.id, self.name, self.description, self.image))

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return str(self.to_dict()).replace("'", '"')

    def is_end(self):
        if self.globs.BLACK >= BLACK_WIN_NUM:
            return 1
        if self.globs.HIT_CHANCELLOR:
            return 1
        if self.globs.RED >= RED_WIN_NUM:
            return -1
        if self.globs.HIT_CAPUT:
            return -1
        if self.globs.HIT_CHANCELLOR_STAL_PRESIDENT:
            return -1
        return 0

    @abstractmethod
    def take_move(self):
        pass

    @abstractmethod
    def stop_game(self):
        pass


    def accept_player(self, player: AbstractPlayer, chooser: AbstractPlayer = None) -> bool:
        if player in self.globs.PURGED:
            return False
        if player == self.prs:
            return False
        if player not in self.players:
            return False
        if player.num == self.prs.num:
            return False
        if player.num == self.globs.GULAG:
            return False
        if player.num == self.globs.KILLED:
            return False
        if chooser is not None:
            if chooser not in self.players:
                return False
            if chooser.num == self.globs.GULAG:
                return False
            if chooser.num == self.globs.KILLED:
                return False
        return True





