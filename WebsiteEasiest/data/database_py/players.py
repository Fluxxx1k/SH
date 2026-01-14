from __future__ import annotations

import os, json
from typing import Optional

from flask import request

from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import denied_literals
path_players = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'players')
path_IP = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'IP')
os.makedirs(path_players, exist_ok=True)
os.makedirs(path_IP, exist_ok=True)
print(path_IP)

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
            with open(os.path.join(path_players, player_name + '.json'), 'w+') as f:
                json.dump({'player_name': player_name,
                           'player_password': player_password,
                           'game': ''
                           }, f, indent=4, ensure_ascii=False)
            save_ip(player_name, creator=True)
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


def save_ip(player_name: str, success:bool =None, creator: bool=False, spec:str=''):
    try:
        real_ip = spec+request.headers.get('X-Forwarded-For', request.remote_addr)
        path_ip_for_player = os.path.join(path_IP, player_name + '.json')
        if creator:
            logger.debug(f"Saving creator's IP ({real_ip}) for player {repr(player_name)}")
            if os.path.exists(path_ip_for_player):
                logger.warning('Trying to rewrite creator\'s IP!')
                save_ip(player_name, spec='RC: ')
            ip_data = {'creator_IP': real_ip,
                       'last_IP': real_ip,
                       'success_IP': [real_ip]}
            with open(path_ip_for_player, 'w+') as f:
                json.dump(ip_data, f, indent=4, ensure_ascii=False)
        else:
            with open(path_ip_for_player, 'r') as f:
                ip_data = json.load(f)
                if success is True:
                    logger.debug(f"Saving last IP ({real_ip}) for player {repr(player_name)}")
                    ip_data['last_IP'] = real_ip
                    logger.debug(f"Saving IP of player {player_name} with successful login")
                    ip_data['success_IP'] = ip_data.get('success_IP', [])
                    if real_ip not in ip_data['success_IP']:
                        ip_data['success_IP'].append(real_ip)
                        with open(path_ip_for_player, 'w') as f:
                            json.dump(ip_data, f, indent=4, ensure_ascii=False)
                elif success is False:
                    logger.debug(f"Saving IP of player {player_name} with failed login")
                    ip_data['fail_IP'] = ip_data.get('fail_IP', [])
                    if real_ip not in ip_data['fail_IP']:
                        ip_data['fail_IP'].append(real_ip)
                        with open(path_ip_for_player, 'w') as f:
                            json.dump(ip_data, f, indent=4, ensure_ascii=False)
                else:
                    logger.debug(f"Saving IP of player {player_name} with unknown status login")
                    ip_data['unknown_IP'] = ip_data.get('unknown_IP', [])
                    if real_ip not in ip_data['unknown_IP']:
                        ip_data['unknown_IP'].append(real_ip)
                        with open(path_ip_for_player, 'w+') as f:
                            json.dump(ip_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        try:
            logger.warning(f"Error logging player's ({repr(player_name)}) IP {repr(real_ip)}: {repr(e)}")
        except Exception as e2:
            logger.error(f"Error logging player's ({repr(player_name)}) IP: {repr(e)} {repr(e2)}")
    else:
        logger.info(f"Saved player's ({repr(player_name)}) IP {repr(real_ip)}")