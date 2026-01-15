import os
from datetime import datetime

from flask import redirect, session, abort, request

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game, exists_game, end_game_db
from WebsiteEasiest.data.database_py.players import get_data_of_player, save_data_of_player
from WebsiteEasiest.logger import logger

def game(game_name):
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    # Load player data
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:

        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")
    print('game_name', game_name)
    print('player_data', player_data)
    if game_name != player_data['game']:
        return redirect(f'/game/{game_name}/password')

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
                                     is_game_started=game_data['status'] == 'playing',
                                     votes=game_data.get('votes', []),
                                     in_game= session['username'] in game_data['players'])


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
        return {'success': False, 'message': 'Игра уже начата'}
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")
    if player_data.get('game') == game_name:
        return {'success': False, 'message': 'Вы уже присоединились к этой игре'}

    # Add player to game data
    if 'players' not in game_data:
        game_data['players'] = []

    if session['username'] not in game_data['players']:
        game_data['players'].append(session['username'])
        game_data['current_players'] += 1

        # Update player data
        player_data['game'] = game_name
        save_data_of_player(session['username'], player_data)

        save_data_of_game(game_name, game_data)
        logger.info(f"Игрок {session['username']} присоединился к игре {game_name}")
        return {'success': True, 'message': 'Вы успешно присоединились к игре'}

    return {'success': False, 'message': 'Вы уже присоединились к этой игре'}





def game_start(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(404, description="Имя игры не может быть пустым")
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    if game_data['status'] == 'playing':
        return {'success': False, 'message': 'Игра уже начата'}
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")
    if player_data.get('game') != game_name:
        abort(403, description=f"Игрок {session['username']} не присоединился к игре {game_name}")
    if game_data['created_by'] != session['username']:
        abort(403, description=f"Игрок {session['username']} не является создателем игры {game_name}")
    game_data['status'] = 'playing'
    save_data_of_game(game_name, game_data)
    return {'success': True, 'message': 'Игра успешно начата'}

def game_end(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(404, description="Имя игры не может быть пустым")
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")
    if game_data['created_by'] != session['username']:
        abort(403, description=f"Игрок {session['username']} не является создателем игры {game_name}")
    game_data['status'] = 'ended'
    end_game_db(game_name, game_data)
    return {'success': True, 'message': 'Игра успешно завершена'}


def game_password(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(404, description="Имя игры не может быть пустым")
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")
    return render_template_abort_500('game_password.html', game_name=game_name)
