from __future__ import annotations

import os, json, sys
from typing import Optional


def exists_player(name: str) -> bool:
    try:
        return os.path.exists(os.path.join('player', name + '.json'))
    except Exception as e:
        print(e)
        return True


def count_players() -> int:
    try:
        return len(os.listdir('players'))
    except Exception as e:
        print(e)
        return 0



def create_player(player_name: str, player_password: str) -> tuple[bool, Optional[str]]:
    try:
        if len(player_name) < 3:
            return False, repr(ValueError("Player name cannot be less than 3 characters"))
        if len(player_password) is None:
            return False, repr(ValueError("Player password cannot be empty"))
        if exists_player(player_name):
            return False, repr(FileExistsError(f'Player "{player_name}" already exists'))
        else:
            with open(os.path.join('players', player_name + '.json'), 'w') as f:
                json.dump({'player_name': player_name,
                           'player_password': player_password,
                           'in_game': ''
                           }, f, indent=4, ensure_ascii=False)
            return True, None
    except Exception as e:
        print(repr(e))
        return False, repr(e)

def get_data_for_player(player_name) -> tuple[bool, dict | str]:
    try:
        if exists_player(player_name):
            return True, json.load('players/' + player_name + '.json')
        else:
            return False, repr(FileNotFoundError(f'Player "{player_name}" not found'))
    except Exception as e:
        print(repr(e))
        return False, repr(e)
