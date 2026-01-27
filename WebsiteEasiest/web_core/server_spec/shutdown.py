from WebsiteEasiest.logger import logger
import json, atexit, os, time, threading

@atexit.register
def shutdown_save():
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

def shutdown_force(timeout=30, memory_info:int =None):
    try:
        threading.Thread(target=shutdown_save, daemon=True).start()
        time.sleep(timeout)
    except BaseException as E:
        logger.critical(f"Shutdown server failed with {f'{(memory_info >> 10) / 1024: .2f} MB' if memory_info else 'No memory info'}: {repr(E)}")
    else:
        logger.critical(f"Shutdown server failed with {f'{(memory_info >> 10) / 1024: .2f} MB' if memory_info else 'No memory info'} with no response, hard kill!")
    finally:
        os._exit(1)
