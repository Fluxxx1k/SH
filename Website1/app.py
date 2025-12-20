import flask
from flask import Flask, render_template, request, redirect, session, jsonify
import os
import sys

from jinja2 import Undefined

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
    stats = {'active_games': len(list(get_games_list()))}
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
    players = game_data.get('players', [])
    if session['username'] not in players:
        return redirect(safe_url_for('lobby'))
    
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

if __name__ == '__main__':
    app.run(debug=True, port=20050, host='0.0.0.0')