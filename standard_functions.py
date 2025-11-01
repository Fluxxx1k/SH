from colors import PURPLE_TEXT, END, RESET_BACKGROUND, RESET_TEXT, UP
from user_color_settings import WARNING
from standard_names_SH import MyErr
def color_clear(s:str | list, print_errors=True) -> str:
    """
    Removes all colors and returns new string.
    Do not use if another special symbols that starts on "\033" in s such as "\033[A"!!!
    """ 
    if not isinstance(s, str) and not isinstance(s, list):
        if print_errors:
            print(s, "isn't an str or list")
        try:
            return color_clear(str(s), print_errors=print_errors)
        except BaseException as err:
            if print_errors:
                print(f"Something went wrong: {err},", s, " can't be str")
            try:
                return color_clear(list(s), print_errors=print_errors)
            except BaseException as err:
                if print_errors:
                    print(f"{WARNING}Something went wrong: {err},", s, f" also can't be list{END}")
                return "Error"
    s1 = ''
    x = False
    for i in s:
        if i == '\033':
            x = True
        elif i == 'm' and x:
            x = False
        elif not x:
            s1 += i
    return s1


def is_x_in_y(x: set | list | str, y: set | list | str) -> bool:
    """
    checks that all symbols from x also in y
    """
    if isinstance(y, set):
        if isinstance(x, set):
            return x.issubset(y)
        for i in set(x):
            if i not in y:
                return False
            if 1 < x.count(i):
                return False
        return True

    for i in set(x):
        if i not in y:
            return False
        if y.count(i) < x.count(i):
            return False
    return True


def yes_or_no(text='Input for something (If you see it, you should understand what should be asked): ',
              yes: set = frozenset({'Y', 'YES'}),
              no: set = frozenset({'N', "NO"})) -> bool:
    dbg_y = "DEBUG_YES"
    dbg_n = "DEBUG_NO"
    text = str(text).strip()
    if text == '':
        pass
        #print(f"{WARNING}No text!{END}")
        #text = 'Input for something (If you see it, you should understand what should be asked): '
    elif text[-1] != ":":
        text += ": "
    else:
        text += " "
    inp = my_input(text, upper=True, possible=yes|no|{dbg_n, dbg_y})
    if inp in no or inp == "DEBUG_NO":
        return False
    elif inp in yes or inp == "DEBUG_YES":
        return True
    else:
        inp = my_input("ERROR" + text, upper=True, possible={"YES", "NO", dbg_n, dbg_y})
        if inp == "YES":
            return True
        elif inp == "NO":
            return False
        else:
            print(f"{UP}FUCK, IDK")
            return False



def show_only_to_one(text: str, hide_len: int = None) -> None:
    if hide_len is None:
        hide_len = len(color_clear(text))
    print("Are you ready to see info?")
    print("(Remember it. Don't show it to anybody)")
    print("Say \"y\" only if YOU should see it: ")
    if yes_or_no("Show?", no=set()):
        print(text)
    if yes_or_no("Hide? ", no=set()):
        print(f"{END}\x1b[A\x1b[A" + "#" * hide_len) # ⣿
        print()


def my_input(prompt, color:str= RESET_TEXT + RESET_BACKGROUND, input_color=PURPLE_TEXT, *,
             possible:set[str]=None, strip=True, upper=False, lower=False, integer: bool=False) -> str|int:
    if possible is None:
        possible = set()
    x = input('\b' + color + prompt + input_color)
    print('\r' + END, end='')    
    while True:
        try:
            if strip:
                x = x.strip()
            if upper:
                x = x.upper()
            if lower:
                x = x.lower()
            if possible:
                if x not in possible:
                    raise MyErr("Impossible")
            if integer:
                if not x.isdigit():
                    raise MyErr("Not a digit")
                return int(x)
            return x
        except MyErr as err:
            x = input('\b' + UP + str(err.args[0]) + ": " + color + prompt + input_color)
            print('\r' + END, end='')
        except KeyboardInterrupt as err:
            raise err
        except EOFError as err:
            return str(err)
        except BaseException as err:
            print(f"{UP*2}Error occurred while inputting: {WARNING}{err}{END}")
