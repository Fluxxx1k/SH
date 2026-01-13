import json
import os

from flask import session, redirect, request, abort

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.website_settings import MIN_PLAYER_NUM, VOTE_ANONYMOUS, VETO_NUM_BLACK, ANARCHY_SKIP_NUM, \
    BLACK_WIN_NUM, RED_WIN_NUM
from WebsiteEasiest.stardard_renders import render_error_page


def create_game():
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    from WebsiteEasiest.settings.website_settings import (
        MAX_PLAYER_NUM,
        TIME_FORMAT,
        DATE_FORMAT
    )
    return render_template_abort_500('create_game.html', username=session['username'], min_players=MIN_PLAYER_NUM,
        max_players=MAX_PLAYER_NUM,
        date_format=DATE_FORMAT, time_format=TIME_FORMAT,
        vote_delay=30)




def create_game_post():
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    from WebsiteEasiest.settings.website_settings import (
        MAX_PLAYER_NUM,
        TIME_FORMAT,
        DATE_FORMAT
    )
    game_name = request.form.get('game_name')
    if not game_name:
        logger.debug(f'Invalid input for game creation: The game name is empty.')
        return render_error_page(400,
                                 f'Invalid input',
                                 "The game name is empty.",
                                 error_comment='You must enter a game name.',
                                 debug_info=repr(game_name),
                                 suggestion='Check your input values')

    game_password = request.form.get('game_password', '')
    max_players = int(request.form.get('max_players', 0))
    if max_players < MIN_PLAYER_NUM:
        logger.debug(f'Invalid input for game creation: The maximum number of players is less than the minimum of possible number of players.')
        return render_error_page(400,
                                 f'Invalid input',
                                 "The maximum number of players is less than the minimum of possible number of players.",
                                 error_comment='You must enter a number of players greater than or equal to the minimum of possible number of players.',
                                 debug_info=repr(max_players),
                                 suggestion='Check your input values')
    if max_players > MAX_PLAYER_NUM:
        logger.debug(f'Invalid input for game creation: The maximum number of players is greater than the maximum of possible number of players.')
        return render_error_page(400,
                                 f'Invalid input',
                                 "The maximum number of players is greater than the maximum of possible number of players.",
                                 error_comment='You must enter a number of players less than or equal to the maximum of possible number of players.',
                                 debug_info=repr(max_players),
                                 suggestion='Check your input values')

    # Create game data
    try:
        game_data = {
            'name': game_name,
            'current_players': 1,
            'status': 'waiting',
            'password': game_password,
            'created_by': session['username'],
            'players': [session['username']],
            'settings': {
                'max_players': max_players,
                'red_win_num': RED_WIN_NUM,
                'black_win_num': BLACK_WIN_NUM,
                'anarchy_skip_num': ANARCHY_SKIP_NUM,
                'date_format': request.form.get('date_format', DATE_FORMAT),
                'time_format': request.form.get('time_format', TIME_FORMAT),
                'vote_anonymous': VOTE_ANONYMOUS,
                'veto_num_black': VETO_NUM_BLACK,
                'vote_delay': int(request.form.get('vote_delay', 30))
            }
        }
    except ValueError as e:
        logger.warning(f'Invalid input for game creation: {repr(e)}')
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