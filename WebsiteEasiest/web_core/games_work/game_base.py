import pprint
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
    # Load game data
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    if game_name not in player_data.get('game_access', []) and game_data.get('password'):
        return redirect(f'/game/{game_name}/password')

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


    if session['username'] not in game_data['players']:
        game_data['players'].append(session['username'])
        game_data['current_players'] += 1

        # Update player data
        player_data['game'] = game_name
        save_data_of_player(session['username'], player_data)

        save_data_of_game(game_name, game_data)
        logger.info(f"Игрок {session['username']} присоединился к игре {game_name}")
        return {'success': True, 'message': 'Вы успешно присоединились к игре'}
    else:
        game_data['players'].append(session['username'])
        game_data['current_players'] = len(game_data['players'])
        save_data_of_game(game_name, game_data)
        logger.warning(f"Игрок {session['username']} пытался присоединиться к игре {game_name}, но уже присоединился")
        if player_data.get('game') == game_name:
            return {'success': False, 'message': 'Вы уже присоединились к этой игре по данным игрока и игры'}
        return {'success': False, 'message': 'Вы уже присоединились к этой игре по данным игры'}


def game_thread(game_name):
    wg_response = 0
    while wg_response == 0:
        wg_response = (game_name)

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
    print(player_data)
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


def game_verify_password(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(404, description="Имя игры не может быть пустым")
    
    data = request.get_json()
    if not data or 'password' not in data:
        return {'success': False, 'description': "Неверные данные запроса"}
    
    game_found, game_data = get_data_of_game(game_name)
    if not game_found:
        abort(404, description=f"Игра {game_name} не найдена: {game_data}")
    
    # Check if game has password and it matches
    logger.debug(f'User {repr(session["username"])} tries to log in in game {repr(game_name)} with password {repr(data["password"])} when the password is {repr(game_data.get("password"))}')
    if game_data.get('password') and game_data['password'] != data['password']:
        return {'success': False, 'message': 'Неверный пароль игры'}
    
    # Update player's game reference
    player_found, player_data = get_data_of_player(session['username'])
    if not player_found:
        abort(401, description=f"Игрок {session['username']} не найден: {player_data}")

    player_data['game_access'] = player_data.get('game_access', []) + [game_name]
    save_data_of_player(session['username'], player_data)

    return {'success': True, 'message': 'Пароль верный'}


def get_game_logs(game_name):
    count = request.args.get('count', default=0, type=int)
    if count < 0:
        logger.warning(f"Count is below zero: {count}, replacing with 0")
        count = 0
    logger.debug(f'User {repr(session.get("username"))} requests logs of game {repr(game_name)} with count {repr(count)}')
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
    if not isinstance(count, int):
        return {'success': False, 'message': f"Count must be an integer, not {type(count)}"}, 400
    predata = [ #{'cps': 'CPS',
                # 'ccs': 'CCS',
                # 'ccp': 'CCP',
                # 'cpsa': "CPSA",
                # 'prs': 'PRS',
                # 'cnc': "CNC",
                # 'special': 'No logs'}
                # for _ in range(10)
                ]
    x = {
        'success': True,
        'logs': game_data.get('logs', predata)[count:]
        }
    if x['logs'] == []:
        return {'success': False, 'message': "No new logs"}
    return x