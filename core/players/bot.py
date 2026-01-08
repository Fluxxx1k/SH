from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.players.player import Player
import datetime
import random as rnd
import time


import user_settings
from core.logs.HTML_logs import InfoLog
from core.players.abstract_player import AbstractPlayer
from legacy.globs import INFO_LOGS, PLAYERS, ROLES, CARDS
from core.standard_classes import Cards
from core.standard_names_SH import X
from user_settings import DATE_FORMAT, TIME_FORMAT, IS_PRINT_SMALL_INFO, IS_PRINT_FULL_INFO, DEBUG_MODE
from core.utils import get_color, weighted_random_for_indexes, preproc_votes


class Bot(AbstractPlayer):
    """
    First attempt of bot player.
    Use Bot2 instead.
    """
    base_name = X.BOT

    def __init__(self, num: int, name:str, role: str):
        super().__init__(num=num, role=role, name=name)
        self.bot_mind: X = get_color(self.role, out_type=X.BOT)
        if self.bot_mind == X.ANARCHIST:
            self.risk: float = rnd.random() * 0.5 + 0.5
        elif self.bot_mind == X.HITLER:
            self.risk: float = rnd.random() * 0.125 + 0.0625
        else:
            self.risk: float = rnd.random() * 0.7 + 0.25
        self.black: set[int] = set()
        if self.bot_mind == X.BLACK:
            from legacy import globs
            for i in range(globs.COUNT_PLAYERS):
                if ROLES[i] == X.BLACK or ROLES[i] == X.RIBBENTROP:
                    self.black.add(i)
            try:
                self.black.add(globs.HITLER)
            except Exception as e:
                if user_settings.IS_PRINT_FULL_INFO:
                    print(repr(e))
                INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                         info_name=f"Cannot add Hitler to black list: {repr(e)}",
                                         info1=f"{ globs.HITLER= } {self.bot_mind= }"))
        if self.bot_mind == X.HITLER:
            self.black.add(self.num)


    def president(self, cards, cnc) -> tuple[str, list[str], bool]:
        cards = sorted(cards)
        if self.bot_mind == X.HITLER:
            if cards == ["R", "R", "R"]:
                return "XXX", ["R", "R"], CARDS[X.BLACK] == 5
            if cards == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if cards == ["B", "B", "R"]:
                if rnd.random() < 0.9 or CARDS[X.RED] == 4 or CARDS[X.BLACK] == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if cards == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
            if user_settings.IS_PRINT_FULL_INFO:
                print(f"Unknown situation {cards= }")
            elif IS_PRINT_SMALL_INFO:
                print(f"Unknown situation")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                     info_name=f"Unknown situation",
                                     info1=f"{self.bot_mind= } {cards= }",
                                     info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
        if self.bot_mind == X.BLACK:
            if cards == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if cards == ["B", "B", "R"]:
                if rnd.random() < 0.96 or CARDS[X.RED] == 4 or CARDS[X.BLACK] == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if cards == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
            if cards == ["R", "R", "R"]:
                return "XXX", ["R", "R"], CARDS[X.BLACK] == 5
            if user_settings.IS_PRINT_FULL_INFO:
                print(f"Unknown situation {cards= }")
            elif IS_PRINT_SMALL_INFO:
                print(f"Unknown situation")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                     info_name=f"Unknown situation",
                                     info1=f"{self.bot_mind= } {cards= }",
                                     info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))

            return "XXX", cards[:2], CARDS[X.BLACK] == 5
        if self.bot_mind == X.RED:
            if cards == ["B", "R", "R"]:
                if CARDS[X.RED] == 4 or CARDS[X.BLACK] == 5:
                    return "XXX", ["R", "R"], False
                else:
                    if cnc in self.black:
                        return "XXX", ["R", "R"], False
                    return "XXX", ["B", "R"], False
            if cards == ["B", "B", "R"]:
                return "XXX", ["B", "R"], False
            if cards == ["R"] * 3:
                return "XXX", ["R"] * 2, False
            if cards == ["B"] * 3:
                return "XXX", ["B"] * 2, CARDS[X.BLACK] == 5
            if user_settings.IS_PRINT_FULL_INFO:
                print(f"Unknown situation {cards= }")
            elif IS_PRINT_SMALL_INFO:
                print(f"Unknown situation")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                     info_name=f"Unknown situation",
                                     info1=f"{self.bot_mind= } {cards=}",
                                     info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
            return "XXX", cards[1:], CARDS[X.BLACK] == 5
        if self.bot_mind == X.NRH:
            if "B" in cards and "R" in cards:
                return "XXX", ["B", "R"], CARDS[X.BLACK] == 5
            else:
                return "XXX", cards[1:], CARDS[X.BLACK] == 5
        else:
            if user_settings.IS_PRINT_FULL_INFO:
                print(f"Unknown bot mind {self.bot_mind= } {cards= }")
            elif IS_PRINT_SMALL_INFO:
                print(f"Unknown bot mind")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR,
                                     info_name=f"Unknown bot mind",
                                     info1=f"{self.bot_mind= }{cards= }",
                                     info2=f"{datetime.datetime.now().strftime(f'{DATE_FORMAT} {TIME_FORMAT}')}"))
            if "B" in cards and "R" in cards:
                return "XXX", ["B", "R"], CARDS[X.BLACK] == 5
            else:
                return "XXX", cards[1:], CARDS[X.BLACK] == 5

    def chancellor(self, cards:str|list[str], prs:int, words:str, veto:bool) -> tuple[str, str]:
        cards = sorted(cards)
        if self.bot_mind == X.RED:
            if "R" in cards:
                return "XX", "R"
            elif veto:
                return "XX", "X"
            else:
                return "XX", 'B'
        if self.bot_mind == X.HITLER:
            if CARDS[X.RED] == 4 or CARDS[X.BLACK] == 5:
                if "B" in cards:
                    return "XX", "B"
                if veto:
                    return "XX", 'X'
            if 'R' in cards:
                return "XX", "R"
            if "B" in cards and prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            else:
                return "XX", "R"
        if self.bot_mind == X.BLACK:
            if cards == ["B"] * 2:
                return "XX", "B"
            if cards == ["R"] * 2:
                if veto:
                    return "XX", 'X'
                return "XX", "R"
            if CARDS[X.RED] == 4 or CARDS[X.BLACK] == 5:
                return "XX", "B"
            if prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            if CARDS[X.RED] == 3:
                if rnd.random() < 0.69:
                    return "XX", "R"
                return "XX", "B"
            if rnd.random() < 0.75:
                return "XX", "R"
            return "XX", "B"
        else:
            if self.bot_mind != X.NRH:
                if IS_PRINT_SMALL_INFO:
                    print(f"Unknown role")
                INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind",
                                         info1=f"№{self.num} [{self}] {self.bot_mind= }"))
            if CARDS[X.RED] <= CARDS[X.BLACK]:
                if "R" in cards:
                    return "XX", "R"
                return "XX", "B"
            else:
                if "B" in cards:
                    return "XX", "B"
                return "XX", "R"

    def president_said_after_chancellor(self, *, cards: str, cnc: int | Player,
                                        ccg: str, cps: str,
                                        ccs: str, ccp: str) -> Cards:
        """
        Check cards after chancellor
        :param cards: Cards president got
        :param cnc: Number of chancellor
        :param ccg: Cards chancellor got
        :param cps: Cards president said
        :param ccs: Cards chancellor said
        :param ccp: Cards chancellor placed
        :return: Cards of president said after chancellor movement
        """
        if isinstance(cnc, AbstractPlayer):
            cnc = cnc.num
        match self.bot_mind:
            case X.RED:
                if "R" in ccg and ccp == "B":
                    self.black.add(cnc)
                return Cards(cards)
            case X.BLACK:
                if cnc in self.black:
                    if ccp == "B":
                        return Cards("BBB")
                    return Cards(cps)
                else:
                    if ccp == "R":
                        return Cards(cards)
                    return Cards(cps)
            case X.HITLER:
                if "R" in ccg and ccp == "B":
                    self.black.add(cnc)
                if 'R' == ccp:
                    return Cards(cards)
                return Cards(cps)
            case X.ANARCHIST:
                return Cards(cps)
            case _:
                INFO_LOGS.append(InfoLog(X.ERROR, info_name="Unknown bot mind",
                                         info1=f"№{self.num} [{self}] {self.bot_mind= }",
                                         info2=datetime.datetime.now().strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
                if IS_PRINT_FULL_INFO:
                    print(f"Unknown {self.bot_mind= }")
                elif IS_PRINT_SMALL_INFO:
                    print("Unknown bot mind")
                return Cards("XXX")




    def check_cards(self, cards, *args, **kwargs) -> Cards:
        match self.bot_mind:
            case X.RED:
                return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
            case X.BLACK:
                if cards == 'BBR':
                    from legacy.globs import COUNT_PLAYERS
                    if PLAYERS[self.num%COUNT_PLAYERS].color == X.RED:
                        return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
                    else:
                        return Cards("BBB")
                if cards == 'BRR':
                    if cards == 'BBR':
                        from legacy.globs import COUNT_PLAYERS
                        if PLAYERS[self.num % COUNT_PLAYERS].color == X.RED:
                            return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
                        else:
                            return Cards("BBB")
                return Cards(cards)
            case X.ANARCHIST:
                return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
            case X.HITLER:
                return Cards(cards) if rnd.random() < self.risk else Cards("BBB")

        if IS_PRINT_SMALL_INFO:
            print(f"Unknown bot_mind")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot_mind",
                                 info1=f"№{self.num} [{self}] {self.bot_mind= }",
                                 info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        return Cards("XXX")

    def check_player(self, votes: list[int] = None) -> tuple[int, str]:
        from legacy.globs import PLAYERS
        if votes is None:
            votes = {}
            if IS_PRINT_SMALL_INFO:
                print("Sorry, You forgot about \"votes\"... It isn't available here...")
            INFO_LOGS.append(InfoLog(info_type=X.WEAK_WARNING, info_name=f"You forgot about vote in Bot.check_player",
                                     info1=f"№{self.num} [{self}] {self.bot_mind= }",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        if self.bot_mind == X.BLACK:
            if rnd.random() < 0.25:
                from legacy import globs
                chosen = globs.HITLER
                PLAYERS[globs.HITLER].black.add(self.num)
                return chosen, X.RED
            if rnd.random() < 0.25:
                if self.black:
                    chosen = list(self.black)[rnd.randint(0, len(self.black) - 1)]
                    return chosen, X.RED
        try:
            from legacy.globs import COUNT_PLAYERS
            ppv = preproc_votes(votes)
            ppv[self.num] = 0
            chosen = weighted_random_for_indexes(ppv)
        except Exception as e:
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while checking another",
                                     info1=f"{votes= } {repr(e)}",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            chosen = rnd.randint(0, len(PLAYERS) - 1)
            while chosen == self.num:
                chosen = rnd.randint(0, len(PLAYERS) - 1)
        if self.color == X.BLACK:
            if PLAYERS[chosen].color == X.BLACK:
                PLAYERS[chosen].black.add(self.num)
                return chosen, X.RED
            elif self.bot_mind != X.HITLER and PLAYERS[chosen].color == X.RED and rnd.random() < self.risk:
                PLAYERS[chosen].black.add(self.num)
                return chosen, X.BLACK
        return chosen, PLAYERS[chosen].color

    def purge_another(self, purge_type: str = None, votes: dict[int, int] = None) -> int:
        if votes is None:
            votes = {}
            if IS_PRINT_SMALL_INFO:
                print("Sorry, coder forgot about \"votes\"... It isn't available here...")
            INFO_LOGS.append(InfoLog(info_type=X.WEAK_WARNING, info_name=f"You forgot about vote in Bot.purge_another",
                                     info1=f"№{self.num} [{self}] {self.bot_mind= }",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        try:
            from legacy import globs
            ppv = [1] * globs.COUNT_PLAYERS
            match self.bot_mind:
                case X.RED:
                    if self.black:
                        ppv = preproc_votes(dict.fromkeys(self.black, 100), (set(range(
                            globs.COUNT_PLAYERS)) - self.black) | {globs.GULAG, globs.KILLED}, times_smalling=float('inf'))
                        ppv[self.num] = 0
                        if sum(votes) == 0:
                            ppv = preproc_votes(votes)
                    else:
                        ppv = preproc_votes(votes)
                case X.BLACK:
                    ppv = preproc_votes(votes, self.black, times_smalling=float('inf'))
                    for i in self.black:
                        ppv[i] = 0
                case X.HITLER:
                    ppv = preproc_votes(votes, self.black, times_smalling=float('inf'))
                    for i in self.black:
                        ppv[i] = 0
                case X.ANARCHIST:
                    ppv = preproc_votes(votes)
                case _:
                    if IS_PRINT_SMALL_INFO:
                        print("Unknown bot mind")
                    INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self= } {self.bot_mind= }",
                                             info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
                    ppv = preproc_votes(votes)
            ppv[self.num] = 0
            if globs.GULAG is not None:
                ppv[globs.GULAG] = 0
            if globs.KILLED is not None:
                ppv[globs.KILLED] = 0
            if sum(ppv) == 0:
                ppv = [1] * globs.COUNT_PLAYERS
                ppv[self.num] = 0
                if globs.GULAG is not None:
                    ppv[globs.GULAG] = 0
                if globs.KILLED is not None:
                    ppv[globs.KILLED] = 0
            x = weighted_random_for_indexes(ppv)
            if DEBUG_MODE:
                print(f"{votes= }")
                print(f"{ppv= }")
            return x
        except Exception as err:
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while purging another",
                                     info1=f"{self.bot_mind= } {repr(err)}",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))

        if IS_PRINT_SMALL_INFO:
            print("Unknown bot mind")
        if user_settings.IS_PRINT_FULL_INFO:
            print(f"{self.bot_mind= }")
        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self.bot_mind= }",
                                 info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        return weighted_random_for_indexes([0])
    def choose_chancellor(self, cannot_be: set[int] = frozenset(), votes: dict[int, int] = None, gov_type=X.CHANCELLOR) -> int:
        if user_settings.DEBUG_MODE:
            print(f"{cannot_be= }")
        if votes is None:
            votes = {}
            if IS_PRINT_SMALL_INFO:
                print("Sorry, You forgot about \"votes\"... It isn't available here...")
            INFO_LOGS.append(InfoLog(info_type=X.WEAK_WARNING, info_name=f"You forgot about vote in Bot.choose_chancellor",
                                     info1=f"№{self.num} [{self}] {self.bot_mind= }",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        if self.bot_mind == X.BLACK:
            ppv = preproc_votes(votes, self.black, times_smalling=0.5)
            ppv[self.num] = 0
            for i in cannot_be:
                if user_settings.DEBUG_MODE:
                    print(i)
                if i is not None:
                    try:
                        ppv[i] = 0
                    except Exception as e:
                        if user_settings.IS_PRINT_FULL_INFO:
                            print(f"Can't set {i= } to 0: {e}")
                        INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while setting ppv[i]=0",
                                                 info1=f"{self= } {i= } {repr(e)}",
                                                 info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            from legacy import globs
            try:
                if gov_type == X.CHANCELLOR:
                    if globs.HITLER is not None and globs.HITLER not in cannot_be:

                            ppv[globs.HITLER] <<= 1
                elif gov_type == X.PRESIDENT:
                    ppv[globs.HITLER] >>= 1
                else:
                    print(f"Unknown government type {gov_type= }")
                    INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown government type", info1=f"{self= } {gov_type= }",
                                             info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            except Exception as e:
                if user_settings.IS_PRINT_FULL_INFO:
                    print(f"Can't find { globs.HITLER= }: {e}")
                INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while choosing chancellor",
                                         info1=f"{self= } {self.bot_mind= } { globs.HITLER= } {repr(e)}",
                                         info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        elif self.bot_mind == X.RED:
            ppv = preproc_votes(votes, self.black, times_smalling=float('inf'))
        elif self.bot_mind == X.HITLER:
            ppv = preproc_votes(votes, self.black, times_smalling=0.25)
        elif self.bot_mind == X.ANARCHIST:
            ppv = preproc_votes(votes)
        else:
            if IS_PRINT_SMALL_INFO:
                print("Unknown bot mind")
            INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self= } {self.bot_mind= }",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            ppv = preproc_votes(votes)
        ppv[self.num] = 0
        if sum(ppv) == 0:
            if IS_PRINT_SMALL_INFO:
                print("votes empty, so choose random player")
            INFO_LOGS.append(InfoLog(info_type=X.INFO, info_name=f"votes empty, so choose random player", info1=f"{self= } {votes= } {cannot_be= }",
                                     info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))

            from legacy import globs
            ppv = [1] * globs.COUNT_PLAYERS
        ppv[self.num] = 0
        for i in cannot_be:
            if user_settings.DEBUG_MODE:
                print(i)
            if i is not None:
                try:
                    ppv[i] = 0
                except Exception as e:
                    if user_settings.IS_PRINT_FULL_INFO:
                        print(f"Can't set {i= } to 0: {e}")
                    INFO_LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while setting ppv[i]=0",
                                             info1=f"{self= } {i= } {repr(e)}",
                                             info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        x = weighted_random_for_indexes(ppv)
        if user_settings.DEBUG_MODE:
            print(f"{ppv= }")
        return x
    place_another = choose_chancellor

    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> bool:
        if IS_PRINT_SMALL_INFO:
            print("Error, using unrealised method vote_for_pair in Bot")
        return rnd.random() < 0.5
