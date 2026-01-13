import os

from flask import session, redirect

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import render_template_abort_500
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for
from WebsiteEasiest.data.database_py.games import get_data_of_game


def lobby():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Load available games
    games = []
    games_dir = os.path.join('data', 'games')
    for file in os.listdir(games_dir):
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

