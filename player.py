from user_settings import MAX_PLAYER_NUM, MAX_NAME_LEN
from colors import (YELLOW_BACKGROUND_BRIGHT as GULAG,
                    RED_BACKGROUND_BRIGHT as DEAD,
                    RESET_BACKGROUND as END_BG,
                    )
import random as rnd
from utils import get_color, coloring, naming
from standard_names_SH import X
from standard_functions import show_only_to_one, yes_or_no, is_x_in_y
from colors import (PURPLE_TEXT_BRIGHT as PURPLE,
                    BLUE_TEXT_BRIGHT as BLUE,
                    CYAN_TEXT_BRIGHT as CYAN,
                    YELLOW_TEXT_BRIGHT as YELLOW,
                    RESET_TEXT as END_T,
                    END, UP,
                    )

class Player:
    base_name = "Player"

    def __init__(self, num, name="RANDOM", role=f"{PURPLE}ANARCHIST{END}"):
        self.gov_pref = ''
        self.gov_suff = ''
        self.purge_pref = ''
        self.purge_suff = ''
        self.num = num
        self.role = role
        self.color = get_color(self.role, out_type=X.BOT)
        if self.color == X.HITLER:
            self.color = X.BLACK
        self.colored_color = get_color(self.role)

        self.prefix = ''
        self.suffix = ''
        if name != "RANDOM":
            self.name = ' '.join(name.split())
        else:
            self.name = Player.base_name + str(num)
        self.tablet_name = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark = 0

    def __repr__(self):
        s = f"{self.name= } ({self.tablet_name= }): {self.role= } (mind_type: {self.color} {self.colored_color= }), {self.dark= }"
        # {len(self.name) == MAX_NAME_LEN = }
        return s

    # def __add__(self, s):
    #     self.suffix += s
    #     return self
    #
    # def __radd__(self, s):
    #     self.prefix += s
    #     return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
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

    def __format__(self, args):
        return str(self).format(*args)

    def degov(self):
        self.gov_suff = ''
        self.gov_pref = ''

    # def president(self, card, cnc):
    #def get_color(self):
    #    return self.colored_color

    def free(self):
        x = self.purge_pref == GULAG
        if x:
            print(f"{self.name} freed")
            self.purge_pref = self.purge_suff = ''
        else:
            print(f"{self.name} wasn't in gulag!!")
        return MAX_PLAYER_NUM

    def chosen_gov(self, gov_type):
        if gov_type == X.PRESIDENT:
            self.gov_pref = CYAN
        elif gov_type == X.CHANCELLOR:
            self.gov_pref = YELLOW
        else:
            self.gov_pref = BLUE
            print(f"Unknown government type: {gov_type}")
        self.gov_suff = END_T

    def purge(self, purge_type):
        self.degov()
        if purge_type == X.GULAG:
            self.purge_pref = GULAG
        elif purge_type == X.KILLED:
            self.purge_pref = DEAD
        else:
            self.purge_pref = BLUE
        self.purge_suff = END_BG

    def president(self, card: str | list[str], cnc: "Player", *, black, red):
        card = ''.join(sorted(card)).upper()
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(card.upper())
        print(card1)
        phrase = f"{CYAN}You{END_T} will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 3 or not set(words).issubset({'X', "B", "R"}):
            words = input(f'{UP}' + phrase).strip().upper()
        print(f'{UP}{phrase}{coloring(words)}')
        phrase1 = f"{CYAN}You{END_T} will give to {YELLOW}chancellor{END_T} ({cnc}): "
        to_cnc = input(phrase1).strip().upper()
        if to_cnc == "RB":
            to_cnc = "BR"
        while len(to_cnc) != 2 or not is_x_in_y(to_cnc, card):
            to_cnc = input(f'{UP}' + phrase1).strip().upper()
        print(f'{UP * 3}' + "#" * len(card)) # ⣿
        print()
        print(phrase1 + '#' * len(to_cnc))
        return words, to_cnc, yes_or_no("Veto? ") if black == 5 else False

    def chancellor(self, card:str, prs:"Player", words, veto, *, black, red):
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(card)
        print(card1)
        phrase = f"You will say that here: "
        words = input(phrase).strip().upper()
        while len(words) != 2 or not set(words).issubset({'X', "B", "R"}):
            words = input(f'{UP}' + phrase).strip().upper()
        print(f'{UP}{phrase}{coloring(words)}')
        phrase1 = f"You will place: "
        placed = input(phrase1).strip().upper()
        while len(placed) != 1 or placed not in card:
            if placed == "VETO" and veto:
                break
            placed = input(f'{UP}' + phrase1).strip().upper()

        print(f'{UP * 3}' + "#" * len(card)) # ⣿
        print()
        if placed == "VETO":
            print(phrase1 + "Nothing (Veto)")
            return words, "X"
        print(phrase1 + coloring(placed))
        return words, placed

    def table(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix

    def out(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix



class Bot(Player):
    base_name = X.BOT

    def __init__(self, num="ERR", role=f"{PURPLE}ANARCHIST{END}",
                 name="RANDOM",
                 ):
        super().__init__(num, role, name)
        self.bot_mind = get_color(self.role, out_type=X.BOT)
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

    def president(self, card, cnc, *, black, red) -> tuple[str, list[str], bool]:
        card = sorted(card)
        if self.bot_mind == X.HTLR:
            if card == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            if card == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                if rnd.random() < 0.9 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
        if self.bot_mind == X.BLACK:
            if card == ["B", "R", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                if rnd.random() < 0.96 or red == 4 or black == 5:
                    return "XXX", ["B", "B"], False
                else:
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "B"]:
                return "XXX", ["B", "B"], False
            if card == ["R", "R", "R"]:
                return "XXX", ["R", "R"], black == 5
            print("Unknown situation {card= }")
            return "XXX", card[:2], black == 5
        if self.bot_mind == X.RED:
            if card == ["B", "R", "R"]:
                if red == 4 or black == 5:
                    return "XXX", ["R", "R"], False
                else:
                    if cnc in self.black:
                        return "XXX", ["R", "R"], False
                    return "XXX", ["B", "R"], False
            if card == ["B", "B", "R"]:
                return "XXX", ["B", "R"], False
            if card == ["R"] * 3:
                return "XXX", ["R"] * 2, False
            if card == ["B"] * 3:
                return "XXX", ["B"] * 2, black == 5
            print("Unknown situation {card= }")
            return "XXX", card[1:], black == 5
        if self.bot_mind == X.NRH:
            if "B" in card and "R" in card:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", card[1:], black == 5
        else:
            print(f"Unknown {self.bot_mind= }")
            if "B" in card and "R" in card:
                return "XXX", ["B", "R"], black == 5
            else:
                return "XXX", card[1:], black == 5

    def chancellor(self, card, prs, words, veto, *, black, red) -> tuple[str, str]:
        card = sorted(card)
        if self.bot_mind == X.RED:
            if "R" in card:
                return "XX", "R"
            elif veto:
                return "XX", "X"
            else:
                return "XX", 'B'
        if self.bot_mind == X.HTLR:
            if red == 4 or black == 5:
                if "B" in card:
                    return "XX", "B"
                if veto:
                    return "XX", 'X'
                return "XX", "R"
            if "B" in card and prs in self.black and (words == "BBB" or words == "XXX"):
                return "XX", "B"
            else:
                return "XX", "R"
        if self.bot_mind == X.BLACK:
            if card == ["B"] * 2:
                return "XX", "B"
            if card == ["R"]:
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
                if "R" in card:
                    return "XX", "R"
                return "XX", "B"
            else:
                if "B" in card:
                    return "XX", "B"
                return "XX", "R"


#    def check_color(self):
#        x = weighted_random(g, list(map(Player.dark, g)))
#        if self.bot_mind == X.RED:
#            return x.name, x.colored_color
#        if self.bot_mind = X.BLACK:
#
#    def check_cards(self,  card):
#        print(coloring("BBB"))