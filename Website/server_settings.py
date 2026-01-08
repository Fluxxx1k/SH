DIRECTORY_FOR_GAME_LOGS: str = "LOGS"
NAME_FOR_GAME_LOGS: str = "SH LOG_TEST "  # You can change it
EXTENSION_FOR_GAME_LOGS: str = '.html'  # расширение
MIN_NAME_LEN: int = 1
MAX_NAME_LEN: int = 15  # You can change it from 10 to infinity


MIN_PLAYER_NUM: int = 4
MAX_PLAYER_NUM: int = 10

RED_WIN_NUM: int = 5
BLACK_WIN_NUM: int = 6

ANARCHY_SKIP_NUM: int = 3
DEBUG_MODE: bool = True
IS_PROMT_ENTERING_COMMAND: bool = False
LOG_CONSOLE: bool = DEBUG_MODE
IS_PRINT_FULL_INFO: bool = DEBUG_MODE
IS_PRINT_SMALL_INFO: bool = False
DIRECTORY_FOR_CONSOLE_LOGS:str = "Console_logs"
NAME_FOR_CONSOLE_LOGS:str = "log"
EXTENSION_FOR_CONSOLE_LOGS: str = '.txt'  # расширение

TABLE_SPLITTER: str = '|'
DATE_FORMAT: str = "%d.%m.%y"
TIME_FORMAT: str = "%H:%M:%S"

def get_roles(length: int) -> tuple[list[str], bool]:
    """
    creates shuffled list of roles
    :param length: len of list
    """
    import random
    from core.standard_names_SH import X
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
        from core.standard_functions import my_input
        black *= int(my_input("Too many players, input how many fascists will be in games",
                          integer=True))
    molotov = []
    ribbentrop = []
    anarchist = [X.ANARCHIST]
    roles = hitler + black + molotov + ribbentrop + anarchist
    red = [X.RED] * (length - len(roles))
    roles.extend(red)
    random.shuffle(roles)
    return roles, bool(molotov or ribbentrop)

def get_bot_places(length: int) -> list[int]:
    """
    creates list of places for bots
    :param length: number of bots
    """
    from legacy.globs import COUNT_PLAYERS
    import random
    bot_places = random.sample(range(COUNT_PLAYERS), length)
    return bot_places


# Funny thing, if you set it to True,
# then all games will be generated automatically with bots
# made for debug
IS_BOT_ONLY: bool = False
BOT_BASE_NAME = "Bot"
BOT_NUM: int = 7


VOTE_BY_ONE: bool = True
VOTE_ANONYMOUS: bool = False


WEBSITE_USING: bool = True
