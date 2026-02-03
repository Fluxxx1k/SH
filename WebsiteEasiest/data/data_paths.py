import os

from WebsiteEasiest.logger import logger
dirname = os.path.dirname(__file__)

path_games = os.path.join(dirname, 'games')
path_existed_games = os.path.join(dirname, 'ended_games')
path_logs_games = os.path.join(dirname, 'logs_games')
path_actions_games = os.path.join(dirname, 'actions_games')
os.makedirs(path_games, exist_ok=True)
os.makedirs(path_existed_games, exist_ok=True)
os.makedirs(path_logs_games, exist_ok=True)
os.makedirs(path_actions_games, exist_ok=True)

path_players = os.path.join(dirname, 'players')
os.makedirs(path_players, exist_ok=True)
try:
    path_IP = os.path.join(dirname, 'IP')
    os.makedirs(path_IP, exist_ok=True)
except Exception as e:
    path_IP = None
    logger.error(f"Failed to create or open IP directory: {repr(e)}")
try:
    path_banned = os.path.join(dirname, 'banned_IP.json')
    open(path_banned, 'a+', encoding='utf-8').close()
except Exception as e:
    path_banned = None
    logger.error(f"Failed to create or open banned_IP.json: {repr(e)}")


logger.low_debug(f"Paths:"
             f"\n\t\t{__file__= }"
             f"\n\t\t{dirname= },"
             f"\n\t\t{path_games= },"
             f"\n\t\t{path_existed_games= },"
             f"\n\t\t{path_logs_games= },"
             f"\n\t\t{path_actions_games= },"
             f"\n\t\t{path_players= },"
             f"\n\t\t{path_IP= },"
             f"\n\t\t{path_banned= }")
