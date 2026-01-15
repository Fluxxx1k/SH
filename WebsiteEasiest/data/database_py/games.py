from __future__ import annotations

import os, json
from typing import Optional

from WebsiteEasiest.memory_checker import memory_info
from WebsiteEasiest.data.data_paths import path_games, path_existed_games
from WebsiteEasiest.logger import logger


def count_games(active: bool = True, default_on_error: int = 0) -> int:
    logger.debug(f"Counting games {'active' if active else 'existed'}")
    try:
        return len(os.listdir(path_games if active else path_existed_games))
    except Exception as e:
        logger.error(repr(e))
        return default_on_error


def exists_game(game_name: str, default_on_error: bool = True) -> bool:
    logger.debug(f"Checking if game {repr(game_name)} exists")
    try:
        return os.path.exists(os.path.join(path_games, game_name + '.json'))
    except Exception as e:
        logger.error(repr(e))
        return default_on_error

def existed_game(game_name: str, default_on_error: bool = True) -> bool:
    logger.debug(f"Checking if game {repr(game_name)} existed")
    try:
        return os.path.exists(os.path.join(path_existed_games, game_name + '.json'))
    except Exception as e:
        logger.error(repr(e))
        return default_on_error


def deep_check_exists_game(game_name: str, default_on_error: bool = True) -> bool:
    logger.debug(f"Deep checking if game {repr(game_name)} exists or existed")
    exists = exists_game(game_name, default_on_error)
    existed = existed_game(game_name, default_on_error)
    print(f'\033[102m{game_name} exists: {exists}, existed: {existed}\033[0m')

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


def save_data_of_game(game_name: str, game_data: dict) -> bool:
    logger.debug(f"Saving data of game {repr(game_name)}: {game_data}")
    try:
        if exists_game(game_name):
            with open(os.path.join(path_games, game_name + '.json'), 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=4, ensure_ascii=False)
            return True
        else:
            logger.debug('Game not found')
    except Exception as e:
        logger.error(repr(e))
    return False

def create_game_db(game_name: str, creator: str, password: str=None, data: dict=None) -> tuple[bool, Optional[str]]:
    logger.debug(f"Creating game {repr(game_name)} with creator {repr(creator)} and password {repr(password)}")
    from WebsiteEasiest.settings.web_config import New_games_allowed
    if not New_games_allowed:
        return False, repr(PermissionError(f'New games are not allowed: {memory_info}'))
    try:
        if len(game_name) < 3:
            return False, repr(ValueError('Game name cannot be less than 3 characters'))
        if password == '':
            password = None
        if deep_check_exists_game(game_name, True):
            logger.debug(f'Game {repr(game_name)} already exists or existed')
            return False, repr(FileExistsError(f'Game "{game_name}" already exists or existed'))
        else:
            open(os.path.join(path_games, game_name + '.json'), 'w+').close()
            save_data_of_game(game_name, {
                'creator': creator,
                **(data or {})
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

