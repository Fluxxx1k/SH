import os
from datetime import datetime

from flask import redirect, session, abort, request, jsonify

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game, exists_game
from WebsiteEasiest.data.database_py.players import get_data_for_player, save_data_of_player
from WebsiteEasiest.logger import logger

from WebsiteEasiest.settings.website_settings import get_roles

def game(game_name):
    if 'username' not in session:
        return redirect(safe_url_for('login'))

    # Load game data
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")

    # Get players list
    players = []
    for player_name in game_data['players']:
        players.append({
            'name': player_name,
            'role': 'creator' if player_name == game_data['created_by'] else 'participant',
        })

    return render_template_abort_500('game.html',
                                     created_by=game_data['created_by'],
                                     game_name=game_name,
                                     players=players,
                                     is_game_started=game_data['status'] == 'started',
                                     votes=game_data.get('votes', []))


def game_post(game_name):
    if 'username' not in session:
        return redirect(safe_url_for('login'))
        # Load game data
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")

    abort(405, description=f"POST запрос на игру {game_name} не реализован")
    return {'success': False, 'message': 'Not implemented yet'}



def game_vote(game_name):
    if 'username' not in session:
        return redirect(safe_url_for('login'))
        # Load game data
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")

    # Handle voting request
    vote_data = request.get_json()
    if 'voter' not in vote_data or 'vote_type' not in vote_data:
        return {'success': False, 'message': 'Invalid vote data'}

    # Store vote in game data
    if 'votes' not in game_data:
        game_data['votes'] = {}

    game_data['votes'][vote_data['voter']] = {
        'type': vote_data['vote_type'],
        'target': vote_data.get('target_player'),
        'timestamp': datetime.now().isoformat()
    }
    save_data_of_game(game_name, game_data)

    return {'success': True, 'message': "Vote registered"}



def game_join(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(404, description="Имя игры не может быть пустым")
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    if game_data['status'] == 'started':
        abort(403, description=f"Игра {game_name} уже не начата")
    player_found, player_data = get_data_for_player(session['username'])
    if not player_found:
        abort(404, description=f"Игрок {session['username']} не найден: {player_data}")
    if player_data['game'] != game_name:
        abort(403, description=f"Игрок {session['username']} уже присоединился к другой игре: {player_data['game']}")
    # Add player to game data
    if 'players' not in game_data:
        game_data['players'] = []
    if session['username'] not in game_data['players']:
        game_data['players'].append(session['username'])
        game_data['current_players'] += 1
        save_data_of_game(game_name, game_data)
        logger.info(f"Игрок {session['username']} присоединился к игре {game_name}")
        return {'success': True, 'message': 'Connected to game room'}
    else:
        return {'success': False, 'message': 'You are already connected to this game room'}

def game_leave():
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    player_found, player_data = get_data_for_player(session['username'])
    if not player_found:
        abort(404, description=f"Игрок {session['username']} не найден: {player_data}")
    # Remove player from game data
    if 'game' not in player_data or player_data['game'] == '':
        abort(403, description=f"Игрок {session['username']} не присоединился к какой-либо игре: {player_data['game']}")
    game_name = player_data['game']
    game_found, game_data = get_data_of_game(game_name)
    player_data['game'] = ''
    save_data_of_player(session['username'], player_data)
    if game_found and 'players' in game_data and session['username'] in game_data['players']:
        game_data['players'].remove(session['username'])
        save_data_of_game(game_name, game_data)
        return {'success': True, 'message': 'Disconnected from game room'}
    else:
        logger.warning(f"Игрок {session['username']} пытался отключиться от игры {game_name}, но {'он не был присоединен к этой игре' if game_found else f'что-то пошло не так: {game_data}'}")
        return {'success': True, 'message': 'Disconnected from game room, but it\'s don\'t exist'}

