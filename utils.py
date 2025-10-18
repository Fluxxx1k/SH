from standard_names_SH import X
from standard_functions import color_clear
from HTML_colors import *
from colors import (GREEN_TEXT_BRIGHT as BLACK,
                    RESET_TEXT as END_T,
                    RED_TEXT as RED,
                    PURPLE_TEXT as PURPLE,
                    BOLD, END, UNDERLINE,
                    )

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
        return BOLD + "ERROR, please, show it in IRL" + END


def weighted_random(a, weights):
    import random
    return random.choices(a, weights, k=1)[0]

