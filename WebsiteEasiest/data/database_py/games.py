from __future__ import annotations

import os, json, sys
from typing import Optional


def count_games() -> int:
    try:
        return len(os.listdir('games'))
    except Exception as e:
        print(repr(e))
        return 0

def exists_game(game_name: str) -> bool:
    return os.path.exists(os.path.join('games', game_name+'.json'))

def existed_game(game_name: str) -> bool:
    return os.path.exists(os.path.join('ended_games', game_name+'.json'))


def deep_check_exists_game(game_name: str) -> bool:
    try:
        exists = exists_game(game_name)
    except Exception as e:
        print(repr(e))
        exists = True
    try:
        existed = existed_game(game_name)
    except Exception as e:
        print(repr(e))
        existed = True
    return exists or existed



def find_game(game_name: str) -> tuple[bool, dict | str]:
    try:
        if exists_game(game_name):
            return True, json.load(open(os.path.join('games', game_name + '.json'), encoding='utf-8'))
        else:
            return False, repr(FileNotFoundError(f'Game "{game_name}" not found'))
    except Exception as e:
        print(repr(e))
        return False, repr(e)


def save_data_of_game(game_name: str, game_data: dict) -> None:
    if exists_game(game_name):
        with open(os.path.join('games', game_name + '.json'), 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=4, ensure_ascii=False)
    else:
        print('Game not found')

def create_game(game_name: str, creator: str, password: str=None) -> tuple[bool, Optional[str]]:
    try:
        if len(game_name) < 3:
            return False, repr(ValueError('Game name cannot be less than 3 characters'))
        if password == '':
            password = None
        if deep_check_exists_game(game_name):
            print('Game already exists')
            return False, repr(FileExistsError(f'Game "{game_name}" already exists'))
        else:
            open(os.path.join('games', game_name + '.json'), 'w+').close()
            save_data_of_game(game_name, {
                'game_name': game_name,
                'password': password,
                'creator': creator,
                'players': [creator],
            })
        return True, None
    except Exception as e:
        print(repr(e))
        return False, repr(e)


def end_game(game_name: str, game_data: dict = None) -> tuple[bool, Optional[str]]:
    try:
        if game_data is not None:
            save_data_of_game(game_name, game_data)
        os.replace(os.path.join('games', game_name + '.json'), os.path.join('ended_games', game_name + '.json'))
        return True, None
    except FileExistsError as e:
        return False, f'Game "{game_name}" already existed, data will be lost: {repr(e)}'
    except Exception as e:
        return False, repr(e)

