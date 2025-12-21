import flask
from flask import Flask, render_template, request, redirect, session, jsonify
import os
import sys

from jinja2 import Undefined

from Website.database_work import get_games_count, get_complete_games_count, get_players_count, get_players_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database_work import verify_player, create_player, create_game, verify_game, find_game_data, save_game_data, \
    get_games_list
from server_settings import MIN_PLAYER_NUM, MAX_PLAYER_NUM, MIN_NAME_LEN, MAX_NAME_LEN

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

class SilentUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return 'error'

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = \
        __int__ = __float__ = __complex__ = __pow__ = __rpow__ = \
        __sub__ = __rsub__ = _fail_with_undefined_error


app.jinja_env.undefined = SilentUndefined

def safe_url_for(endpoint, **values):
    """Helper function to generate safe URLs"""
    try:
        return flask.url_for(endpoint, _external=True, **values)
    except Exception as e:
        print(f"Error in safe_url_for: {e}")
        return '/'

@app.route('/')
def index():
    """Main page for Secret Hitler online game"""
    stats = {'active_games': get_games_count(),
             'complete_games': get_complete_games_count(),
             'total_players': get_players_count(),
             # 'players_list': list(get_players_list()),
             }
    return render_template('index.html', stats=stats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Player login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Please fill in all fields', 
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
        
        success, message = verify_player(username, password)
        if success:
            session['username'] = username
            return redirect(safe_url_for('lobby'))
        else:
            return render_template('login.html', error=message, 
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
    
    return render_template('login.html', min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Player registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password:
            return render_template('register.html', error='Please fill in all fields',
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
        
        if len(username) < MIN_NAME_LEN or len(username) > MAX_NAME_LEN:
            return render_template('register.html', error=f'Username must be between {MIN_NAME_LEN} and {MAX_NAME_LEN} characters',
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match',
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
        
        error = create_player(username, password)
        if error is None:
            session['username'] = username
            return redirect(safe_url_for('lobby'))
        else:
            return render_template('register.html', error=str(error),
                                 min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)
    
    return render_template('register.html', min_name_len=MIN_NAME_LEN, max_name_len=MAX_NAME_LEN)

@app.route('/lobby')
def lobby():
    """Game lobby page"""
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # Get list of available games
    games = list(get_games_list())
    
    return render_template('lobby.html', username=session['username'], games=games)

@app.route('/logout')
def logout():
    """Logout route"""
    session.pop('username', None)
    return redirect(safe_url_for('index'))

@app.route('/create_game', methods=['POST'])
def create_game_route():
    """Create new game"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    game_name = request.json.get('game_name')
    game_password = request.json.get('game_password', '')
    max_players = request.json.get('max_players', MIN_PLAYER_NUM)
    
    if not game_name:
        return jsonify({'success': False, 'error': 'Game name is required'})
    
    try:
        max_players = int(max_players)
        if max_players < MIN_PLAYER_NUM or max_players > MAX_PLAYER_NUM:
            return jsonify({'success': False, 'error': f'Players must be between {MIN_PLAYER_NUM} and {MAX_PLAYER_NUM}'})
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid player count'})
    
    game_data = {
        'name': game_name,
        'password': game_password,
        'max_players': max_players,
        'current_players': 1,
        'status': 'waiting',
        'created_by': session['username']
    }
    
    error = create_game(game_name, game_data, session['username'])
    if error is None:
        return jsonify({'success': True, 'message': 'Game created successfully'})
    else:
        return jsonify({'success': False, 'error': str(error)})

@app.route('/join_game', methods=['POST'])
def join_game_route():
    """Join existing game"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    game_name = request.json.get('game_name')
    game_password = request.json.get('game_password', '')
    
    if not game_name:
        return jsonify({'success': False, 'error': 'Game name is required'})
    
    success, message = verify_game(game_name, game_password, session['username'])
    if success:
        return jsonify({'success': True, 'message': 'Joined game successfully'})
    else:
        return jsonify({'success': False, 'error': message})

@app.route('/api/games')
def api_games():
    """API endpoint to get list of available games"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    games = list(get_games_list())
    return jsonify({'success': True, 'games': games})

@app.route('/game/<game_name>')
def game(game_name):
    """Game page for playing Secret Hitler"""
    if 'username' not in session:
        return redirect(safe_url_for('login'))
    
    # Get game data
    game_data = find_game_data(game_name)
    if not game_data:
        return redirect(safe_url_for('lobby'))
    
    # Get list of players in the game
    if isinstance(game_data, Exception):
        if isinstance(game_data, FileNotFoundError):
            return redirect(safe_url_for('error',
                                         error_code=404,
                                         error_message='Game not found',
                                         error_description='Game data file not found',
                                         suggestion='Contact administrator if you sure if game is valid',
                                         debug_info=repr(game_data)))
        return redirect(safe_url_for('error',
                                     error_code=500,
                                     error_message=repr(game_data),
                                     error_description='Game data error',
                                     error_comment='Game data is corrupted or doesn\'t exist',
                                     suggestion='Contact administrator if you sure if game is valid',
                                     debug_info=repr(game_data)))
    if isinstance(game_data.get('players'), list):
        players = game_data.get('players', [])
    else:
        players = []
    if session['username'] not in players:
        return redirect(safe_url_for('error',
                                     error_code=403,
                                     error_message='Forbidden',
                                     error_description='Player not in game',
                                     error_comment='You are not part of this game',
                                     suggestion='Contact administrator if you sure if game is valid',
                                     debug_info=f'Player {session["username"]} not in game {game_name}'))
    
    return render_template('game.html', 
                         username=session['username'],
                         game_name=game_name,
                         players=players,
                         current_turn=game_data.get('current_turn', ''),
                         game_phase=game_data.get('phase', 'waiting'),
                         player_count=len(players))

@app.route('/api/game/vote', methods=['POST'])
def api_game_vote():
    """API endpoint for voting in game"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    game_name = request.json.get('game_name')
    vote = request.json.get('vote')
    
    if not game_name or not vote:
        return jsonify({'success': False, 'error': 'Game name and vote are required'})
    
    # Get current game data
    game_data = find_game_data(game_name)
    if not game_data:
        return jsonify({'success': False, 'error': 'Game not found'})
    
    # Check if player is in the game
    if session['username'] not in game_data.get('players', []):
        return jsonify({'success': False, 'error': 'Player not in game'})
    
    # Process vote (this is a simplified version)
    if 'votes' not in game_data:
        game_data['votes'] = {}
    
    game_data['votes'][session['username']] = vote
    game_data['last_action'] = f"{session['username']} voted {vote}"
    
    # Save updated game data
    save_game_data(game_name, game_data)
    
    return jsonify({
        'success': True,
        'message': 'Vote recorded',
        'game_data': game_data
    })

@app.route('/api/game/select_player', methods=['POST'])
def api_game_select_player():
    """API endpoint for selecting a player in game"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    game_name = request.json.get('game_name')
    selected_player = request.json.get('selected_player')
    
    if not game_name or not selected_player:
        return jsonify({'success': False, 'error': 'Game name and selected player are required'})
    
    # Get current game data
    game_data = find_game_data(game_name)
    if not game_data:
        return jsonify({'success': False, 'error': 'Game not found'})
    
    # Check if player is in the game
    if session['username'] not in game_data.get('players', []):
        return jsonify({'success': False, 'error': 'Player not in game'})
    
    # Check if selected player is in the game
    if selected_player not in game_data.get('players', []):
        return jsonify({'success': False, 'error': 'Selected player not in game'})
    
    # Process player selection (this is a simplified version)
    game_data['selected_player'] = selected_player
    game_data['last_action'] = f"{session['username']} selected {selected_player}"
    
    # Save updated game data
    save_game_data(game_name, game_data)
    
    return jsonify({
        'success': True,
        'message': 'Player selected',
        'game_data': game_data
    })

@app.route('/api/game/<game_name>')
def api_game_data(game_name):
    """API endpoint to get game data"""
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    game_data = find_game_data(game_name)
    if not game_data:
        return jsonify({'success': False, 'error': 'Game not found'})
    
    # Check if player is in the game
    if session['username'] not in game_data.get('players', []):
        return jsonify({'success': False, 'error': 'Player not in game'})
    
    return jsonify({
        'success': True,
        'game_data': game_data
    })

# Error handling functions
def render_error_page(error_code, error_message=None, error_description=None, error_comment=None, suggestion=None, debug_info=None):
    """Render error page with comprehensive error information"""
    try:
        return render_template('error.html',
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
    """Handle game-specific errors"""
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
    app.run(debug=True, port=20050, host='0.0.0.0')