#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Упрощенное Flask-приложение с минимальным использованием Jinja2
Все данные рендерятся через JavaScript
"""

import os
import json
import secrets
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash

# Конфигурация
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SITE_NAME = os.environ.get('SITE_NAME') or 'Игра'

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

# Добавляем middleware для обработки JSON
def json_error_handler(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f'Error in {f.__name__}: {str(e)}')
            return jsonify({'error': 'Internal server error'}), 500
    wrapper.__name__ = f.__name__  # Сохраняем оригинальное имя функции
    return wrapper

# Глобальный обработчик ошибок
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('error.html'), 500

# Инициализация SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    logger=False, 
    engineio_logger=False,
    async_mode='threading',
    ping_timeout=20,
    ping_interval=25
)

# Простое хранилище данных в памяти
class SimpleDataStore:
    def __init__(self):
        self.users = {}
        self.games = {}
        self.sessions = {}
        self.online_users = set()
        
    def add_user(self, username, email, password_hash):
        if username in self.users:
            return False
        self.users[username] = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'rating': 1000
        }
        return True
        
    def get_user(self, username):
        return self.users.get(username)
        
    def create_game(self, creator, max_players=6):
        game_id = secrets.token_hex(8)
        self.games[game_id] = {
            'id': game_id,
            'creator': creator,
            'status': 'waiting',
            'players': [creator],
            'max_players': max_players,
            'current_players': 1,
            'created_at': datetime.now().isoformat(),
            'chat': []
        }
        return game_id
        
    def get_active_games(self):
        return [
            {
                'id': game['id'],
                'creator': game['creator'],
                'status': game['status'],
                'current_players': game['current_players'],
                'max_players': game['max_players'],
                'players': game['players'][:4]
            }
            for game in self.games.values()
            if game['status'] in ['waiting', 'playing']
        ]
        
    def get_game(self, game_id):
        return self.games.get(game_id)
        
    def add_player_to_game(self, game_id, username):
        game = self.games.get(game_id)
        if not game or game['status'] != 'waiting':
            return False
        if username in game['players']:
            return True
        if len(game['players']) >= game['max_players']:
            return False
        game['players'].append(username)
        game['current_players'] += 1
        return True

# Инициализация хранилища
data_store = SimpleDataStore()

# Вспомогательные функции
def require_auth(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# API endpoints
@app.route('/api/auth/register', methods=['POST'])
@json_error_handler
def api_register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if data_store.get_user(username):
            return jsonify({'error': 'Username already exists'}), 400
            
        password_hash = generate_password_hash(password)
        if data_store.add_user(username, email, password_hash):
            session['username'] = username
            return jsonify({'success': True, 'username': username})
        
        return jsonify({'error': 'Registration failed'}), 500
    except Exception as e:
        app.logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
@json_error_handler
def api_login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Missing required fields'}), 400
            
        user = data_store.get_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            data_store.online_users.add(username)
            return jsonify({'success': True, 'username': username})
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        app.logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def api_logout():
    username = session.pop('username', None)
    if username:
        data_store.online_users.discard(username)
    return jsonify({'success': True})

@app.route('/api/auth/status')
def api_auth_status():
    return jsonify({
        'authenticated': 'username' in session,
        'username': session.get('username')
    })

@app.route('/api/games')
def api_games():
    games = data_store.get_active_games()
    return jsonify({'games': games})

@app.route('/api/games', methods=['POST'])
@require_auth
def api_create_game():
    data = request.get_json()
    max_players = data.get('max_players', 6)
    username = session['username']
    
    game_id = data_store.create_game(username, max_players)
    return jsonify({'success': True, 'game_id': game_id})

@app.route('/api/games/<game_id>')
def api_game_details(game_id):
    game = data_store.get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(game)

@app.route('/api/games/<game_id>/join', methods=['POST'])
@require_auth
def api_join_game(game_id):
    username = session['username']
    if data_store.add_player_to_game(game_id, username):
        return jsonify({'success': True})
    return jsonify({'error': 'Failed to join game'}), 400

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username:
        data_store.online_users.discard(username)
    print('Client disconnected')

@socketio.on('join_game')
@require_auth
def handle_join_game(data):
    game_id = data.get('game_id')
    if game_id:
        join_room(game_id)
        emit('player_joined', {'username': session['username']}, room=game_id)

@socketio.on('leave_game')
@require_auth
def handle_leave_game(data):
    game_id = data.get('game_id')
    if game_id:
        leave_room(game_id)
        emit('player_left', {'username': session['username']}, room=game_id)

@socketio.on('chat_message')
@require_auth
def handle_chat_message(data):
    game_id = data.get('game_id')
    message = data.get('message')
    if game_id and message:
        emit('chat_message', {
            'username': session['username'],
            'message': message,
            'timestamp': datetime.now().isoformat()
        }, room=game_id)

# HTML routes - минимальные шаблоны без данных
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/lobby')
def lobby():
    return render_template('lobby.html')

@app.route('/game/<game_id>')
def game(game_id):
    return render_template('game.html', game_id=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)