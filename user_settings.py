NAME_FOR_LOGS: str = "SH LOG_TEST "  # You can change it
tp: str = '.html'  # расширение
MIN_NAME_LEN: int = 1
MAX_NAME_LEN: int = 15  # You can change it from 10 to infinity


MIN_PLAYER_NUM: int = 4
MAX_PLAYER_NUM: int = 10

RED_WIN_NUM: int = 5
BLACK_WIN_NUM: int = 6

ANARCHY_SKIP_NUM: int = 3
DEBUG_MODE: bool = True
IS_PRINT_FULL_INFO: bool = DEBUG_MODE
IS_PRINT_SMALL_INFO: bool = DEBUG_MODE

TABLE_SPLITTER: str = '|'
def get_roles(length: int) -> tuple[list[str], bool]:
    """
    creates shuffled list of roles
    :param length: len of list
    """
    import random
    from standard_names_SH import X
    hitler = [X.HITLER]
    black = [X.BLACK]
    if length <= 4:
        black *= 0
    elif length <= 6:
        black *= 1
    elif length <= 8:
        black *= 2
    elif length <= 10:
        black *= 3
    else:
        from standard_functions import my_input
        black *= my_input("Too many players, input how many fascists will be in game",
                          integer=True)
    molotov = []
    ribbentrop = []
    roles = hitler + black + molotov + ribbentrop
    red = [X.RED] * (length - len(roles))
    roles.extend(red)
    random.shuffle(roles)
    return roles, bool(molotov or ribbentrop)
