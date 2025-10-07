def color_clear(s:str) -> str:
    """
    Removes all colors and returns new string.
    Do not use if another special symbols that starts on "\033" in s such as "\033[A"!!!
    """ 
    if not isinstance(s, str):
        return str(s)
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