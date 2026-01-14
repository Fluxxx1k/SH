from __future__ import annotations

import os, json
from typing import Optional

from flask import request

from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import denied_literals

path_players = os.path.join(os.path.basename(os.path.basename(__file__)), 'data', 'players')
path_IP = os.path.join(os.path.basename(os.path.basename(__file__)), 'data', 'success_IP')
os.makedirs(path_players, exist_ok=True)
os.makedirs(path_IP, exist_ok=True)

def exists_player(name: str, default_on_error: bool = True) -> bool:
    logger.debug(f"Checking if player {repr(name)} exists")
    try:
        return os.path.exists(os.path.join(path_players, name + '.json'))
    except Exception as e:
        logger.error(f"Error checking if player {repr(name)} exists: {repr(e)}, return default_on_error={default_on_error}")
        return default_on_error


def count_players(default_on_error: int = 0) -> int:
    logger.debug("Counting players")
    try:
        return len(os.listdir(path_players))
    except Exception as e:
        logger.error(f"Error counting players: {repr(e)}, return default_on_error={default_on_error}")
        return default_on_error



def create_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    logger.debug(f"Creating player {repr(player_name)} with password {repr(player_password)}")
    try:
        if len(player_name) < 3:
            return False, repr(ValueError("Player name cannot be less than 3 characters"))
        if len(player_password) < 3:
            return False, repr(ValueError("Player password cannot be less than 3 characters"))
        if any(char in player_name for char in denied_literals):
            return False, repr(ValueError(f"Player name cannot contain any of the following characters: {denied_literals}"))
        if exists_player(player_name):
            return False, repr(FileExistsError(f'Player "{player_name}" already exists'))
        else:
            save_ip(player_name, creator=True)
            with open(os.path.join(path_players, player_name + '.json'), 'w+') as f:
                json.dump({'player_name': player_name,
                           'player_password': player_password,
                           'game': ''
                           }, f, indent=4, ensure_ascii=False)
            return True, None
    except Exception as e:
        logger.error(f"Error creating player {repr(player_name)} with password {repr(player_password)}: {repr(e)}")
        return False, repr(e)

def get_data_for_player(player_name) -> tuple[bool, dict | str]:
    logger.debug(f"Getting data for player {repr(player_name)}")
    try:
        if exists_player(player_name):
            return True, json.load(open(os.path.join(path_players, player_name + '.json'), encoding='utf-8'))
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
                if data[1]['player_password'] == player_password:
                    save_ip(player_name)
                    return True, None
                else:
                    save_ip(player_name, success=False)
                    return False, repr(ValueError("Player password is incorrect"))
            else:
                return False, data[1]
    except Exception as e:
        print(repr(e))
        return False, repr(e)


def save_ip(player_name, success=True, creator=False):
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    try:
        with open(os.path.join(path_IP, player_name + '.json'), 'r') as f:
            ip_data = json.load(f)
            if creator:
                if real_ip not in ip_data['creator_IP']:
                    ip_data['creator_IP'].append(real_ip)
                    with open(os.path.join(path_IP, player_name + '.json'), 'w+') as f:
                        json.dump(ip_data, f, indent=4, ensure_ascii=False)
            else:
                if success:
                    if real_ip not in ip_data['success_IP']:
                        ip_data['success_IP'].append(real_ip)
                        with open(os.path.join(path_IP, player_name + '.json'), 'w+') as f:
                            json.dump(ip_data, f, indent=4, ensure_ascii=False)
                else:
                    if real_ip not in ip_data['fail_IP']:
                        ip_data['fail_IP'].append(real_ip)
                        with open(os.path.join(path_IP, player_name + '.json'), 'w+') as f:
                            json.dump(ip_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Error logging player's ({repr(player_name)}) IP {repr(real_ip)}: {repr(e)}")
