from __future__ import annotations

import os, json
from typing import Optional, Literal

from WebsiteEasiest.data.database_py.players import add_game_to_player
from WebsiteEasiest.data.data_paths import path_games, path_existed_games, path_logs_games, path_actions_games
from WebsiteEasiest.logger import logger


games_data_dict: dict[str, dict] = {}


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
    if game_name in games_data_dict:
        logger.debug(f"Getting data of game {repr(game_name)} from cache")
        return True, games_data_dict[game_name]
    try:
        logger.debug(f"Getting data of game {repr(game_name)} from file")
        if exists_game(game_name):
            games_data_dict[game_name] = json.load(open(os.path.join(path_games, game_name + '.json'), encoding='utf-8'))
            return True, games_data_dict[game_name]
        else:
            return False, f'Game "{game_name}" not found'
    except Exception as e:
        logger.error(repr(e))
        return False, e.__class__.__name__

def get_logs_of_game(game_name: str) -> tuple[bool, list[dict[str, str|int]] | str]:
    try:
        logger.debug(f"Getting logs of game {repr(game_name)} from file")
        if exists_game(game_name):
            game_logs = json.load(open(os.path.join(path_logs_games, game_name + '.json'), encoding='utf-8'))
            return True, game_logs
        else:
            return False, f'Game "{game_name}" not found'
    except Exception as e:
        logger.error(repr(e))
        return False, e.__class__.__name__



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
        from WebsiteEasiest.memory_checker import memory_info
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




def end_game_db(game_name: str, game_data: dict = None, delete: bool = False) -> tuple[bool, Optional[str]]:
    logger.debug(f"Ending game {repr(game_name)} with data {game_data}")
    try:
        if game_data is None:
            game_found, game_data = get_data_of_game(game_name)
            if not game_found:
                return False, game_data
        save_data_of_game(game_name, game_data)
        players = game_data.get('players')
        if players is None:
            logger.warning(f'Game {repr(game_name)} has no players')
        else:
            for player in players:
                success, info = add_game_to_player(player, '')
                if not success:
                    logger.warning(f'Error removing game from player {repr(player)}: {info}')
        if not delete:
            logger.info(f"Ending game {game_name}: {game_data}")
            os.replace(os.path.join(path_games, game_name + '.json'), os.path.join(path_existed_games, game_name + '.json'))
        else:
            logger.warning(f"Deleting game {game_name}: {game_data}")
            os.remove(os.path.join(path_games, game_name + '.json'))
        games_data_dict.pop(game_name, None)
        return True, None
    except FileExistsError as e:
        return False, f'Game "{game_name}" already existed, data will be lost: {repr(e)}'
    except Exception as e:
        logger.error(repr(e))
        return False, e.__class__.__name__ + f' Game "{game_name}" will be lost'

def get_vote_of_player_in_game(player_name: str, game_name: str) -> tuple[bool, dict | str]:
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        return False, game_data
    if player_name not in game_data.get('votes', {}):
        return False, f'Player {player_name} has not voted in game {game_name}'
    return True, game_data['votes'][player_name]

def get_vote_of_player_in_game_type_2(player_name: str, game_name: str, get_type: Literal['yesNo', 0, 'target', 1]) -> tuple[bool, str, float]:
    try:
        if get_type == 'yesNo' or get_type == 0:
            with open(os.path.join(path_actions_games, "YesNo", game_name + '.txt'), encoding='utf-8') as f:
                vote = f.readline()
                timestamp = float(f.readline())
                return True, vote.strip(), timestamp
        elif get_type == 'target' or get_type == 1:
            with open(os.path.join(path_actions_games, "Target", game_name + '.txt'), encoding='utf-8') as f:
                vote = f.readline()
                timestamp = float(f.readline().strip())
                return True, vote.strip(), timestamp
        else:
            raise ValueError(f"Invalid get_type: {get_type}")

    except Exception as e:
        logger.error(f"Failed to get vote of player {player_name} in game {game_name}: {repr(e)}")
        return False, repr(e), 0

def set_vote_of_player_in_game_type_2(player_name: str, game_name: str, vote: str, get_type: Literal['yesNo', 0, 'target', 1], timestamp: float = None) -> tuple[bool, str|None]:
    if timestamp is None:
        import time
        timestamp = time.time()
    try:
        if get_type == 'yesNo' or get_type == 0:
            with open(os.path.join(path_actions_games, "YesNo", game_name + '.txt'), 'w+', encoding='utf-8') as f:
                f.write(vote + '\n')
                f.write(str(timestamp) + '\n')
            return True, None
        elif get_type == 'target' or get_type == 1:
            with open(os.path.join(path_actions_games, "Target", game_name + '.txt'), 'w+', encoding='utf-8') as f:
                f.write(vote + '\n')
                f.write(str(timestamp) + '\n')
            return True, None
        else:
            raise ValueError(f"Invalid get_type: {get_type}")

    except Exception as e:
        logger.error(f"Failed to set vote of player {player_name} in game {game_name}: {repr(e)}")
        return False, repr(e)