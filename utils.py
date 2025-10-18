from standard_names_SH import X
from standard_functions import color_clear
from HTML_colors import *
from colors import (GREEN_TEXT_BRIGHT as BLACK,
                    RESET_TEXT as END_T,
                    RED_TEXT as RED,
                    PURPLE_TEXT as PURPLE,
                    BOLD, END, UNDERLINE
                    )
from user_color_settings import INPUT_COLOR, WARNING


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


def get_color(x, out_type=''):
    x = color_clear(x)
    for i in [X.BLACK, X.HITLER, X.RIB]:
        if i in x:
            if out_type == X.BOT:
                if i == X.HITLER:
                    return X.HTLR
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
    letters = {'X', 'R', 'B'}
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

