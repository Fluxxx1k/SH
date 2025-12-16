from __future__ import annotations
from typing import Iterable

from Players.abstract_player import AbstractPlayer
from colors import (CYAN_TEXT_BRIGHT as CYAN,
                    YELLOW_TEXT_BRIGHT as YELLOW,
                    RESET_TEXT as END_T,
                    END, UP,
                    )
from globs import PLAYERS, ROLES, CARDS
from standard_functions import show_only_to_one, yes_or_no, is_x_in_y, my_input
from standard_names_SH import X
from user_color_settings import (INPUT_COLOR,
                                 BLACK_PLAYER_COLOR as BLACK,
                                 RED_PLAYER_COLOR as RED,
                                 PURPLE_PLAYER_COLOR as PURPLE, WARNING)
from utils import get_color, coloring, naming, input_cards


class Player(AbstractPlayer):
    base_name = "Player"

    def __init__(self, num: int, name: str, role: str):
        super().__init__(num=num, name=name, role=role)
    def president(self, cards: str | list[str], cnc: "AbstractPlayer"):
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
        return words, to_cnc, yes_or_no("Veto? ") if CARDS[X.BLACK] == 5 else False

    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
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

    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
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

