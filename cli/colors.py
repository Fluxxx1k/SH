try:
    raise Exception("We won't use colorama, because it doesn't support all colors")
    # from cli.colors2 import *
except Exception as e:
    from cli.colors_comp_test import get_best_color_code
    # from WebsiteEasiest.logger import logger
    # logger.warning(f"Could not import colors2: {repr(e)}"
    #                "\n\t\tMay be compatibility issues")
    GRAY_LIGHT_TEXT = get_best_color_code('\033[90m', '\033[38;5;252m')  # Светло-серый
    GRAY_MEDIUM_TEXT = GRAY_TEXT = get_best_color_code('\033[90m', '\033[38;5;244m')  # Средне-серый
    GRAY_DARK_TEXT = get_best_color_code('\033[90m', '\033[38;5;238m')  # Темно-серый
    BLACK_TEXT = '\033[30m'
    RED_TEXT = '\033[31m'
    GREEN_TEXT = '\033[32m'
    YELLOW_TEXT = '\033[33m'
    BLUE_TEXT = '\033[34m'
    PURPLE_TEXT = '\033[35m'
    CYAN_TEXT = '\033[36m'
    WHITE_TEXT = '\033[37m'
    RESET_TEXT = '\033[39m'

    RED_TEXT_BRIGHT = '\033[91m'
    GREEN_TEXT_BRIGHT = '\033[92m'
    YELLOW_TEXT_BRIGHT = '\033[93m'
    BLUE_TEXT_BRIGHT = '\033[94m'
    PURPLE_TEXT_BRIGHT = '\033[95m'
    CYAN_TEXT_BRIGHT = '\033[96m'
    WHITE_TEXT_BRIGHT = '\033[97m'

    GRAY_LIGHT_BACKGROUND = get_best_color_code('\033[100m', '\033[48;5;252m')
    GRAY_MEDIUM_BACKGROUND = GREY_BACKGROUND = get_best_color_code('\033[100m', '\033[48;5;244m')
    GRAY_DARK_BACKGROUND = get_best_color_code('\033[100m', '\033[48;5;238m')
    BLACK_BACKGROUND = '\033[40m'
    RED_BACKGROUND = '\033[41m'
    GREEN_BACKGROUND = '\033[42m'
    YELLOW_BACKGROUND = '\033[43m'
    BLUE_BACKGROUND = '\033[44m'
    PURPLE_BACKGROUND = '\033[45m'
    CYAN_BACKGROUND = '\033[46m'
    WHITE_BACKGROUND = '\033[47m'
    RESET_BACKGROUND = '\033[49m'

    RED_BACKGROUND_BRIGHT = '\033[101m'
    GREEN_BACKGROUND_BRIGHT = '\033[102m'
    YELLOW_BACKGROUND_BRIGHT = '\033[103m'
    BLUE_BACKGROUND_BRIGHT = '\033[104m'
    PURPLE_BACKGROUND_BRIGHT = '\033[105m'
    CYAN_BACKGROUND_BRIGHT = '\033[106m'
    WHITE_BACKGROUND_BRIGHT = '\033[107m'

    RESET = END = '\033[0m'
    NORMAL = '\033[22m'

    BOLD = '\033[1m'
    DIM = '\033[2m'
    # Яркие цвета текста с улучшенной палитрой при поддержке 256 цветов
    RED_TEXT_VERY_BRIGHT = get_best_color_code('\033[91m', '\033[38;5;196m')
    GREEN_TEXT_VERY_BRIGHT = get_best_color_code('\033[92m', '\033[38;5;46m')
    YELLOW_TEXT_VERY_BRIGHT = get_best_color_code('\033[93m', '\033[38;5;226m')
    BLUE_TEXT_VERY_BRIGHT = get_best_color_code('\033[94m', '\033[38;5;21m')
    PURPLE_TEXT_VERY_BRIGHT = get_best_color_code('\033[95m', '\033[38;5;201m')
    CYAN_TEXT_VERY_BRIGHT = get_best_color_code('\033[96m', '\033[38;5;51m')
    WHITE_TEXT_VERY_BRIGHT = get_best_color_code('\033[97m', '\033[38;5;15m')

    # Яркие цвета фона с улучшенной палитрой при поддержке 256 цветов
    RED_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[101m', '\033[48;5;196m')
    GREEN_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[102m', '\033[48;5;46m')
    YELLOW_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[103m', '\033[48;5;226m')
    BLUE_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[104m', '\033[48;5;21m')
    PURPLE_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[105m', '\033[48;5;201m')
    CYAN_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[106m', '\033[48;5;51m')
    WHITE_BACKGROUND_VERY_BRIGHT = get_best_color_code('\033[107m', '\033[48;5;15m')

# Additional styles - using closest available colorama equivalents
# Since colorama doesn't have direct equivalents for these, we'll define them as needed
CURSIVE = ITALIC = '\033[3m'  # Using ANSI code since colorama doesn't support italic
UNDERLINE = '\033[4m'  # Using ANSI code since colorama doesn't support underline
BLINK = '\033[5m'
NEGATIVE = '\033[7m'  # Using ANSI code since colorama doesn't support negative
CROSSED = STRIKETHROUGH = '\033[9m'  # Using ANSI code since colorama doesn't support strikethrough

# Additional ANSI codes for cursor movement and other features
UP = '\033[A'
DOWN = '\033[B'
RIGHT = '\033[C'
LEFT = '\033[D'
CLEAR_SCREEN = '\033[2J'
CLEAR_LINE = '\033[K'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'



def custom_text_rgb(r:int ,g: int,b: int) -> str:
    """
        May cause incompatibility issues, use carefully
    """
    return '\033[38;2;'f'{r};{g};{b}m'
def custom_font_rgb(r:int ,g:int ,b:int) -> str:
    """
        May cause incompatibility issues, use carefully
    """
    return '\033[48;2;'f'{r};{g};{b}m'

def custom_text_256(color:int) -> str:
    """
    May cause incompatibility issues but rarely, use carefully
    """
    return '\033[38;5;{color}m'.format(color=color)

def custom_font_256(color:int) -> str:
    """
    May cause incompatibility issues but rarely, use carefully
    """
    return '\033[48;5;{color}m'.format(color=color)

ct24 = custom_text_rgb
cf24 = custom_font_rgb
ct8 = custom_text_256
cf8 = custom_font_256

if __name__ == '__main__':
    for i in range(256):
        print(f"{ct8(i)}{i}", end=END+'\n')
        print(f"{cf8(i)}{i}", end=END+'\n')

    x = globals()
    for i in list(x):
        if i not in {'UP', 'DOWN', 'RIGHT', 'LEFT', 'CLEAR_SCREEN', 'CLEAR_LINE', 'HIDE_CURSOR', 'SHOW_CURSOR', 'SAVE_CURSOR', 'RESTORE_CURSOR'}:
            print(f'{x[i]}{i}{END}')
