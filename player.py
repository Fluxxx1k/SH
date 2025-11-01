from user_settings import MAX_PLAYER_NUM, MAX_NAME_LEN
from colors import (YELLOW_BACKGROUND_BRIGHT as GULAG,
                    RED_BACKGROUND_BRIGHT as DEAD,
                    RESET_BACKGROUND as END_BG,
                    )
from utils import get_color, coloring, naming, input_cards
from standard_names_SH import X
from standard_functions import show_only_to_one, yes_or_no, is_x_in_y, my_input
from colors import (BLUE_TEXT_BRIGHT as BLUE,
                    CYAN_TEXT_BRIGHT as CYAN,
                    YELLOW_TEXT_BRIGHT as YELLOW,
                    RESET_TEXT as END_T,
                    END, UP,
                    )


class Player:
    base_name = "Player"

    def __init__(self, num: int, name: str, role: str):
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
        if name == '' or not isinstance(name, str):
            self.name = Player.base_name + str(num)
        else:
            self.name = name
        self.tablet_name = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark = 0

    def __repr__(self):
        s = '[Info: '
        for name, value in self.__dict__.items():
            s += f"({name}: {repr(value)}) "
        s = s[:-1] + ']'
        return s
    def __hash__(self):
        return hash(self.name)

    # def __add__(self, s):
    #     self.suffix += s
    #     return self
    #
    # def __radd__(self, s):
    #     self.prefix += s
    #     return self
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

    def president(self, cards: str | list[str], cnc: "Player", *, black, red):
        cards = ''.join(sorted(cards)).upper()
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(cards.upper())
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
        while len(to_cnc) != 2 or not is_x_in_y(to_cnc, cards):
            to_cnc = input(f'{UP}' + phrase1).strip().upper()
        print(f'{UP * 3}' + "#" * len(cards))  # ⣿
        print()
        print(phrase1 + '#' * len(to_cnc))
        return words, to_cnc, yes_or_no("Veto? ") if black == 5 else False

    def chancellor(self, cards: str, prs: "Player", words, veto, *, black, red):
        show_only_to_one(f"Remember, your role is {naming(self.role)}, color is {self.colored_color}.", hide_len=60)
        card1 = coloring(cards)
        print(card1)
        phrase = f"You will say that here: "
        words_ch = input(phrase).strip().upper()
        while len(words_ch) != 2 or not set(words_ch).issubset({'X', "B", "R"}):
            words_ch = input(f'{UP}' + phrase).strip().upper()
        print(f'{UP}{phrase}{coloring(words_ch)}')
        phrase1 = f"You will place: "
        placed = my_input(phrase1, upper=True, possible=set(cards))
        print(f'{UP * 3}' + "#" * len(cards))  # ⣿
        print()
        if placed == "VETO":
            print(phrase1 + "Nothing (Veto)")
            return words_ch, "X"
        print(phrase1 + coloring(placed))
        return words_ch, placed

    def president_said_after_chancellor(self, *, cards: str, cnc: "Player", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        phrase = f"Cards {CYAN}president{END_T} ({self}) said after chancellor ({cnc}): "
        cpsa = input_cards(phrase, q={3, 0})
        print(UP + phrase + coloring(cpsa))
        return cpsa

    def check_cards(self):
        ...

    def table(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix

    def out(self):
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix

#    def check_color(self):
#        x = weighted_random(g, list(map(Player.dark, g)))
#        if self.bot_mind == X.RED:
#            return x.name, x.colored_color
#        if self.bot_mind = X.BLACK:
#
#    def check_cards(self,  card):
#        print(coloring("BBB"))
