import os
import json
from typing import Iterable, Literal

from flask import Flask, request, redirect, session, jsonify

import user_settings
from Website_featetures.error_handler.safe_functions import *
from Website_featetures.error_handler.undefined import SilentUndefined
from WebsiteEasiest.data.database_work import exists_player, create_player, login_player
from core.players.abstract_player import AbstractPlayer

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.jinja_env.undefined = SilentUndefined

class GamesDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.games = {}
    def __setitem__(self, key, value) -> bool:
        if len(self.games) > 7:
            return False
        else:
            self.games[key] = value
            return True
games_dict = GamesDict()


class WebPlayer(AbstractPlayer):
    def president(self, cards: str | list[str], cnc: "AbstractPlayer"):
        pass
    def chancellor(self, cards: str, prs: "AbstractPlayer", words, veto):
        pass

    def president_said_after_chancellor(self, *, cards: str, cnc: "AbstractPlayer", ccg: str, cps: str, ccs: str,
                                        ccp: str) -> str:
        pass

    def check_cards(self, cards: str) -> str:
        pass

    def check_player(self) -> tuple[int, str]:
        pass

    def purge_another(self, purge_type: str, votes: dict[int, int] = None) -> int:
        pass

    def place_another(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass

    def choose_chancellor(self, cannot_be: Iterable[int] = frozenset(), votes: dict[int, int] = None) -> int:
        pass

    def vote_for_pair(self, prs: AbstractPlayer, cnc: AbstractPlayer) -> Literal[-1, 0, 1]:
        pass

@app.route('/')
def index():
    return safe_render_template('index.html')

@app.route('/login')
def login():
    return safe_render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        return render_error_page(400, logging_in_player[1])
    else:
        return redirect(safe_url_for('lobby'))
@app.route('/register', methods=['POST'])
def register_post():
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
    return safe_render_template('logout.html')
@app.route('/register')
def register():
    return safe_render_template('register.html')
@app.route('/lobby')
def lobby():
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
    
    return safe_render_template('lobby.html', 
                         username=session['username'], 
                         games=games)

@app.route('/game/<game_name>')
def game(game_name):
    print(f'GAME {game_name} |  {session["username"]}')
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # Load game data
    game_file = os.path.join('data', 'games', f'{game_name}.json')
    if not os.path.exists(game_file):
        return safe_render_template('error.html', error_code=404, error_message="Игра не найдена"), 404
    
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
    
    return safe_render_template('game.html',
                        created_by=game_data['created_by'],
                        game_name=game_name,
                        players=players)

@app.route('/game/<game_name>/ws')
def game_ws(game_name):
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # TODO: Implement WebSocket connection
    return "Not implemented", 501

@app.route('/game/<game_name>/vote', methods=['POST'])
def game_vote(game_name):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    # TODO: Implement vote processing
    return jsonify({'success': True, 'message': 'Vote recorded'})

@app.route('/game/<game_name>/vote_player', methods=['POST'])
def game_vote_player(game_name):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    # TODO: Implement player vote processing
    return jsonify({'success': True, 'message': 'Player vote recorded'})

@app.route('/game/<game_name>/start', methods=['POST'])
def game_start(game_name):
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    # Load game data
    game_file = os.path.join('data', 'games', f'{game_name}.json')
    if not os.path.exists(game_file):
        return jsonify({'success': False, 'message': 'Game not found'}), 404
    
    with open(game_file, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    
    # Check if user is the creator
    if game_data['created_by'] != session['username']:
        return jsonify({'success': False, 'message': 'Only game creator can start the game'}), 403

    roles = user_settings.get_roles(game_data['current_players'])
    players = [WebPlayer(i, game_data['players'], roles[i]) for i in range(game_data['players'])]
    from core.games.basegame import BaseGame
    games_dict[game_name] = BaseGame(game_name, players)
    
    # Update game status
    game_data['status'] = 'started'
    with open(game_file, 'w', encoding='utf-8') as f:
        json.dump(game_data, f)
    
    return jsonify({'success': True, 'message': 'Game started'})

@app.route('/create_game', methods=['GET', 'POST'])
def create_game(VOTE_DELAY=30):
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
        return safe_render_template('create_game.html',
                             username=session['username'],
                             min_players=MIN_PLAYER_NUM,
                             max_players=MAX_PLAYER_NUM,
                             default_players=default_players,
                             red_win_num=RED_WIN_NUM,
                             black_win_num=BLACK_WIN_NUM,
                             anarchy_skip_num=ANARCHY_SKIP_NUM,
                             date_format=DATE_FORMAT,
                             time_format=TIME_FORMAT,
                             vote_anonymous=VOTE_ANONYMOUS,
                             veto_num_black=VETO_NUM_BLACK,
                             vote_delay=VOTE_DELAY)
    
    # Handle POST request for game creation
    game_name = request.form.get('game_name')
    game_password = request.form.get('game_password', '')
    max_players = int(request.form.get('max_players', MIN_PLAYER_NUM))
    

    # Create game data
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
    
    # Save game
    games_dir = os.path.join('data', 'games')
    os.makedirs(games_dir, exist_ok=True)
    with open(os.path.join(games_dir, f"{game_name}.json"), 'w') as f:
        json.dump(game_data, f)
    
    return redirect(safe_url_for('lobby'))


def render_error_page(error_code, error_message=None, error_description=None, error_comment=None, suggestion=None,
                      debug_info=None):
    """Render error page with comprehensive error information"""
    try:
        return safe_render_template('error.html',
                               error_code=error_code,
                               error_message=error_message,
                               error_description=error_description,
                               error_comment=error_comment,
                               suggestion=suggestion,
                               debug_info=debug_info,
                               config={'DEBUG': app.debug})
    except Exception as e:
        # Fallback if error template fails
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Критическая ошибка {error_code}</title></head>
        <body>
            <h1>Критическая ошибка {e}</h1>
            <p>{error_message or 'Произошла ошибка'}</p>
            <p>{error_description or 'Произошла ошибка'}</p>
            <p>{error_comment or 'Нет дополнительной информации'}</p>
            <p>{suggestion or 'Нет совета'}</p>
            <p>{debug_info or 'Нет отладочной информации о изначальной ошибке'}</p>
            <p>{repr(e)}</p>
            <a href="{safe_url_for('index')}">На главную</a>
        </body>
        </html>
        """, error_code


# HTTP Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    return render_error_page(
        error_code=404,
        error_message="Страница не найдена",
        error_description="Запрошенная страница не существует или была перемещена.",
        error_comment="Возможно, вы ввели неправильный адрес или страница была удалена.",
        suggestion="Проверьте правильность URL-адреса или вернитесь на главную страницу."
    ), 404


@app.errorhandler(500)
def internal_error(handled_error: Exception):
    """Handle 500 Internal Server errors"""
    import traceback
    debug_info = None
    if app.debug:
        debug_info = traceback.format_exc()

    return render_error_page(
        error_code=500,
        error_message="Внутренняя ошибка сервера",
        error_description="Произошла ошибка на сервере при обработке вашего запроса.",
        error_comment="Мы уже работаем над решением этой проблемы.",
        suggestion="Попробуйте обновить страницу через несколько минут. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=f"{debug_info} | {handled_error}"
    ), 500


@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors"""
    return render_error_page(
        error_code=403,
        error_message="Доступ запрещен",
        error_description="У вас нет прав для доступа к этой странице или ресурсу.",
        error_comment="Возможно, вам нужно войти в систему или у вас недостаточно прав.",
        suggestion="Попробуйте войти в систему или обратитесь к администратору для получения необходимых прав."
    ), 403


@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized errors"""
    return render_error_page(
        error_code=401,
        error_message="Необходима авторизация",
        error_description="Для доступа к этой странице необходимо войти в систему.",
        error_comment="Пожалуйста, авторизуйтесь, чтобы продолжить.",
        suggestion="Используйте форму входа или зарегистрируйтесь, если у вас еще нет аккаунта."
    ), 401


@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors"""
    return render_error_page(
        error_code=400,
        error_message="Неверный запрос",
        error_description="Запрос содержит неверные данные или параметры.",
        error_comment="Проверьте правильность введенных данных.",
        suggestion="Попробуйте выполнить действие еще раз, проверив все введенные данные."
    ), 400


@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 Method Not Allowed errors"""
    return render_error_page(
        error_code=405,
        error_message="Метод не разрешен",
        error_description="Используемый метод HTTP не разрешен для этого ресурса.",
        error_comment="Например, попытка отправить POST-запрос на страницу, которая принимает только GET-запросы.",
        suggestion="Попробуйте использовать другой метод или обратитесь к документации API."
    ), 405


# Custom error route for manual error display
@app.route('/error')
def error():
    """Manual error display route"""
    error_code = request.args.get('error_code', request.args.get('code', 500, type=int), type=int)
    error_message = request.args.get('error_message', request.args.get('message'))
    error_description = request.args.get('error_description', request.args.get('description'))
    error_comment = request.args.get('error_comment', request.args.get('comment'))
    suggestion = request.args.get('suggestion')
    debug_info = request.args.get('debug_info')

    return render_error_page(
        error_code=error_code,
        error_message=error_message,
        error_description=error_description,
        error_comment=error_comment,
        suggestion=suggestion,
        debug_info=debug_info
    ), error_code


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
    app.run(debug=True)