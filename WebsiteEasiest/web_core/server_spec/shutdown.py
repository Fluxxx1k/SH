from WebsiteEasiest.logger import logger
import json, atexit, os, time, threading

saving_finished: bool = False

@atexit.register
def save_cache(final=False):
    from WebsiteEasiest.data.data_paths import path_banned
    from WebsiteEasiest.data.database_py.games import games_data_dict, save_data_of_game
    from WebsiteEasiest.data.database_py.players import players_data_dict, save_data_of_player
    logger.warning("Shutting down the server")
    for i in games_data_dict:
        if not save_data_of_game(i, games_data_dict[i]):
            logger.error(f"Could not save data of game {i}: {games_data_dict[i]}")
        else:
            logger.debug(f"Successfully saved data of game {i}: {games_data_dict[i]}")
    for i in players_data_dict:
        if not save_data_of_player(i, players_data_dict[i]):
            logger.error(f"Could not save data of player {i}: {players_data_dict[i]}")
        else:
            logger.debug(f"Successfully saved data of player {i}: {players_data_dict[i]}")
    try:
        from WebsiteEasiest.web_loggers import bans
        with open(path_banned, "w+", encoding='utf-8') as f:
            json.dump(list(bans), f)
    except NameError as e:
        logger.error(f"Could not save bans: {repr(e)}")
    except Exception as e:
        try:
            logger.critical(f"Could not save bans: {repr(e)} | {bans}")
        except Exception as e2:
            logger.critical(f"Could not save bans: {repr(e)}, {repr(e2)}")
    else:
        logger.debug(f"Successfully saved data of bans: {bans}")
    global saving_finished
    if final:
        saving_finished = True

def shutdown_force(timeout=30):
    try:
        from WebsiteEasiest.settings import web_config
        web_config.New_games_allowed = False
    except Exception as e:
        logger.error(f"Could not set New_games_allowed to False: {repr(e)}")
    try:
        from WebsiteEasiest.memory_checker import memory_info
    except Exception as e:
        logger.warning(f"Could not get memory_info: {repr(e)}")
        memory_info = None
    try:
        from WebsiteEasiest.memory_checker import cpu_percent
    except Exception as e:
        logger.warning(f"Could not get cpu_percent: {repr(e)}")
        cpu_percent = None
    try:
        threading.Thread(target=save_cache, daemon=True, args=(True, )).start()
        time.sleep(timeout)
    except BaseException as E:
        logger.critical(f"Shutdown server failed with:"
                        f"\n\t\tMemory ({f'{(memory_info >> 10) / 1024: .2f} MB' if memory_info else 'No memory info'}) and"
                        f"\n\t\tCPU ({f'{cpu_percent: .1f}%' if cpu_percent else 'No cpu_percent info'}): "
                        f"\n\t\t{repr(E)}")
    else:
        if saving_finished:
            logger.info(f"Time for saving files ended:"
                f"\n\t\tMemory ({f'{(memory_info >> 10) / 1024: .2f} MB' if memory_info else 'No memory info'}) and"
                f"\n\t\tCPU ({f'{cpu_percent: .1f}%' if cpu_percent else 'No cpu_percent info'}): "
                f"\n\t\tSaved successfully.")
        else:
            logger.critical(f"Shutdown server failed with time out:"
                           f"\n\t\tMemory ({f'{(memory_info >> 10) / 1024: .2f} MB' if memory_info else 'No memory info'}) and"
                           f"\n\t\tCPU ({f'{cpu_percent: .1f}%' if cpu_percent else 'No cpu_percent info'}): "
                           f"\n\t\tNo response in {timeout} sec.")
    finally:
        os._exit(1)
