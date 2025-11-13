import sys
from globs import PLAYERS
from standard_classes import POSSIBLE_CARDS
from standard_names_SH import X
from standard_functions import color_clear, my_input
from HTML_colors import *
from colors import (GREEN_TEXT_BRIGHT as BLACK,
                    RESET_TEXT as END_T,
                    RED_TEXT as RED,
                    PURPLE_TEXT as PURPLE,
                    BOLD, END, UNDERLINE, RESET_TEXT, UP
                    )
from user_color_settings import INPUT_COLOR, WARNING, CRITICAL


def coloring(s, sort=True, is_print=True):
    if sort:
        s = sorted(color_clear(s))
    s1 = ''
    for i in s:
        if i == 'B':
            s1 += BLACK + i + END_T
        elif i == 'R':
            s1 += RED + i + END_T
        elif i == 'X':
            s1 += i
        elif i == 'P':
            s1 += PURPLE + i + END_T
        else:
            if is_print:
                print(f"{i} should be 'X' or 'R' or 'B'")
            break
    else:
        return s1
    return s



def naming(s:str) -> str:
    if s in {"R", X.RED}:
        return RED + "RED" + END_T
    if s in {"H", X.HITLER}:
        return BLACK + "HITLER" + END_T
    if s in {"B", X.BLACK}:
        return BLACK + "BLACK" + END_T
    if s in {"S", X.STALIN}:
        return RED + "STALIN" + END_T
    if s in {"M", X.MOLOTOV}:
        return RED + "MOLOTOV" + END_T
    if s in {"RIB", X.RIBBENTROP}:
        return BLACK + "RIBBENTROP" + END_T
    if s in {"A", "ANARCHY", X.ANARCHIST}:
        return PURPLE + "ANARCHIST" + END_T
    if s in {"X", "UNKNOWN", "IDK"}:
        return "UNKNOWN"
    return X.ERROR


def get_color(x:str, out_type=''):
    """
    :param x: role
    :param out_type: can be
    :return: returns colored string with role or color in HTML or bot_mind
    """
    x = color_clear(x)
    for i in [X.BLACK, X.HITLER, X.RIB]:
        if i in x:
            if out_type == X.BOT:
                if i == X.HITLER:
                    return X.HITLER
                return X.BLACK
            if out_type == "HTML":
                return black_c
            return BLACK + BOLD + X.BLACK + END
    for i in [X.RED, X.MOLOTOV, X.STALIN]:
        if i in x:
            if out_type == X.BOT:
                return X.RED
            if out_type == "HTML":
                return red_c
            return RED + BOLD + X.RED + END
    if X.NRH in x:
        if out_type == X.BOT:
            return X.NRH
        if out_type == "HTML":
            return nrh_c
        return BOLD + X.NRH + END
    else:
        if out_type == X.BOT:
            print(f"{RED}{BOLD}{UNDERLINE}Bot error, unknown role... Using {PURPLE}ANARCHIST{RED} type...{END}")
            return X.NRH
        if out_type == "HTML":
            return norm_c
        return WARNING + "ERROR, please, show it in IRL" + END


def weighted_random(a, weights):
    import random
    return random.choices(a, weights, k=1)[0]


def input_cards(text=f"{WARNING}Some input: {END_T}", q: int | set[int] = 0, c_p:bool=False, veto=False) -> str:
    """
    c_p - chancellor placing, don't laugh
    """
    if not isinstance(veto, bool):
        print(f"{RED}{BOLD}{UNDERLINE}{veto = } | it's not good!{END}")
        veto = True
    letters = POSSIBLE_CARDS.copy()
    if q == 0:  # quality didn't change
        print(f"{RED}{BOLD}{UNDERLINE}Input length is {q = }, it will be 1-3 now")
        q = {1, 2, 3}
    elif not isinstance(q, set):
        q = {q}
    if c_p and not veto:  # chancellor should place card if it wasn't veto
        letters -= {'X'}
    if c_p:  # if president was skipped in game, but not in code
        letters.add("SKIP")
    inp = input(text + END + INPUT_COLOR).strip().upper()
    print(END, end='')
    while len(inp) not in q or (len(letters | set(inp)) > 3 and inp not in letters):
        print(f"{RED}WRONG    INPUT{END}")
        inp = input(PURPLE + "New try: " + END_T + text + END + INPUT_COLOR).strip().upper()
        print(END, end='')
    return inp

def voting_human(theme: str = f"{WARNING}Voting, U forgot to add text{END}", who: list["Player"]=None, type_ov_voting=X.COORDINATION, *, anonim = False) -> dict[int, int]:
    if who is None:
        who = PLAYERS
    result: dict[int, int] = {}
    print(theme)
    skip = {'=', 'skip', 'pass', 'x'}
    if type_ov_voting == X.COORDINATION:
        no = {'-', 'n', 'no'}
        yes = {'+', 'y', 'yes'}
        for player in who:
            vote =  my_input(f"[{PURPLE}{player}{RESET_TEXT}]: {INPUT_COLOR}", possible=skip|yes|no, lower=True)
            if anonim:
                print(f"{UP}[{PURPLE}{player}{RESET_TEXT}]: {INPUT_COLOR}" + f"####{END}")
            if vote in skip:
                continue
            elif vote in no:
                result[player.num] = -1
            elif vote in yes:
                result[player.num] = 1
            else:
                print(f"{CRITICAL}WRONG    VOTE ({vote}), ignoring{END}")

    elif type_ov_voting == X.CHOOSE_ONE:
        ...

def out(c:int = None, file=sys.stdout):
    if c is None:
        import globs
        c = globs.COUNT_PLAYERS
    for player_num in range(c):
        print(f"№{player_num + 1}) {PLAYERS[player_num].out()}", file=file)

