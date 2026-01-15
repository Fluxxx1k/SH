import os

from flask import session, redirect, abort

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import render_template_abort_500
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for
from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game, end_game_db
from WebsiteEasiest.data.data_paths import path_games
from WebsiteEasiest.data.database_py.players import save_data_of_player, get_data_of_player, add_game_to_player
from WebsiteEasiest.logger import logger


def game_leave():
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(404, description=f"Игрок {session['username']} не найден: {player_data}")
    # Remove player from game data
    if 'game' not in player_data or player_data['game'] == '':
        return {'success': False, 'message': 'Player not in any game'}
    game_name = player_data['game']
    game_found, game_data = get_data_of_game(game_name)
    if game_data.get('status', '') == 'playing':
        abort(403, description="Нельзя покинуть игру, пока она идет")

    if game_found:
        if game_data.get('created_by', '') == session['username']:
            abort(403, description="Нельзя покинуть игру, если вы её создали")
        elif 'players' in game_data and session['username'] in game_data['players']:
            game_data['players'].remove(session['username'])
            game_data['current_players'] -= 1
            if game_data['current_players'] == 0:
                end_game_db(game_name)
            save_data_of_game(game_name, game_data)
            add_game_to_player(session['username'], '')
            return {'success': True, 'message': 'Disconnected from game room'}
        else:
            logger.warning(f"Игрок {session['username']} пытался отключиться от игры {game_name}, но он не был присоединен к этой игре")
            add_game_to_player(session['username'], '')
            return {'success': True, 'message': 'Player not in game'}
    else:
        add_game_to_player(session['username'], '')
        logger.warning(f"Игрок {session['username']} пытался отключиться от игры {game_name}, но что-то пошло не так: {game_data}")
        return {'success': True, 'message': 'Disconnected from game room, but it\'s don\'t exist'}


def lobby():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Load available games
    games = []
    for file in os.listdir(path_games):
        if file.endswith('.json'):
            game_name = file[:-5]
            game_found, game_data = get_data_of_game(game_name)
            if game_found:
                print(game_data)
                games.append({
                    'name': game_name,
                    'players': game_data.get('players', ['DATA_LOST_PLAYERS']),
                    'max_players': game_data.get('settings', {}).get('max_players', 0),
                    'status': game_data.get('status', 'DATA_LOST_STATUS'),
                    'creator': game_data.get('created_by', 'DATA_LOST_CREATOR'),
                    'current_players': game_data.get('current_players', 0),
                })

    return render_template_abort_500('lobby.html', username=session['username'], games=games)