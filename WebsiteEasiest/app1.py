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

# @app.route('/create_game', methods=['GET', 'POST'])







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