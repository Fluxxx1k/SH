from __future__ import annotations

import os, json, sys
from typing import Optional

from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import denied_literals


def exists_player(name: str) -> bool:
    logger.debug(f"Checking if player {repr(name)} exists")
    try:
        return os.path.exists(os.path.join('data', 'players', name + '.json'))
    except Exception as e:
        print(e)
        return True


def count_players() -> int:
    logger.debug("Counting players")
    try:
        return len(os.listdir(os.path.join('data', 'players')))
    except Exception as e:
        print(e)
        return 0



def create_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    logger.debug(f"Creating player {repr(player_name)} with password {repr(player_password)}")
    try:
        if len(player_name) < 3:
            return False, repr(ValueError("Player name cannot be less than 3 characters"))
        if len(player_password) is None:
            return False, repr(ValueError("Player password cannot be empty"))
        if exists_player(player_name):
            return False, repr(FileExistsError(f'Player "{player_name}" already exists'))
        else:
            with open(os.path.join('data', 'players', player_name + '.json'), 'w+') as f:
                json.dump({'player_name': player_name,
                           'player_password': player_password,
                           'game': ''
                           }, f, indent=4, ensure_ascii=False)
            return True, None
    except Exception as e:
        print(repr(e))
        return False, repr(e)

def get_data_for_player(player_name) -> tuple[bool, dict | str]:
    logger.debug(f"Getting data for player {repr(player_name)}")
    try:
        if exists_player(player_name):
            return True, json.load(open(os.path.join('data', 'players', player_name + '.json'), encoding='utf-8'))
        else:
            return False, repr(FileNotFoundError(f'Player "{player_name}" not found'))
    except Exception as e:
        print(repr(e))
        return False, repr(e)

def login_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    logger.debug(f"Logging in player {repr(player_name)} with password {repr(player_password)}")
    '''
    Logs in a player with the given name and password.

    Args:
        player_name (str): The name of the player.
        player_password (str): The password of the player.

    Returns:
        tuple[bool, Optional[str]]: A tuple containing a boolean indicating whether the login was successful,
        and an optional error message.
    '''
    try:
        if len(player_name) < 3:
            return False, repr(ValueError("Player name cannot be less than 3 characters"))
        if any(char in player_password for char in denied_literals):
            return False, repr(ValueError("Player password cannot contain denied characters"))
        if not exists_player(player_name):
            return False, repr(FileNotFoundError(f'Player "{player_name}" not found'))
        else:
            data = get_data_for_player(player_name)
            if data[0]:
                print(data[1])
                if data[1]['player_password'] == player_password:
                    return True, None
                else:
                    return False, repr(ValueError("Player password is incorrect"))
            else:
                return False, data[1]
    except Exception as e:
        print(repr(e))
        return False, repr(e)
