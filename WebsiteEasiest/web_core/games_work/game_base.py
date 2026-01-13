import os
from datetime import datetime

from flask import redirect, session, abort, request, jsonify

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.app_globs import socketio
from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game

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
    
    # Broadcast vote to all clients
    socketio.emit('vote_update', {
        'voter': vote_data['voter'],
        'type': vote_data['vote_type'],
        'target': vote_data.get('target_player')
    }, room=game_name)
    
    return {'success': True}



def game_start(game_name):
    print(f'game_start ({game_name})  |  {"not logged in" if "username" not in session else session["username"]}')
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    game = get_data_of_game(game_name)
    if not game[0]:
        return jsonify({'success': False, 'message': f'Game {game_name} not found: {game[1]}'}), 404
    else:
        game_data = game[1]
    # Load game data
    if game_data['status'] == 'started':
        return jsonify({'success': False, 'message': 'Game already started'}), 400
    if game_data['current_players'] < game_data['min_players']:
        return jsonify({'success': False, 'message': 'Not enough players'}), 400
    # Load game data
    game_file = os.path.join('data', 'games', f'{game_name}.json')
    if not os.path.exists(game_file):
        return jsonify({'success': False, 'message': 'Game not found in server files'}), 404


    # Check if user is the creator
    if game_data['created_by'] != session['username']:
        return jsonify({'success': False, 'message': 'Only game creator can start the game'}), 403

    roles = get_roles(game_data['current_players'])
    players = [WebPlayer(i, game_data['players'], roles[i]) for i in range(len(game_data['players']))]
    from webplayers.web_game import WebGame
    import threading
    
    def run_game():
        game = WebGame(game_name, players)
        WebGame.globs = GlobalStorage(game_name,
                                    roles=roles[0],
                                    players=players,
                                    count_players=game_data['current_players'],
                                    )
        while game.take_move() != 0:
            continue

    # Start game in separate thread
    game_thread = threading.Thread(target=run_game)
    game_thread.daemon = True
    game_thread.start()

    # Update game status
    game_data['status'] = 'started'
    with open(game_file, 'w', encoding='utf-8') as f:
        json.dump(game_data, f)

    return jsonify({'success': True, 'message': 'Game started'})