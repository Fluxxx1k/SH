import os
import json
from datetime import datetime
from typing import Iterable, Literal

from flask import Flask, request, redirect, session, jsonify

import user_settings
from WebsiteEasiest.data.database_py.games import count_games, get_data_of_game
from WebsiteEasiest.data.database_py.players import count_players
from WebsiteEasiest.webplayers.web_game import WebPlayer
from Website_featetures.error_handler.safe_functions import *
from Website_featetures.error_handler.undefined import SilentUndefined
from WebsiteEasiest.data.database_work import exists_player, create_player, login_player
from core.globalstorage import GlobalStorage
from core.players.abstract_player import AbstractPlayer
from cli.colors import RED_TEXT_BRIGHT, GREEN_TEXT_BRIGHT, RESET_TEXT, YELLOW_TEXT, YELLOW_TEXT_BRIGHT, GREEN_TEXT
from app_globs import app



@app.route('/')
def index():
    print(f'index  |  {"not logged in" if "username" not in session else session["username"]}')
    stats = {'active_games': count_games(),
             'complete_games': count_games(active=False),
             'total_players': count_players(),
             }
    return render_template_abort_500('index.html', stats=stats)

@app.route('/login')
def login():
    print(f'login  |  {"not logged in" if "username" not in session else session["username"]}')
    return render_template_abort_500('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    print(f'login_post  |  {"not logged in" if "username" not in session else session["username"]}')
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        return render_error_page(400, logging_in_player[1])
    else:
        session['username'] = username
        return redirect(safe_url_for('lobby'))
@app.route('/register', methods=['POST'])
def register_post():
    print(f'register_post  |  {"not logged in" if "username" not in session else session["username"]}')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if exists_player(username):
        return render_error_page(400, 'Username already exists')
    if password != confirm_password:
        return render_error_page(400, 'Passwords do not match')
    if len(password) < 3:
        return render_error_page(400, 'Password must be at least 3 characters long')
    creating_player = create_player(username, password)
    if creating_player[0]:
        return redirect(safe_url_for('login'))
    else:
        return render_error_page(400, creating_player[1])
@app.route('/logout')
def logout():
    print(f'logout   |  {"not logged in" if "username" not in session else session["username"]}')
    return render_template_abort_500('logout.html')
@app.route('/register')
def register():
    print(f'register  |  {"not logged in" if "username" not in session else session["username"]}')
    return render_template_abort_500('register.html')
@app.route('/lobby')
def lobby():
    print(f'lobby  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # Load available games
    games = []
    games_dir = os.path.join('data', 'games')
    if os.path.exists(games_dir):
        for file in os.listdir(games_dir):
            if file.endswith('.json'):
                with open(os.path.join(games_dir, file), 'r') as f:
                    game_data = json.load(f)
                    games.append({
                        'name': game_data.get('name', file[:-5]),
                        'players': len(game_data.get('players', [])),
                        'max_players': game_data.get('max_players', 8),
                        'status': game_data.get('status', 'waiting')
                    })
    
    return render_template_abort_500('lobby.html', username=session['username'], games=games)

@app.route('/game/<game_name>')
def game(game_name):
    print(f'GAME {game_name}  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # Load game data
    game_file = os.path.join('data', 'games', f'{game_name}.json')
    if not os.path.exists(game_file):
        return render_template_abort_500('error.html', error_code=404, error_message="Игра не найдена"), 404
    
    with open(game_file, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    
    # Get players list
    players = []
    for player_name in game_data['players']:
        # player_file = os.path.join('data', 'players', f'{player_name}.json')
        # if os.path.exists(player_file):
        #     with open(player_file, 'r', encoding='utf-8') as f:
        #         player_data = json.load(f)
                players.append({
                    'name': player_name,
                    # 'role': player_data.get('role', 'unknown')
                    'role': 'creator' if player_name == game_data['created_by'] else 'participant',
                })
    
    return render_template_abort_500('game.html', created_by=game_data['created_by'], game_name=game_name,
                                     players=players, is_game_started=game_data['status'] == 'started')

@app.route('/game/<game_name>/ws')
def game_ws(game_name):
    print(f'game_ws ({game_name})  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        
        # Register player in WebSocket connections
        player_name = session['username']
        
        while True:
            try:
                message = ws.receive()
                if message is None:
                    break
                    
                data = json.loads(message)
                
                # Check if game exists before broadcasting
                if game_name not in games_dict:
                    return "Game not found", 404
                
                # Broadcast message to all players
                for player in games_dict[game_name].players:
                    if hasattr(player, 'ws') and player.ws:
                        player.ws.send(json.dumps({
                            'type': 'action',
                            'player': player_name,
                            'action': data.get('action'),
                            'time': datetime.now().strftime('%H:%M:%S')
                        }))
                
            except Exception as e:
                print(f"WebSocket error: {e}")
                break
        
        return ""
    
    return "WebSocket connection required", 400

@app.route('/game/<game_name>/vote', methods=['POST'])
def game_vote(game_name):
    print(f'game_vote ({game_name})  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    vote_type = request.json.get('vote')
    if vote_type not in ['yes', 'no', 'pass']:
        return jsonify({'success': False, 'message': 'Invalid vote type'}), 400

    if game_name not in games_dict:
        return jsonify({'success': False, 'message': 'Game not started or not exists'}), 404
    # Convert to numeric value (1=YES, -1=NO, 0=PASS)
    vote_value = 1 if vote_type == 'yes' else (-1 if vote_type == 'no' else 0)
    

    player = next((p for p in games_dict[game_name].players if p.name == session['username']), None)
    if not player:
        return jsonify({'success': False, 'message': 'Player not found'}), 404

    player.set_vote(vote_value)
    
    return jsonify({'success': True, 'message': 'Vote recorded'})

@app.route('/game/<game_name>/vote_player', methods=['POST'])
def game_vote_player(game_name):
    print(f'game_vote_player ({game_name})  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    player_id = request.json.get('player_id')
    if not player_id:
        return jsonify({'success': False, 'message': 'Player ID required'}), 400
    
    # Find player and set vote for specific player
    if game_name not in games_dict:
        return jsonify({'success': False, 'message': 'Game not started or not exists'}), 404
    player = next((p for p in games_dict[game_name].players if p.name == session['username']), None)
    if not player:
        return jsonify({'success': False, 'message': 'Player not found'}), 404
        
    player.set_action({'type': 'vote_player', 'player_id': player_id})
    
    return jsonify({'success': True, 'message': 'Player vote recorded'})

@app.route('/game/<game_name>/start', methods=['POST'])
def game_start(game_name):
    print(f'game_start ({game_name})  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    game = get_data_of_game(game_name)
    if not game[0]:
        return jsonify({'success': False, 'message': 'Game not found'}), 404
    else:
        game = game[1]
    if games_dict[game_name]['status'] == 'started':
        return jsonify({'success': False, 'message': 'Game already started'}), 400
    if games_dict[game_name]['current_players'] < games_dict[game_name]['min_players']:
        return jsonify({'success': False, 'message': 'Not enough players'}), 400
    # Load game data
    game_file = os.path.join('data', 'games', f'{game_name}.json')
    if not os.path.exists(game_file):
        return jsonify({'success': False, 'message': 'Game not found in server files'}), 404
    
    with open(game_file, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    
    # Check if user is the creator
    if game_data['created_by'] != session['username']:
        return jsonify({'success': False, 'message': 'Only game creator can start the game'}), 403

    roles = user_settings.get_roles(game_data['current_players'])
    players = [WebPlayer(i, game_data['players'], roles[i]) for i in range(len(game_data['players']))]
    from webplayers.web_game import WebGame
    games_dict[game_name] = WebGame(game_name, players)
    WebGame.globs = GlobalStorage(game_name,
                                  roles=roles[0],
                                  players=players,
                                  count_players=game_data['current_players'],
                                  )
    
    # Update game status
    game_data['status'] = 'started'
    with open(game_file, 'w', encoding='utf-8') as f:
        json.dump(game_data, f)
    
    return jsonify({'success': True, 'message': 'Game started'})

@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    print(f'create_game  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    from user_settings import (MIN_PLAYER_NUM,
                               MAX_PLAYER_NUM,
                               RED_WIN_NUM,
                               BLACK_WIN_NUM,
                               ANARCHY_SKIP_NUM,
                               DATE_FORMAT,
                               TIME_FORMAT,
                               VOTE_ANONYMOUS,
                               VETO_NUM_BLACK)
    if request.method == 'GET':
        default_players = min(MAX_PLAYER_NUM, 8)  # Default to 8 players if max is higher
        return render_template_abort_500('create_game.html', username=session['username'], min_players=MIN_PLAYER_NUM,
                                         max_players=MAX_PLAYER_NUM, default_players=default_players,
                                         red_win_num=RED_WIN_NUM, black_win_num=BLACK_WIN_NUM,
                                         anarchy_skip_num=ANARCHY_SKIP_NUM, date_format=DATE_FORMAT,
                                         time_format=TIME_FORMAT, vote_anonymous=VOTE_ANONYMOUS,
                                         veto_num_black=VETO_NUM_BLACK, vote_delay=30)
    
    # Handle POST request for game creation
    game_name = request.form.get('game_name')
    game_password = request.form.get('game_password', '')
    max_players = int(request.form.get('max_players', MIN_PLAYER_NUM))
    

    # Create game data
    try:
        game_data = {
            'name': game_name,
            'password': game_password,
            'max_players': max_players,
            'current_players': 1,
            'status': 'waiting',
            'created_by': session['username'],
            'players': [session['username']],
            'settings': {
                'red_win_num': int(request.form.get('red_win_num', 5)),
                'black_win_num': int(request.form.get('black_win_num', 6)),
                'anarchy_skip_num': int(request.form.get('anarchy_skip_num', 3)),
                'date_format': request.form.get('date_format', '%d.%m.%y'),
                'time_format': request.form.get('time_format', '%H:%M:%S'),
                'vote_anonymous': bool(request.form.get('vote_anonymous', False)),
                'veto_num_black': int(request.form.get('veto_num_black', 5)),
                'vote_delay': int(request.form.get('vote_delay', 30))
            }
        }
    except ValueError as e:
        return render_error_page(400,
                                 f'Invalid input',
                                 str(e),
                                 error_comment='This may mean that your input values are not integers or are out of range or like that.',
                                 debug_info=repr(e),
                                 suggestion='Check your input values')
    
    # Save game
    games_dir = os.path.join('data', 'games')
    os.makedirs(games_dir, exist_ok=True)
    with open(os.path.join(games_dir, f"{game_name}.json"), 'w') as f:
        json.dump(game_data, f)
    
    return redirect(safe_url_for('lobby'))







# Application-specific error handlers
def handle_game_error(error_message, error_code=400):
    """Handle games-specific errors"""
    return render_error_page(
        error_code=error_code,
        error_message="Ошибка в игре",
        error_description=error_message,
        error_comment="Проверьте правильность действий в игре.",
        suggestion="Попробуйте вернуться в лобби и начать заново."
    ), error_code


def handle_database_error(error_message):
    """Handle database errors"""
    return render_error_page(
        error_code=500,
        error_message="Ошибка базы данных",
        error_description="Произошла ошибка при работе с базой данных.",
        error_comment="Возможно, проблема с соединением или данными.",
        suggestion="Попробуйте обновить страницу. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=error_message if app.debug else None
    ), 500


if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    
    if app.debug:

        from gevent import monkey
        monkey.patch_all()
        from gevent.pywsgi import WSGIServer
        from geventwebsocket.handler import WebSocketHandler

        http_server = WSGIServer(('0.0.0.0', 5000),
                                 app,
                                 handler_class=WebSocketHandler,
                                 log=None)
        print("Running WebSocket server in debug mode on port 5000")
        http_server.serve_forever()
    else:
        server = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
        server.serve_forever()