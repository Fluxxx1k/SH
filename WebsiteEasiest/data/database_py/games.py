from __future__ import annotations

import os, json, sys
from typing import Optional

from WebsiteEasiest.logger import logger

path_games = os.path.join(os.path.basename(os.path.basename(__file__)), 'data', 'games')
path_existed_games = os.path.join(os.path.basename(os.path.basename(__file__)), 'data', 'ended_games')
os.makedirs(path_games, exist_ok=True)
os.makedirs(path_existed_games, exist_ok=True)

def count_games(active: bool = True) -> int:
    logger.debug(f"Counting games {'active' if active else 'existed'}")
    try:
        return len(os.listdir(path_games if active else path_existed_games))
    except Exception as e:
        logger.error(repr(e))
        return 0


def exists_game(game_name: str) -> bool:
    logger.debug(f"Checking if game {repr(game_name)} exists")
    return os.path.exists(os.path.join(path_games, game_name + '.json'))

def existed_game(game_name: str) -> bool:
    logger.debug(f"Checking if game {repr(game_name)} existed")
    return os.path.exists(os.path.join(path_existed_games, game_name + '.json'))


def deep_check_exists_game(game_name: str) -> bool:
    logger.debug(f"Deep checking if game {repr(game_name)} exists or existed")
    try:
        exists = exists_game(game_name)
    except Exception as e:
        logger.error(repr(e))
        exists = True
    try:
        existed = existed_game(game_name)
    except Exception as e:
        logger.error(repr(e))
        existed = True
    return exists or existed



def get_data_of_game(game_name: str) -> tuple[bool, dict | str]:
    logger.debug(f"Getting data of game {repr(game_name)}")
    try:
        if exists_game(game_name):
            return True, json.load(open(os.path.join(path_games, game_name + '.json'), encoding='utf-8'))
        else:
            return False, repr(FileNotFoundError(f'Game "{game_name}" not found'))
    except Exception as e:
        logger.error(repr(e))
        return False, repr(e)


def save_data_of_game(game_name: str, game_data: dict) -> None:
    logger.debug(f"Saving data of game {repr(game_name)}: {game_data}")
    try:
        if exists_game(game_name):
            with open(os.path.join(path_games, game_name + '.json'), 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=4, ensure_ascii=False)
        else:
            logger.debug('Game not found')
    except Exception as e:
        logger.error(repr(e))

def create_game(game_name: str, creator: str, password: str=None) -> tuple[bool, Optional[str]]:
    logger.debug(f"Creating game {repr(game_name)} with creator {repr(creator)} and password {repr(password)}")
    try:
        if len(game_name) < 3:
            return False, repr(ValueError('Game name cannot be less than 3 characters'))
        if password == '':
            password = None
        if deep_check_exists_game(game_name):
            logger.debug(f'Game {repr(game_name)} already exists')
            return False, repr(FileExistsError(f'Game "{game_name}" already exists'))
        else:
            open(os.path.join(path_games, game_name + '.json'), 'w+').close()
            save_data_of_game(game_name, {
                'game_name': game_name,
                'password': password,
                'creator': creator,
                'players': [creator],
            })
        return True, None
    except Exception as e:
        logger.error(repr(e))
        return False, repr(e)




def end_game(game_name: str, game_data: dict = None) -> tuple[bool, Optional[str]]:
    logger.debug(f"Ending game {repr(game_name)} with data {game_data}")
    try:
        if game_data is not None:
            save_data_of_game(game_name, game_data)
        os.replace(os.path.join(path_games, game_name + '.json'), os.path.join(path_existed_games, game_name + '.json'))
        return True, None
    except FileExistsError as e:
        return False, f'Game "{game_name}" already existed, data will be lost: {repr(e)}'
    except Exception as e:
        return False, repr(e) + f' Game "{game_name}" will be lost'

