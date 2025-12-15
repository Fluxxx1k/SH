from typing import Iterable

from globs import PLAYERS, ROLES
from user_color_settings import (INPUT_COLOR,
                                 BLACK_PLAYER_COLOR as BLACK,
                                 RED_PLAYER_COLOR as RED,
                                 PURPLE_PLAYER_COLOR as PURPLE, WARNING)
from user_settings import MAX_PLAYER_NUM, MAX_NAME_LEN, IS_PRINT_SMALL_INFO
from colors import (YELLOW_BACKGROUND_BRIGHT as GULAG,
                    RED_BACKGROUND_BRIGHT as DEAD,
                    RESET_BACKGROUND as END_BG,
                    )
from utils import get_color, coloring, naming, input_cards, preproc_votes, weighted_random_for_indexes
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
            self.name: str = Player.base_name + str(num)
        else:
            self.name: str = name
        self.tablet_name: str = f"{self.name: <{MAX_NAME_LEN}}"
        self.dark: float = 0
        self.black: set[int] = set()

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

    def check_cards(self, cards: str) -> str:
        show_only_to_one(coloring(cards))
        return input_cards(f"Cards {CYAN}president{END} said after checking: ", q=3)

    def table(self) -> str:
        return self.gov_pref + self.purge_pref + self.prefix + self.tablet_name + self.gov_suff + self.purge_suff + self.suffix

    def out(self) -> str:
        return self.gov_pref + self.purge_pref + self.prefix + self.name + self.gov_suff + self.purge_suff + self.suffix

    def check_player(self) -> tuple[int, str]:
        while True:
            try:
                pc = int(input(f"{CYAN}President{END} will check number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                from globs import COUNT_PLAYERS
                if pc >= COUNT_PLAYERS or pc < 0:
                    raise ValueError(f"Wrong number: {pc + 1}")
                if pc == self.num:
                    raise ValueError(f"Can't check yourself")
            except Exception as error:
                print(f"{RED}{error}{END}")
            else:
                if yes_or_no(
                        f"Are you sure that number {INPUT_COLOR}{pc + 1}{END} is right (it's [{INPUT_COLOR}{PLAYERS[pc]}{END}]): "):
                    break
        show_only_to_one(f"Color is {get_color(ROLES[pc])}")
        print(f"Input {BLACK}{X.BLK}{END} or {RED}{X.RED}{END} or {PURPLE}{X.NRH}{END}")
        cpc = input(f"Color of {PLAYERS[pc]} {CYAN}President{END} said: {INPUT_COLOR}").upper()
        print(END, end='')  # card_chancellor_placed
        while cpc not in {X.BLACK, X.RED, X.NRH}:
            print(f"{RED}WRONG    INPUT{END}")
            cpc = input(f"Color of {PURPLE}{PLAYERS[pc]}{END_T} {CYAN}President{END_T} said: {INPUT_COLOR}").upper()
            print(END, end='')
        return pc, cpc

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        match purge_type:
            case X.GULAG:
                while True:
                    try:
                        gulag = int(
                            input(f"{CYAN}President{END} will place in gulag number (not index): {INPUT_COLOR}")) - 1
                        print(END, end='')
                        from globs import COUNT_PLAYERS
                        if gulag < 1 or gulag >= COUNT_PLAYERS:
                            raise ValueError(f"Wrong number: {gulag + 1}")
                        if gulag == self.num:
                            raise ValueError(f"Can't purge yourself")
                    except Exception as error:
                        print(f"{RED}{error}{END}")
                    else:
                        if yes_or_no(
                                f"Are you sure that if number {INPUT_COLOR}{gulag + 1}{END} is right (it's [{INPUT_COLOR}{PLAYERS[gulag]}{END}]): "):
                            break
                return gulag
            case X.SHOUT:
                while True:
                    try:
                        killed = int(input(f"{CYAN}President{END} will kill number (not index): {INPUT_COLOR}")) - 1
                        print(END, end='')
                        from globs import COUNT_PLAYERS
                        if killed < 0 or killed >= COUNT_PLAYERS:
                            raise ValueError(f"Wrong number: {killed + 1}")
                        elif killed == self.num:
                            raise ValueError("No suicide!!")
                    except Exception as error:
                        print(f"{RED}{error}{END}")
                    else:
                        if yes_or_no(
                                f"Are you sure that number {INPUT_COLOR}{killed + 1}{END} is right (it's [{INPUT_COLOR}{PLAYERS[killed]}{END}]): "):
                            break
                return killed
            case _:
                print(f"{WARNING}Wrong purge type{END}")
                return self.purge_another(purge_type, votes)

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        while True:
            try:
                placed = int(
                    input(f"{CYAN}President{END} will place number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                from globs import COUNT_PLAYERS
                if placed < 0 or placed >= COUNT_PLAYERS:
                    raise ValueError(f"Wrong number: {placed + 1}")
                if placed in cannot_be:
                    raise ValueError(f"Can't place number {placed + 1}")
                if placed == self.num:
                    raise ValueError(f"Can't place yourself")
            except Exception as error:
                print(f"{RED}{error}{END}")
            else:
                if yes_or_no(
                        f"Are you sure that number {INPUT_COLOR}{placed + 1}{END} is right (it's [{INPUT_COLOR}{PLAYERS[placed]}{END}]): "):
                    break
        return placed

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        print(f"{CYAN}President{END} [{PURPLE}{PLAYERS[self.num]}{END}] will choose  {YELLOW}chancellor{END}")
        while True:
            try:
                chancellor = int(
                    input(f"{CYAN}President{END} will choose number (not index): {INPUT_COLOR}")) - 1
                print(END, end='')
                from globs import COUNT_PLAYERS
                if chancellor < 0 or chancellor >= COUNT_PLAYERS:
                    raise ValueError(f"Wrong number: {chancellor + 1}")
                if chancellor in cannot_be:
                    raise ValueError(f"Can't choose number {chancellor + 1}")
                if chancellor == self.num:
                    raise ValueError(f"Can't choose yourself")
            except Exception as error:
                print(f"{RED}{error}{END}")
            else:
                if yes_or_no(
                        f"Are you sure that number {INPUT_COLOR}{chancellor + 1}{END} is right (it's [{INPUT_COLOR}{PLAYERS[chancellor]}{END}]): "):
                    break
        return chancellor

