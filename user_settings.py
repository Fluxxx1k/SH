NAME_FOR_LOGS = "SH LOG_TEST "  # You can change it
tp = '.html'  # расширение
MAX_NAME_LEN = 15  # You can change it from 10 to infinity


MIN_PLAYER_NUM = 4
MAX_PLAYER_NUM = 10

RED_WIN_NUM = 5
BLACK_WIN_NUM = 6

ANARCHY_SKIP_NUM = 3

def get_roles(c: int) -> tuple[list[str], bool]:
    import random
    from standard_names_SH import X
    hitler = [X.HITLER]
    black = [X.BLACK]
    if c <= 4:
        black *= 0
    elif c <= 6:
        black *= 1
    elif c <= 8:
        black *= 2
    elif c <= 10:
        black *= 3
    else:
        from standard_functions import my_input
        black *= my_input("Too many players, input q",
                          integer=True)
    molotov = []
    ribbentrop = []
    roles = hitler + black + molotov + ribbentrop
    red = [X.RED] * (c - len(roles))
    roles.extend(red)
    random.shuffle(roles)
    return roles, bool(molotov + ribbentrop)
