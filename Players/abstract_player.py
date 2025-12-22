from __future__ import annotations
from typing import Iterable, Literal
import datetime

from core.infolog import InfoLog
from core.globs import INFO_LOGS, PLAYERS
from abc import abstractmethod, ABC

from cli.colors import (BLUE_TEXT_BRIGHT as BLUE,
                        CYAN_TEXT_BRIGHT as CYAN,
                        YELLOW_TEXT_BRIGHT as YELLOW,
                        RESET_TEXT as END_T,
                        YELLOW_BACKGROUND_BRIGHT as GULAG,
                        RED_BACKGROUND_BRIGHT as DEAD,
                        RESET_BACKGROUND as END_BG,
                        )
from core.standard_names_SH import X
from user_settings import MAX_NAME_LEN
from core.utils import get_color, naming


class AbstractPlayer(ABC):
    base_name = "Player"

    def __init__(self, num: int, name: str, role: str):
        self.gov_pref: str = ''
        self.gov_suff: str = ''
        self.purge_pref: str = ''
        self.purge_suff: str = ''
        self.num: int = num
        self.role: str = role
        self.color = get_color(self.role, out_type=X.BOT)
        if self.color == X.HITLER:
            self.color = X.BLACK
        self.colored_color: str = get_color(self.role)
        self.prefix: str = ''
        self.suffix: str = ''
        if name == '' or not isinstance(name, str):
            self.name: str = self.base_name + str(num)
        else:
            self.name: str = name
        self.tablet_name: str = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark: float = 0
        self.black: set[int] = set()
        self.contr: int = 0

    def __repr__(self):
        s = '[Info: '
        for name, value in self.__dict__.items():
            s += f"({name}: {repr(value)}) "
        s = s[:-1] + ']'
        return s

    def __hash__(self):
        return hash(self.name)

    def __add__(self, s):
        print(f"Add {s} to suffix of {self.name}")
        self.suffix += s
        return self

    def __radd__(self, s):
        print(f"Add {s} to prefix of {self.name}")
        self.prefix += s
        return self
    def __or__(self, other):
        return None

    def __str__(self):
        return self.name

    def __eq__(self, other: "Player str"):
        if type(other) == str:
            if self.name == other:
                return True
            return False
        if self.name == other.name:
            return True
        return False

    def __lt__(self, other):
        if self.dark < other.dark:
            return True
        return False

    def __le__(self, other):
        if self.dark <= other.dark:
            return True
        return False

    def __gt__(self, other):
        if self.dark > other.dark:
            return True
        return False

    def __ge__(self, other):
        if self.dark >= other.dark:
            return True
        return False

    def __format__(self, *args, **kwargs):
        return str(self).format(*args, **kwargs)


    def degov(self):
        self.gov_suff = ''
        self.gov_pref = ''

    def free(self):
        x = self.purge_pref == GULAG
        if x:
            print(f"{self.name} freed")
            self.purge_pref = self.purge_suff = ''
        else:

            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"{self.name} wasn't in gulag!!",
                                     info1=f'player= {self.name}',
                                     info2=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print(f"{self.name} wasn't in gulag!!")

    def chosen_gov(self, gov_type):
        if gov_type == X.PRESIDENT:
            self.gov_pref = CYAN
        elif gov_type == X.CHANCELLOR:
            self.gov_pref = YELLOW
        else:
            self.gov_pref = BLUE
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown government type: {gov_type= }",
                                     info1=f'player= {self.name}',
                                     info2=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.gov_suff = END_T

    def purge(self, purge_type):
        self.degov()
        if purge_type == X.GULAG:
            self.purge_pref = GULAG
        elif purge_type == X.KILLED:
            self.purge_pref = DEAD
        else:
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown purge type: {purge_type= }",
                                     info1=f'player= {self.name}',
                                     info2=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.purge_pref = BLUE
        self.purge_suff = END_BG

    def table(self) -> str:
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix

    def out(self) -> str:
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix

    @abstractmethod
    def president(self, cards: str | list[str], cnc: "AbstractPlayer"):
        pass
    @abstractmethod
    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
        pass
    @abstractmethod
    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        pass
    @abstractmethod
    def check_cards(self, cards: str) -> str:
        pass

    @abstractmethod
    def check_player(self) -> tuple[int, str]:
        """Returns player number and named color"""
        pass
    @abstractmethod
    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        pass
    @abstractmethod
    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass
    @abstractmethod
    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass

    def print_short_info(self) -> None:
        print(f"№{self.num}) {self.out()}\n"
              f"Role: {naming(self.role)}\n"
              f"Darkness= {self.dark}\n"
              f"Definitely now who is black: {', '.join( f'№{i.num} [{i.out()}]' for i in sorted([PLAYERS[i] for i in self.black], key=lambda p: p.num)) or 'No one'}")

    @abstractmethod
    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        pass



