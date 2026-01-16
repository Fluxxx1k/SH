import os
import json
from datetime import datetime

from flask import request, redirect, session, jsonify

import user_settings
from WebsiteEasiest.data.database_py.games import get_data_of_game
from WebsiteEasiest.old.webplayers.web_game import WebPlayer
from Website_featetures.error_handler.safe_functions import *
from Website_featetures.error_handler.undefined import SilentUndefined
from WebsiteEasiest.data.database_work import exists_player, create_player, login_player
from core.globalstorage import GlobalStorage
from app_globs import app



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
    game_file = os.path.join('../data', 'games', f'{game_name}.json')
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