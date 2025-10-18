import random as rnd
from colors import PURPLE_TEXT_BRIGHT as PURPLE, END
from player import Player
from standard_names_SH import X
from utils import get_color


class Bot(Player):
    base_name = X.BOT

    def __init__(self, num: int, role: str,
                 name=X.BOT, *, hitler: int):
        super().__init__(num=num, role=role, name=name)
        self.bot_mind = get_color(self.role, out_type=X.BOT)
        if self.bot_mind == X.BLACK:
            self.hitler = hitler
        self.risk = rnd.random()
        self.black = []
        # if self.bot_mind == X.BLACK:
        #     for player_num in range(c):
        #         if g[player_num].color == X.BLACK:
        #             self.black.append(player_num)

    def __repr__(self):
        s = super().__repr__()
        s += " "
        s += f"[BOT INFO: {self.bot_mind= }, {self.dark= }, {self.risk= }]"
        return s

    def __hash__(self):
        return hash(self.name)

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
            print("Unknown situation {card= }")
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

    def chancellor(self, cards, prs, words, veto, *, black, red) -> tuple[str, str]:
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

    def president_said_after_chancellor(self, *, cards: str, cnc: "Player", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        return 'XXX'

    def check_cards(self):
        return "XXX"

    def check_player(self, g, votes: dict["Player": int] = None):
        if self.bot_mind == X.BLACK:
            if rnd.random() < 0.25:
                return self.hitler, X.RED
            if rnd.random() < 0.25:
                if self.black:
                    return self.black[rnd.randint(0, len(self.black) - 1)], X.RED
        print(votes)
        return rnd.randint(0, len(self.black) - 1)
