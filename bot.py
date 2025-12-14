import random as rnd
import time

import user_settings
from HTML_logs import InfoLog
from colors import END
from globs import LOGS
from player import Player
from standard_classes import Cards
from standard_names_SH import X
from user_color_settings import CRITICAL
from user_settings import DATE_FORMAT, TIME_FORMAT, IS_PRINT_SMALL_INFO
from utils import get_color, weighted_random_for_indexes, preproc_votes


class Bot(Player):
    base_name = X.BOT

    def __init__(self, num: int, name:str, role: str, *, hitler: int = None):
        super().__init__(num=num, role=role, name=name)
        self.bot_mind = get_color(self.role, out_type=X.BOT)
        if self.bot_mind == X.BLACK:
            if hitler is None:
                if user_settings.IS_PRINT_FULL_INFO:
                    print(f"{CRITICAL}Bot won't know who is hitler{END}")
        self.risk = rnd.random()
        self.black: list[int] = []


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
                print("Unknown role {self.bot_mind= }")
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

    def check_cards(self, *args, **kwargs) -> Cards:
        return Cards("XXX")

    def check_player(self, votes: list[int] = None) -> tuple[int, str]:
        from globs import PLAYERS
        chosen:int = None
        if votes is None:
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        if self.bot_mind == X.BLACK:
            if rnd.random() < 0.25:
                import globs
                chosen = globs.HITLER

            if rnd.random() < 0.25:
                if self.black:
                    chosen = self.black[rnd.randint(0, len(self.black) - 1)]
            if chosen is not None:
                return chosen, X.RED
        try:

            from globs import COUNT_PLAYERS
            x = [0]*COUNT_PLAYERS
            for i in votes:
                x[i] = votes[i]
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
                return chosen, X.RED
        return chosen, PLAYERS[chosen].color

    def purge_another(self, purge_type: str = None, votes: dict[int, int] = None) -> int:
        if votes is None:
            votes = {}
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        try:
            match self.bot_mind:
                case X.RED:
                    if self.black:
                        return list(self.black)[rnd.randint(0, len(self.black) - 1)]
                    return weighted_random_for_indexes(preproc_votes(votes))
                case X.BLACK, X.HITLER:
                    return weighted_random_for_indexes(preproc_votes(votes, self.black, times_smalling=float('inf')))
                case X.ANARCHIST:
                    return weighted_random_for_indexes(preproc_votes(votes))
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
        from globs import COUNT_PLAYERS
        x = rnd.randint(0, COUNT_PLAYERS - 1)
        while x == self.num:
            x = rnd.randint(0, COUNT_PLAYERS - 1)
        return x
    def place_another(self, votes: dict[int, int] = None) -> int:
        if votes is None:
            votes = {}
            print("Sorry, You forgot about \"votes\"... It isn't available here...")
        x = weighted_random_for_indexes(preproc_votes(votes))
        while x == self.num:
            x = weighted_random_for_indexes(preproc_votes(votes))
        return x
    def choose_chancellor(self, cannot_be: set[int] = set(), votes: dict[int, int] = {}) -> int:
        ppv = preproc_votes(votes)
        x = weighted_random_for_indexes(ppv)
        while x == self.num or x in cannot_be:
            x = weighted_random_for_indexes(ppv)
        return x


