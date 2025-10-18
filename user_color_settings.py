from colors import *
INPUT_COLOR = BOLD + PURPLE_TEXT_BRIGHT

CRITICAL = RED_BACKGROUND_BRIGHT + CYAN_TEXT_BRIGHT + UNDERLINE + BOLD
WARNING = YELLOW_BACKGROUND_BRIGHT + CYAN_TEXT_BRIGHT + UNDERLINE + BOLD
GOOD = GREEN_BACKGROUND_BRIGHT + BLACK_TEXT + UNDERLINE + BOLD
def critical(text:str | list[str], negative_letter=2) -> None:
    s = CRITICAL
    for letter in range(len(text)):
        if letter % negative_letter == negative_letter - 1:
            s += NEGATIVE + text[letter] + RESET
        else:
            s += CRITICAL + text[letter]
    s += RESET
    print(s)

if __name__ == '__main__':
    x = globals()
    for i in list(x):
        print(f'{x[i]}{i}{END}')
    critical("TEST for CrItIcAl", negative_letter=3)
