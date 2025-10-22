import random as rnd
from colors import PURPLE_TEXT_BRIGHT as PURPLE, END
from player import Player
from standard_names_SH import X
from user_color_settings import CRITICAL
from utils import get_color


class Bot(Player):
    base_name = X.BOT

    def __init__(self, num: int, name:str, role: str, *, hitler: int = None):
        super().__init__(num=num, role=role, name=name)
        self.bot_mind = get_color(self.role, out_type=X.BOT)
        if self.bot_mind == X.BLACK:
            if hitler is None:
                print(f"{CRITICAL}Bot won't know who is hitler{END}")
        self.hitler = hitler
        self.risk = rnd.random()
        self.black = []

    def president(self, cards, cnc, *, black, red) -> tuple[str, list[str], bool]:
        cards = sorted(cards)
        if self.bot_mind == X.HTLR:
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
        if self.bot_mind == X.HTLR:
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
                                        ccp: str) -> str:
        return 'XXX'

    def check_cards(self) -> str:
        return "XXX"

    def check_player(self, votes: dict[int, int] = None) -> tuple[int, str]:
        chosen:int = None
        if votes is not None:
            print("Sorry, \"votes\" isn't available")
        if self.bot_mind == X.BLACK:
            if rnd.random() < 0.25:
                chosen = self.hitler
            if rnd.random() < 0.25:
                if self.black:
                    chosen = self.black[rnd.randint(0, len(self.black) - 1)]
            if chosen is not None:
                return chosen, X.RED
        chosen = rnd.randint(0, len(self.black) - 1)
        if self.bot_mind == X.BLACK:
            if chosen in self.black:
                return chosen, X.RED
        from globs import PLAYERS
        return chosen, PLAYERS[chosen].color
