from __future__ import annotations

import json
import pickle
import os, sys
import re
from typing import Any, Generator

from web_logger import error_log
from server_settings import MIN_PLAYER_NUM


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
        with open(f'{game_data_dir}/{game_name}.json', 'r', encoding='utf-8') as file:
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


def verify_game(game_name: str, password: str, player_name:str) -> tuple[bool, str]:
    game_data = find_game_data(game_name)
    if isinstance(game_data, FileNotFoundError):
        return False, "Game not found"
    if isinstance(game_data, Exception):
        return False, repr(game_data)

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


def get_games_list() -> Generator[tuple[str, int, int, str, bool]]:
    for file in (temp := os.listdir(game_data_dir)):
        if file.endswith(".json"):
            # print(f"{file= }")
            game_name = file[:-5]  # Remove .json extension
            game_data = find_game_data(game_name)
            if not isinstance(game_data, Exception):
                current_players = len(game_data.get('players', []))
                max_players = game_data.get('max_players', MIN_PLAYER_NUM)
                status = game_data.get('status', 'waiting')
                has_password = bool(game_data.get('password', ''))
                yield (game_name, current_players, max_players, status, has_password)
    # print(f"{temp= }")

def get_complete_games_count() -> int:
    count = 0
    for file in os.listdir(game_data_dir_end):
        if file.endswith(".json"):
            count += 1
        else:
            error_log(f"File {file} in {game_data_dir_end} is not a json file")
    return count

def get_games_count() -> int:
    count = 0
    for file in os.listdir(game_data_dir):
        if file.endswith(".json"):
            count += 1
        else:
            error_log(f"File {file} in {game_data_dir} is not a json file")
    return count
def get_players_count() -> int:
    count = 0
    for file in os.listdir(player_data_dir):
        if file.endswith(".json"):
            count += 1
        else:
            error_log(f"File {file} in {player_data_dir} is not a json file")
    return count
def get_players_list() -> Generator[str]:
    for file in os.listdir(player_data_dir):
        if file.endswith(".json"):
            yield file[:-5]  # Remove .json extension
        else:
            error_log(f"File {file} in {player_data_dir} is not a json file")
