try:
    import user_settings
except Exception as e:
    print(repr(e))
    print("Cannot use user settings")
    exit(0)
else:
    try:
        if user_settings.LOG_CONSOLE:
            import based_logger
        print("Will be created log of console")
    except Exception as e:
        print(repr(e))
        print("Cannot log console of game")
print("Checking files:")
try:
    import os
    out_file = []
    out_dirs = []
    need = ['HTML_colors.py', 'HTML_logs.py', 'LAUNCHING_GAME.py', 'SH2.py', 'bot.py', 'colors.py', 'globs.py', 'player.py', 'standard_classes.py', 'standard_functions.py', 'standard_names_SH.py', 'test.py', 'user_color_settings.py', 'user_settings.py', 'utils.py']
    for item in sorted(os.listdir(os.getcwd())):
        if item.endswith('.py'):
            out_file.append(item)
        elif os.path.isdir(item):
            out_dirs.append(f"[{item}]")
    for item in out_dirs:
        print(item)
    for item in out_file:
        print(item)
    not_done = set(need).difference(set(out_file))
    for item in not_done:
        print(f"\033[33m{item}\033[0m")
    if not_done:
        print("\033[31mWARNING: Some files are not installed or renamed, may be problems!\033[0m")
        if not input("Press Enter if you want to exit or anything to try to launch: "):
            print("\033[31mClosing...\033[0m")
            exit(0)
        else:
            print("\033[31mContinuing...\033[0m")
except Exception as e:
    print(e)
print("Do you want to play (1) or only log the game (2)?")
temp = input("Input: ")
while temp != '1' and temp != '2':
    temp = input("Input: ")
if temp == '1':
    print("\033[32mLaunching\033[0m")
    # noinspection PyUnusedImports
    import SH2
elif temp == '2':
    print("\033[31mNot available now...\033[0m")