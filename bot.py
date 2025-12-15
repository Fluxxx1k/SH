from __future__ import annotations

import random as rnd
import time


import user_settings
from HTML_logs import InfoLog
from globs import LOGS, PLAYERS, ROLES
from player import Player
from standard_classes import Cards
from standard_names_SH import X
from user_settings import DATE_FORMAT, TIME_FORMAT, IS_PRINT_SMALL_INFO
from utils import get_color, weighted_random_for_indexes, preproc_votes


class Bot(Player):
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
            import globs
            for i in range(globs.COUNT_PLAYERS):
                if ROLES[i] == X.BLACK or ROLES[i] == X.RIBBENTROP:
                    self.black.add(i)
            try:
                self.black.add(globs.HITLER)
            except Exception as e:
                if user_settings.IS_PRINT_FULL_INFO:
                    print(repr(e))
                LOGS.append(InfoLog(info_type=X.ERROR,info_name=f"Cannot add Hitler to black list: {repr(e)}", info1=f"{globs.HITLER= } {self.bot_mind= }"))
        if self.bot_mind == X.HITLER:
            self.black.add(self.num)


    def president(self, cards, cnc, *, black, red) -> tuple[str, list[str], bool]:
        cards = sorted(cards)
        if self.bot_mind == X.HITLER:
            if cards == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            if cards == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if cards == ["B", "B", "R"]:
                if rnd.random() < 0.9 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if cards == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
        if self.bot_mind == X.BLACK:
            if cards == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if cards == ["B", "B", "R"]:
                if rnd.random() < 0.96 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if cards == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
            if cards == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            print(f"Unknown situation {cards= }")
            return "XXX", cards[:2], black == 5
        if self.bot_mind == X.RED:
            if cards == ["B", "R", "R"]:
                if red == 4 or black == 5:
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
                return "XXX", ["B"] * 2, black == 5
            print("Unknown situation {card= }")
            return "XXX", cards[1:], black == 5
        if self.bot_mind == X.NRH:
            if "B" in cards and "R" in cards:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", cards[1:], black == 5
        else:
            print(f"Unknown {self.bot_mind= }")
            if "B" in cards and "R" in cards:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", cards[1:], black == 5

    def chancellor(self, cards:str|list[str], prs:int, words:str, veto:bool, *, black:int, red:int) -> tuple[str, str]:
        cards = sorted(cards)
        if self.bot_mind == X.RED:
            if "R" in cards:
                return "XX", "R"
            elif veto:
                return "XX", "X"
            else:
                return "XX", 'B'
        if self.bot_mind == X.HITLER:
            if red == 4 or black == 5:
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
            if cards == ["R"]:
                if veto:
                    return "XX", 'X'
                return "XX", "R"
            if red == 4 or black == 5:
                return "XX", "B"
            if prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            if red == 3:
                if rnd.random() < 0.69:
                    return "XX", "R"
                return "XX", "B"
            if rnd.random() < 0.96:
                return "XX", "R"
            return "XX", "B"
        else:
            if self.bot_mind != X.NRH:
                if IS_PRINT_SMALL_INFO:
                    print(f"Unknown role")
                LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind",
                                    info1=f"№{self.num} [{self}] {self.bot_mind= }"))
            if red <= black:
                if "R" in cards:
                    return "XX", "R"
                return "XX", "B"
            else:
                if "B" in cards:
                    return "XX", "B"
                return "XX", "R"

    def president_said_after_chancellor(self, *, cards: str, cnc: "Player int", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> Cards:
        return Cards('XXX')

    def check_cards(self, cards, *args, **kwargs) -> Cards:
        match self.bot_mind:
            case X.RED:
                return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
            case X.BLACK:
                if cards == 'BBR':
                    from globs import COUNT_PLAYERS
                    if PLAYERS[self.num%COUNT_PLAYERS].color == X.RED:
                        return Cards(cards) if rnd.random() < self.risk else Cards("BBB")
                    else:
                        return Cards("BBB")
                if cards == 'BRR':
                    if cards == 'BBR':
                        from globs import COUNT_PLAYERS
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
        LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot_mind",
                            info1=f"№{self.num} [{self}] {self.bot_mind= }",
                            info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        return Cards("XXX")

    def check_player(self, votes: list[int] = None) -> tuple[int, str]:
        from globs import PLAYERS
        if votes is None:
            votes = {}
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        if self.bot_mind == X.BLACK:
            if rnd.random() < 0.25:
                import globs
                chosen = globs.HITLER
                return chosen, X.RED
            if rnd.random() < 0.25:
                if self.black:
                    chosen = list(self.black)[rnd.randint(0, len(self.black) - 1)]
                    return chosen, X.RED
        try:
            from globs import COUNT_PLAYERS
            if votes:
                x = [0]*COUNT_PLAYERS
                for i in votes:
                    x[i] = votes[i]
            else:
                x=[1]*COUNT_PLAYERS
            chosen = weighted_random_for_indexes(x)
        except Exception as e:
            LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while checking another",
                                info1=f"{votes= } {repr(e)}",
                                info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            chosen = rnd.randint(0, len(PLAYERS) - 1)
            while chosen == self.num:
                chosen = rnd.randint(0, len(PLAYERS) - 1)
        if self.color == X.BLACK:
            if PLAYERS[chosen].color == X.BLACK:
                PLAYERS[chosen].black.add(self.num)
                return chosen, X.RED
            elif PLAYERS[chosen].color == X.RED and rnd.random() < 0.25:
                PLAYERS[chosen].black.add(self.num)
                return chosen, X.BLACK
        return chosen, PLAYERS[chosen].color

    def purge_another(self, purge_type: str = None, votes: dict[int, int] = None) -> int:
        if votes is None:
            votes = {}
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        try:
            import globs
            ppv = [1] * globs.COUNT_PLAYERS
            match self.bot_mind:
                case X.RED:
                    if self.black:
                        return list(self.black)[rnd.randint(0, len(self.black) - 1)]
                    return weighted_random_for_indexes(preproc_votes(votes))
                case X.BLACK:
                    ppv = preproc_votes(votes, self.black, times_smalling=float('inf'))
                case X.HITLER:
                    ppv = preproc_votes(votes, self.black, times_smalling=float('inf'))
                case X.ANARCHIST:
                    ppv = preproc_votes(votes)
                case _:
                    if IS_PRINT_SMALL_INFO:
                        print("Unknown bot mind")
                    LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self= } {self.bot_mind= }",
                                        info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
                    ppv = preproc_votes(votes)
            ppv[self.num] = 0
            if sum(ppv) == 0:
                ppv = [1] * globs.COUNT_PLAYERS
                ppv[self.num] = 0
            x = weighted_random_for_indexes(ppv)
            return x
        except Exception as err:
            LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while purging another",
                                info1=f"{self.bot_mind= } {repr(err)}",
                                info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))

        if IS_PRINT_SMALL_INFO:
            print("Unknown bot mind")
        if user_settings.IS_PRINT_FULL_INFO:
            print(f"{self.bot_mind= }")
        LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self.bot_mind= }",
                            info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
        return weighted_random_for_indexes([0])
    def choose_chancellor(self, cannot_be: set[int] = frozenset(), votes: dict[int, int] = None, gov_type=X.CHANCELLOR) -> int:
        if votes is None:
            votes = {}
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        if self.bot_mind == X.BLACK:
            ppv = preproc_votes(votes, self.black, times_smalling=0.5)
            import globs
            try:
                if gov_type == X.CHANCELLOR:
                    ppv[globs.HITLER] <<= 1
                elif gov_type == X.PRESIDENT:
                    ppv[globs.HITLER] >>= 1
                else:
                    print(f"Unknown government type {gov_type= }")
                    LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown government type", info1=f"{self= } {gov_type= }",
                                        info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            except Exception as e:
                if user_settings.IS_PRINT_FULL_INFO:
                    print(f"Can't find {globs.HITLER= }: {e}")
                LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Error while choosing chancellor",
                                    info1=f"{self= } {self.bot_mind= } {globs.HITLER= } {repr(e)}",
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
            LOGS.append(InfoLog(info_type=X.ERROR, info_name=f"Unknown bot mind", info1=f"{self= } {self.bot_mind= }",
                                info2=time.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")))
            ppv = preproc_votes(votes)
        ppv[self.num] = 0
        if sum(ppv) == 0:
            import globs
            ppv = [1] * globs.COUNT_PLAYERS
            ppv[self.num] = 0
        x = weighted_random_for_indexes(ppv)
        return x
    place_another = choose_chancellor

