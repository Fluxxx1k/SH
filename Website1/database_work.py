from __future__ import annotations

import json
import pickle
import os, sys
import re
from typing import Any, Generator

from Website1.web_logger import error_log


game_data_dir = "data/game_data"
if not os.path.exists(game_data_dir):
    os.makedirs(game_data_dir)
game_data_dir_end = "data/game_data_end"
if not os.path.exists(game_data_dir_end):
    os.makedirs(game_data_dir_end)

player_data_dir = "data/player_data"
if not os.path.exists(player_data_dir):
    os.makedirs(player_data_dir)

cashed_games = []


def find_game_data(game_name: str) -> dict[str, Any] | Exception:
    try:
        with open(f'{game_data_dir}{game_name}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        error_log(e, f"opening {game_data_dir}/{game_name}.json")
        return e
    except json.JSONDecodeError as e:
        error_log(e, f"opening {game_data_dir}/{game_name}.json")
        return e
    except Exception as e:
        error_log(e, f"opening {game_data_dir}/{game_name}.json")
        return e


def find_player_data(player_name: str) -> dict[str, Any] | Exception:
    try:
        with open(f'{player_data_dir}/{player_name}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        error_log(e, f"opening {player_data_dir}/{player_name}.json")
        return e
    except json.JSONDecodeError as e:
        error_log(e, f"opening {player_data_dir}/{player_name}.json")
        return e
    except Exception as e:
        error_log(e, f"opening {player_data_dir}/{player_name}.json")
        return e


def save_player_data(player_name: str, data: dict) -> Exception | None:
    try:
        with open(f'{player_data_dir}/{player_name}.json', 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return None
    except Exception as e:
        error_log(e, f"opening {player_data_dir}/{player_name}.json")
        return e

def save_game_data(game_name: str, data: dict) -> Exception | None:
    try:
        with open(f'{game_data_dir}/{game_name}.json', 'w+', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return None
    except Exception as e:
        error_log(e, f"opening {game_data_dir}/{game_name}.json")
        return e

def verify_player(player_name: str, password: str) -> tuple[bool, str]:
    player_data = find_player_data(player_name)
    if isinstance(player_data, FileNotFoundError):
        return False, "Player not found"
    if isinstance(player_data, Exception):
        return False, repr(player_data)
    if player_data.get("password") == password:
        return True, "Successfully verified"
    else:
        return False, "Incorrect password"


def create_player(player_name: str, password: str) -> Exception | None:
    if os.path.exists(f'{player_data_dir}/{player_name}.json'):
        return FileExistsError(f"Player {player_name} already exists")
    try:
        with open(f'{player_data_dir}/{player_name}.json', 'w+', encoding='utf-8') as file:
            json.dump({'password': password,
                       'games': {
                                "head":[],
                                "participant":[]
                                }
                       },
                      file, ensure_ascii=False, indent=4)
            return None
    except Exception as e:
        error_log(e, f"opening {player_data_dir}/{player_name}.json")
        return e


def verify_game(game_name: str, password: str, player_name:str, player_password: str) -> tuple[bool, str]:
    game_data = find_game_data(game_name)
    if isinstance(game_data, FileNotFoundError):
        return False, "Game not found"
    if isinstance(game_data, Exception):
        return False, repr(game_data)
    verifying_player = verify_player(player_name, player_password)
    if not verifying_player[0]:
        return verifying_player
    if game_data.get("password") == password:
        if player_name not in game_data.get("players"):
            game_data['players'].append(player_name)
            save_game_data(game_name, game_data)
        return True, "Successfully verified"
    return False, "Incorrect password"

def create_game(game_name: str, game_data: dict, player_name: str) -> Exception | None:
    if os.path.exists(f'{game_data_dir}/{game_name}.json'):
        return FileExistsError(f"Game {game_name} already exists")
    if not os.path.exists(f'{player_data_dir}/{player_name}.json'):
        return FileNotFoundError(f"Player {player_name} not found")
    game_data['players'] = [player_name]
    try:
        with open(f'{game_data_dir}/{game_name}.json', 'w+', encoding='utf-8') as file:
            json.dump(game_data, file, ensure_ascii=False, indent=4)
            return None
    except Exception as e:
        error_log(e, f"opening {game_data_dir}/{game_name}.json")
        return e


def get_games_list() -> Generator[tuple[str, int]]:
    for file in os.listdir(game_data_dir):
        if file.endswith(".json"):
            yield file[len(game_data_dir):-5], len(find_game_data(file[len(game_data_dir):-5])['players'])

    