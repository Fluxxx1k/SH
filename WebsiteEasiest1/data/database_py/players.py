from __future__ import annotations

import os, json, sys
from typing import Optional


def exists_player(name: str) -> bool:
    print(f"Checking if player {name} exists")
    try:
        return os.path.exists(os.path.join('data', 'players', name + '.json'))
    except Exception as e:
        print(e)
        return True


def count_players() -> int:
    print("Counting players")
    try:
        return len(os.listdir(os.path.join('data', 'players')))
    except Exception as e:
        print(e)
        return 0



def create_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    print(f"Creating player {player_name} with password {player_password}")
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
                           'in_game': ''
                           }, f, indent=4, ensure_ascii=False)
            return True, None
    except Exception as e:
        print(repr(e))
        return False, repr(e)

def get_data_for_player(player_name) -> tuple[bool, dict | str]:
    print(f"Getting data for player {player_name}")
    try:
        if exists_player(player_name):
            return True, json.load(open(os.path.join('data', 'players', player_name + '.json'), encoding='utf-8'))
        else:
            return False, repr(FileNotFoundError(f'Player "{player_name}" not found'))
    except Exception as e:
        print(repr(e))
        return False, repr(e)

def login_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    print(f"Logging in player {player_name} with password {player_password}")
    try:
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
