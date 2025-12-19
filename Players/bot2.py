from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from Players.abstract_player import AbstractPlayer
import datetime
import random as rnd
from globs import CARDS

from HTML_logs import InfoLog
from globs import INFO_LOGS
from standard_names_SH import X
from user_settings import DATE_FORMAT, TIME_FORMAT, IS_PRINT_SMALL_INFO, IS_PRINT_FULL_INFO, BLACK_WIN_NUM, RED_WIN_NUM
from Players.bot import Bot


class Bot2(Bot):
    def _president_anarchist(self, cards, cnc: AbstractPlayer) -> tuple[str, list[str], bool]:
        if "B" in cards and "R" in cards:
            return "XXX", ["B", "R"], CARDS[X.BLACK] == BLACK_WIN_NUM - 1
        else:
            return "XXX", cards[1:], CARDS[X.BLACK] == BLACK_WIN_NUM - 1

    def _president_unknown(self, cards, cnc: AbstractPlayer) -> tuple[str, list[str], bool]:
        if IS_PRINT_FULL_INFO:
            print(f"Unknown president situation {cards= }")
        elif IS_PRINT_SMALL_INFO:
            print(f"Unknown president situation")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                 info_name=f"Unknown president situation",
                                 info1=f"№{self.num} [{self}] {self.bot_mind= } {cards= }",
                                 info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
        return self._president_anarchist(cards, cnc)

    def _president_hitler(self, cards, cnc: AbstractPlayer) -> tuple[str, list[str], bool]:
        if cards == ["R", "R", "R"]:
            return "RRR", ["R", "R"], CARDS[X.BLACK] == BLACK_WIN_NUM - 1
        if cards == ["B", "R", "R"]:
            return "BBR" if rnd.random() < 0.5 else "BRR", ["B", "R"], False
        if cards == ["B", "B", "R"]:
            if rnd.random() < 0.9 or CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
                return "BBB", ["B", "B"], False
            else:
                return "BBB", ["B", "R"], False
        if cards == ["B", "B", "B"]:
            return "BBB", ["B", "B"], False
        return self._president_unknown(cards, cnc)

    def _president_black(self, cards, cnc: AbstractPlayer) -> tuple[str, list[str], bool]:
        if cards == ["B", "R", "R"]:
            return "BRR" if rnd.random() < 0.5 else "BBR", ["B", "R"], False
        if cards == ["B", "B", "R"]:
            if rnd.random() < 0.96 or CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
                return "BBB", ["B", "B"], False
            else:
                return "BBR" if rnd.random() < 0.5 else "BRR", ["B", "R"], False
        if cards == ["B", "B", "B"]:
            return "BBB", ["B", "B"], False
        if cards == ["R", "R", "R"]:
            return "RRR", ["R", "R"], CARDS[X.BLACK] == BLACK_WIN_NUM - 1
        return self._president_unknown(cards, cnc)

    def _president_red(self, cards, cnc: AbstractPlayer) -> tuple[str, list[str], bool]:
        if cards == ["B", "R", "R"]:
            if CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
                return ''.join(cards), ["R", "R"], False
            else:
                if cnc in self.black:
                    return ''.join(cards), ["R", "R"], False
                return "BBB" if rnd.random() < self.risk else ''.join(cards), ["B", "R"], False
        if cards == ["B", "B", "R"]:
            return "BBB" if rnd.random() < self.risk else ''.join(cards), ["B", "R"], False
        if cards == ["R"] * 3:
            return "RRR", ["R"] * 2, False
        if cards == ["B"] * 3:
            return "BBB", ["B"] * 2, CARDS[X.BLACK] == BLACK_WIN_NUM - 1
        return self._president_unknown(cards, cnc)

    def _chancellor_anarchist(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        if CARDS[X.RED] <= CARDS[X.BLACK]:
            if "R" in cards:
                return "XX", "R"
            return "XX", "B"
        else:
            if "B" in cards:
                return "XX", "B"
            return "XX", "R"

    def _chancellor_unknown(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        if IS_PRINT_FULL_INFO:
            print(f"Unknown chancellor situation {cards= }")
        elif IS_PRINT_SMALL_INFO:
            print(f"Unknown chancellor situation")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown chancellor situation",
                                 info1=f"№{self.num} [{self}] {self.bot_mind= } {cards= }",
                                 info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
        return self._chancellor_anarchist(cards, prs, words, veto)

    def _chancellor_red(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        if "R" in cards:
            return ''.join(cards), "R"
        elif veto:
            return ''.join(cards), "X"
        else:
            return ''.join(cards), 'B'


    def _chancellor_hitler(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        if CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
            if "B" in cards:
                return ''.join(cards), "B"
            if veto:
                return "BB", 'X'
        if "B" in cards and prs in self.black and (words == "BBB" or words == "XXX"):
            return "BB", "B"
        if 'R' in cards:
            return ''.join(cards), "R"
        return ''.join(cards), "R"

    def _chancellor_black(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        if cards == ["B"] * 2:
            return "BB", "B"
        if cards == ["R"] * 2:
            if veto:
                return "BB", 'X'
            return "RR", "R"
        if CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
            return ''.join(cards), "B"
        if prs in self.black and (words == "BBB" or words == "XXX"):
            return "BB", "B"
        if CARDS[X.RED] == 3:
            if rnd.random() < 0.69:
                return ''.join(cards), "R"
            return "BB", "B"
        if rnd.random() < 0.75:
            return ''.join(cards), "R"
        return "BB", "B"

    def _president(self, cards, cnc, *args) -> tuple[str, list[str], bool]:
        cards = sorted(cards)
        if self.bot_mind == X.HITLER:
            return self._president_hitler(cards, cnc)
        if self.bot_mind == X.BLACK:
            return self._president_black(cards, cnc)
        if self.bot_mind == X.RED:
            return self._president_red(cards, cnc)
        if self.bot_mind == X.NRH:
            return self._president_anarchist(cards, cnc)
        else:
            return self._president_unknown(cards, cnc)
    def president(self, cards, cnc) -> tuple[str, list[str], bool]:
        temp: tuple[str, list[str], bool] = self._president(cards, cnc)
        return 'XXX', temp[1], temp[2]

    def chancellor(self, cards: str | list[str], prs: int, words: str, veto: bool) -> tuple[str, str]:
        cards = sorted(cards)
        if self.bot_mind == X.RED:
            return self._chancellor_red(cards, prs, words, veto)
        if self.bot_mind == X.HITLER:
            return self._chancellor_hitler(cards, prs, words, veto)
        if self.bot_mind == X.BLACK:
            return self._chancellor_black(cards, prs, words, veto)
        elif self.bot_mind == X.NRH:
            return self._chancellor_anarchist(cards, prs, words, veto)
        else:
            return self._chancellor_unknown(cards, prs, words, veto)

    def _vote_for_pair_hitler(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        if prs in self.black or cnc in self.black:
            return 1
        if CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1:
            return -1
        return 1

    def _vote_for_pair_red(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        if prs in self.black or cnc in self.black:
            return -1
        if (prs.contr > 0 or cnc.contr > 0) and rnd.random() < 0.87:
            return -1
        return 1

    def _vote_for_pair_black(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        if prs in self.black or cnc in self.black:
            return 1
        if CARDS[X.RED] == RED_WIN_NUM - 1 or CARDS[X.BLACK] == BLACK_WIN_NUM - 1 or rnd.random() < 0.03125:
            return -1
        return 1

    def _vote_for_pair_anarchist(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        return -1 if rnd.random() < 0.333 else rnd.random() < 0.5

    def _vote_for_pair_unknown(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        if IS_PRINT_FULL_INFO:
            print(f"Unknown vote situation {self.bot_mind= } {prs= } {cnc= }")
        elif IS_PRINT_SMALL_INFO:
            print(f"Unknown vote situation")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                 info_name=f"Unknown vote situation",
                                 info1=f"№{self.num} [{self}] {self.bot_mind= } {prs= } {cnc= }",
                                 info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
        return 0
    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        if self.bot_mind == X.HITLER:
            return self._vote_for_pair_hitler(prs, cnc)
        elif self.bot_mind == X.RED:
            return self._vote_for_pair_red(prs, cnc)
        elif self.bot_mind == X.BLACK:
            return self._vote_for_pair_black(prs, cnc)
        elif self.bot_mind == X.NRH:
            return self._vote_for_pair_anarchist(prs, cnc)
        else:
            return self._vote_for_pair_unknown(prs, cnc)
