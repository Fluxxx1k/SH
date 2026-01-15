import os

from WebsiteEasiest.logger import logger
dirname = os.path.dirname(__file__)

path_games = os.path.join(dirname, 'games')
path_existed_games = os.path.join(dirname, 'ended_games')
os.makedirs(path_games, exist_ok=True)
os.makedirs(path_existed_games, exist_ok=True)

path_players = os.path.join(dirname, 'players')
path_IP = os.path.join(dirname, 'IP')
os.makedirs(path_players, exist_ok=True)
os.makedirs(path_IP, exist_ok=True)

logger.debug(f"Paths:"
             f"\n\t\t{__file__= }"
             f"\n\t\t{dirname= },"
             f"\n\t\t{path_games= },"
             f"\n\t\t{path_existed_games= },"
             f"\n\t\t{path_players= },"
             f"\n\t\t{path_IP= }")
