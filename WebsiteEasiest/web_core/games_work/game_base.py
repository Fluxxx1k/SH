import os
from datetime import datetime

from flask import redirect, session, abort, request

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.data.database_py.games import get_data_of_game, save_data_of_game


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
        game_data['votes'] = []
    game_data['votes'].append({
        'voter': vote_data['voter'],
        'type': vote_data['vote_type'],
        'target': vote_data.get('target_player'),
        'timestamp': datetime.now().isoformat()
    })
    save_data_of_game(game_name, game_data)
    return {'success': True}
