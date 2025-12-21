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
for i in range(1):
    import user_settings
    user_settings.IS_BOT_ONLY = True
    print(f"GAME No {i}")
    # noinspection PyTypeChecker


