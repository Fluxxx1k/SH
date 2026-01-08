from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import uuid
from collections import defaultdict
from webplayers.web_player import WebPlayer
from core.games.basegame import BaseGame
from core.standard_names_SH import X

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)
from jinja2 import Undefined
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

# Game state storage
games = {}
active_games = {}
players_in_games = defaultdict(dict)
player_objects = {}

def create_game_instance(game_id):
    players = [WebPlayer(i, name, '', request.sid) for i, name in enumerate(games[game_id]['players'])]
    game = BaseGame(players)
    active_games[game_id] = game
    return game

# User data storage
USERS_FILE = 'users.json'

# Initialize users file if not exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({}, f)

# WebPlayer class
class WebPlayer:
    def __init__(self, username, player_id):
        self.username = username
        self.id = player_id
        self.role = None
        self.party = None

# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return "Username already exists", 400
            
        users[username] = {
            'password': generate_password_hash(password)
        }
        
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
            
        session['username'] = username
        return redirect(url_for('lobby'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        
        if username not in users or not check_password_hash(users[username]['password'], password):
            return "Invalid username or password", 401
            
        session['username'] = username
        return redirect(url_for('lobby'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lobby')
def lobby():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('lobby.html')

@app.route('/game/<game_id>')
def game(game_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if game_id not in games:
        return redirect(url_for('lobby'))
        
    return render_template('game.html')

# SocketIO events
@socketio.on('connect', namespace='/lobby')
def handle_lobby_connect():
    if 'username' in session:
        emit('games_list', {'games': list(games.values())})

@socketio.on('create_game', namespace='/lobby')
def handle_create_game():
    game_id = str(uuid.uuid4())[:8]
    games[game_id] = {
        'id': game_id,
        'players': [session['username']],
        'max_players': 10,
        'status': 'waiting'
    }
    
    players_in_games[game_id][session['username']] = request.sid
    emit('game_created', {'game_id': game_id}, room=request.sid)
    emit('games_list', {'games': list(games.values())}, broadcast=True)

@socketio.on('join_game', namespace='/lobby')
def handle_join_game(data):
    game_id = data['game_id']
    if game_id in games and len(games[game_id]['players']) < games[game_id]['max_players']:
        games[game_id]['players'].append(session['username'])
        players_in_games[game_id][session['username']] = request.sid
        emit('game_joined', {'game_id': game_id}, room=request.sid)
        emit('games_list', {'games': list(games.values())}, broadcast=True)

@socketio.on('connect', namespace='/game')
def handle_game_connect(data):
    game_id = data['game_id']
    if game_id in games and 'username' in session:
        join_room(game_id)
        
        # Initialize game if not already
        if game_id not in active_games:
            game = create_game_instance(game_id)
        else:
            game = active_games[game_id]
            
        # Assign player object
        player_idx = games[game_id]['players'].index(session['username'])
        player = game.globs.PLAYERS[player_idx]
        player.socket_id = request.sid
        player_objects[request.sid] = player
        
        emit('game_state', {
            'players': games[game_id]['players'],
            'game_state': game.get_state()
        }, room=game_id)
        
        # Handle pending actions
        if player.pending_action:
            emit('player_action', player.pending_action, room=request.sid)

@socketio.on('player_response', namespace='/game')
def handle_player_response(data):
    player = player_objects.get(request.sid)
    if player:
        player.action_result = data
        
        # Continue game logic
        game_id = next((gid for gid, game in active_games.items() 
                       if player in game.globs.PLAYERS), None)
        if game_id:
            game = active_games[game_id]
            result = game.take_move()
            
            if result != 0:  # Game ended
                emit('game_over', {'result': result}, room=game_id)
            else:
                emit('game_state', {
                    'players': games[game_id]['players'],
                    'game_state': game.get_state()
                }, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True)