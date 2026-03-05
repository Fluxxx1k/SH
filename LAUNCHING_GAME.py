try:
    import user_settings
except Exception as e:
    print(repr(e))
    print("Cannot use user settings")
    exit(0)
else:
    try:
        if user_settings.LOG_CONSOLE:
            from DEBUG_TOOLS import based_logger
        print("Will be created log of console")
    except Exception as e:
        print(repr(e))
        print("Cannot log console of game")
print("Checking files:")
try:
    import os
    not_done = False
    need = ['core/HTML_colors.py', 'core/HTML_logs.py',
            'LAUNCHING_GAME.py', 'SH2.py',
            'Players/bot.py', 'Players/bot2.py', 'cli/colors.py',
            'core/globs.py', 'Players/player.py',
            'core/standard_classes.py',
            'core/standard_functions.py',
            'core/standard_names_SH.py',
            'cli/user_color_settings.py',
            'user_settings.py', 'core/utils.py',]
    for i in need:
        if os.path.isfile(i):
            print(f"\033[32mFound: {i}\033[0m")
        else:
            print(f"\033[31mNot found: {i}\033[0m")
            not_done = True
    if not_done:
        print("\033[31mWARNING: Some files are not installed or renamed, may be problems!\033[0m")
        if not input("Press Enter if you want to exit or anything to try to launch: "):
            print("\033[31mClosing...\033[0m")
            exit(0)
        else:
            print("\033[31mContinuing...\033[0m")
except BaseException as e:
    import traceback
    print(traceback.format_exc())
    print(repr(e))
print("Do you want to play (1) or only log the game (2)?")
temp = input("Input: ")
while temp != '1' and temp != '2':
    temp = input("Input: ")
if temp == '1':
    print("\033[32mLaunching\033[0m")
    try:
        # noinspection PyUnusedImports
        import SH2
    except BaseException as e:
        import traceback
        print(traceback.format_exc())
        print(repr(e))
        print("\033[31mClosing...\033[0m")
        exit(0)
elif temp == '2':
    print("\033[31mNot available now...\033[0m")