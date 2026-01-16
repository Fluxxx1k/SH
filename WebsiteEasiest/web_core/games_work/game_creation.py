from flask import session, redirect, request

from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for, render_template_abort_500
from WebsiteEasiest.data.database_py.games import create_game_db
from WebsiteEasiest.data.database_py.players import add_game_to_player, get_data_of_player
from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import denied_literals
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
    return render_template_abort_500('create_game.html',
        username=session['username'],
        min_players=MIN_PLAYER_NUM,
        max_players=MAX_PLAYER_NUM,
        date_format=DATE_FORMAT, time_format=TIME_FORMAT,
        vote_delay=30)


def create_game_post():
    if 'username' not in session:
        return redirect(safe_url_for('login'))

    found_player, player_data = get_data_of_player(session['username'])
    if not found_player:
        logger.debug(f'Invalid input for game creation: The player {repr(session["username"])} is not found.')
        return render_error_page(400,
                                 f'Invalid input',
                                 f"The player {repr(session['username'])} is not found.",
                                 error_comment='You must enter a valid player name.',
                                 debug_info=repr(session['username']),
                                 suggestion='Check your input values')
    if player_data['game'] != '':
        logger.debug(f'Invalid input for game creation: The player {repr(session["username"])} is already in game {repr(player_data["game"])}.')
        return render_error_page(400,
                                 f'Invalid input',
                                 f"The player {repr(session['username'])} is already in game {repr(player_data['game'])}.",
                                 error_comment='You must enter a valid player name.',
                                 debug_info=repr(session['username']),
                                 suggestion='Check your input values')

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
    if len(game_name) > 32:
        logger.debug(f'Invalid input for game creation: The game name is too long.')
        return render_error_page(400,
                                 f'Invalid input',
                                 "The game name is too long.",
                                 error_comment='You must enter a game name with less than 32 characters.',
                                 debug_info=repr(game_name),
                                 suggestion='Check your input values')
    if any(char in game_name for char in denied_literals):
        logger.debug(f'Invalid input for game creation: The game name contains invalid characters.')
        return render_error_page(400,
                                 f'Invalid input',
                                 "The game name contains invalid characters.",
                                 error_comment='You must enter a game name without backslashes or slashes.',
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
    success, error = create_game_db(game_name, session['username'], password=game_password, data=game_data)
    if not success:
        logger.error(f'Error creating game ({repr(game_name)}) : {error}')
        return render_error_page(500,
                                 f'Error creating game',
                                 f"Error creating game ({repr(game_name)}) : {error}",
                                 error_comment='This may mean that the game name is already taken or that the game password is invalid.',
                                 debug_info=repr(error),
                                 suggestion='Check your input values')
    found, error = add_game_to_player(session['username'], game_name)
    if not found:
        logger.error(f'Error adding game ({repr(game_name)}) to player ({repr(session["username"])}) : {error}')
        return render_error_page(500,
                                 f'Error adding game to player',
                                 f"Error adding game ({repr(game_name)}) to player ({repr(session['username'])}) : {error}",
                                 error_comment='This may mean that the player is already in another game.',
                                 debug_info=repr(error),
                                 suggestion='Contact the administrator.')
    player_data['game_access'] = player_data.get('game_access', []) + [game_name]
    return redirect(safe_url_for('lobby'))