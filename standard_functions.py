from colors import PURPLE_TEXT, WARNING, END
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
    text = str(text).strip()
    if text == '':
        print(f"{WARNING}No text!{END}")
        text = 'Input for something (If you see it, you should understand what should be asked): '
    elif text[-1] != ":":
        text += ": "
    else:
        text += " "
    inp = input(text).strip().upper()
    while True:
        if inp in no or inp == "DEBUG_NO":
            return False
        elif inp in yes or inp == "DEBUG_YES":
            return True
        inp = input('\x1b[A' + f"{PURPLE_TEXT}New try: {text}{END}").strip().upper()


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