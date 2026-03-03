#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Основное Flask-приложение для игры с real-time обновлениями
Перенос логики из WebsiteEasiest с добавлением WebSocket и современных функций
"""

import os
import json
import secrets
from datetime import datetime, timedelta
from functools import wraps
from typing import Dict, List, Optional, Any

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
import redis

# Конфигурация
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SITE_NAME = os.environ.get('SITE_NAME') or 'Игра'
    
    # Redis настройки
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CACHE_MAX_SIZE = 1024 * 1024 * 1024  # 1GB
    CACHE_TIMEOUT = 300  # 5 минут
    
    # Настройки сессий
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Настройки WebSocket
    SOCKETIO_ASYNC_MODE = 'threading'
    SOCKETIO_PING_TIMEOUT = 60
    SOCKETIO_PING_INTERVAL = 25
    
    # Настройки безопасности
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация Redis
try:
    redis_client = redis.from_url(app.config['REDIS_URL'])
    redis_client.ping()
    print("✅ Redis подключен успешно")
except Exception as e:
    print(f"⚠️  Redis недоступен: {e}")
    redis_client = None

# Инициализация SocketIO
socketio = SocketIO(
    app,
    async_mode=app.config['SOCKETIO_ASYNC_MODE'],
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# Временное хранилище данных (до миграции из WebsiteEasiest)
class DataStore:
    """Временное хранилище данных в памяти"""
    
    def __init__(self):
        self.users = {}  # username -> user_data
        self.games = {}  # game_id -> game_data
        self.sessions = {}  # session_id -> session_data
        self.online_users = set()
        self.stats = {
            'total_users': 0,
            'active_games': 0,
            'complete_games': 0,
            'total_players': 0
        }
        
    def add_user(self, username: str, email: str, password_hash: str) -> bool:
        """Добавить нового пользователя"""
        if username in self.users:
            return False
            
        self.users[username] = {
            'username': username,
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'games_played': 0,
            'games_won': 0,
            'rating': 1000,
            'is_demo': False
        }
        self.stats['total_users'] += 1
        return True
        
    def get_user(self, username: str) -> Optional[Dict]:
        """Получить данные пользователя"""
        return self.users.get(username)
        
    def update_user_login(self, username: str):
        """Обновить время последнего входа"""
        if username in self.users:
            self.users[username]['last_login'] = datetime.now().isoformat()
            self.online_users.add(username)
            self.stats['total_players'] = len(self.online_users)
            
    def remove_online_user(self, username: str):
        """Удалить пользователя из онлайн списка"""
        self.online_users.discard(username)
        self.stats['total_players'] = len(self.online_users)
        
    def create_game(self, creator: str, max_players: int = 6) -> str:
        """Создать новую игру"""
        game_id = secrets.token_hex(8)
        
        self.games[game_id] = {
            'id': game_id,
            'creator': creator,
            'status': 'waiting',
            'players': [creator],
            'max_players': max_players,
            'current_players': 1,
            'created_at': datetime.now().isoformat(),
            'started_at': None,
            'ended_at': None,
            'winner': None,
            'chat': [],
            'logs': [],
            'votes': {},
            'game_state': {}
        }
        
        self.stats['active_games'] += 1
        return game_id
        
    def get_active_games(self) -> List[Dict]:
        """Получить список активных игр"""
        return [
            {
                'id': game['id'],
                'creator': game['creator'],
                'status': game['status'],
                'players': game['players'][:4],  # Показать только первых 4 игроков
                'current_players': game['current_players'],
                'max_players': game['max_players'],
                'created_at': game['created_at']
            }
            for game in self.games.values()
            if game['status'] in ['waiting', 'playing']
        ]
        
    def get_game(self, game_id: str) -> Optional[Dict]:
        """Получить данные игры"""
        return self.games.get(game_id)
        
    def add_player_to_game(self, game_id: str, username: str) -> bool:
        """Добавить игрока в игру"""
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
        
    def remove_player_from_game(self, game_id: str, username: str) -> bool:
        """Удалить игрока из игры"""
        game = self.games.get(game_id)
        if not game or username not in game['players']:
            return False
            
        game['players'].remove(username)
        game['current_players'] -= 1
        
        if game['current_players'] == 0:
            self.delete_game(game_id)
            
        return True
        
    def delete_game(self, game_id: str):
        """Удалить игру"""
        if game_id in self.games:
            del self.games[game_id]
            self.stats['active_games'] -= 1
            self.stats['complete_games'] += 1
            
    def get_stats(self) -> Dict:
        """Получить статистику"""
        return self.stats.copy()

# Инициализация хранилища
data_store = DataStore()

# Улучшенная система авторизации
class AuthManager:
    """Менеджер аутентификации с использованием Redis"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_prefix = "session:"
        self.user_prefix = "user:"
        self.token_prefix = "token:"
        
    def create_session(self, username: str, remember_me: bool = False) -> str:
        """Создать новую сессию"""
        session_token = secrets.token_urlsafe(32)
        session_data = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')[:200]
        }
        
        # Сохраняем сессию в Redis
        if self.redis:
            session_key = f"{self.session_prefix}{session_token}"
            expires_in = timedelta(days=30) if remember_me else timedelta(hours=24)
            
            self.redis.hset(session_key, mapping={
                k: json.dumps(v) if isinstance(v, (dict, list)) else str(v)
                for k, v in session_data.items()
            })
            self.redis.expire(session_key, int(expires_in.total_seconds()))
            
            # Обновляем активность пользователя
            user_key = f"{self.user_prefix}{username}"
            self.redis.hset(user_key, 'last_activity', datetime.now().isoformat())
            self.redis.expire(user_key, int(expires_in.total_seconds()))
        
        return session_token
    
    def get_session(self, session_token: str) -> Optional[Dict]:
        """Получить данные сессии"""
        if not self.redis or not session_token:
            return None
            
        session_key = f"{self.session_prefix}{session_token}"
        session_data = self.redis.hgetall(session_key)
        
        if not session_data:
            return None
            
        # Обновляем последнюю активность
        self.redis.hset(session_key, 'last_activity', datetime.now().isoformat())
        
        # Декодируем данные
        decoded_data = {}
        for key, value in session_data.items():
            key = key.decode('utf-8') if isinstance(key, bytes) else key
            value = value.decode('utf-8') if isinstance(value, bytes) else value
            
            # Пытаемся декодировать JSON
            try:
                decoded_data[key] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                decoded_data[key] = value
                
        return decoded_data
    
    def delete_session(self, session_token: str) -> bool:
        """Удалить сессию"""
        if not self.redis or not session_token:
            return False
            
        session_key = f"{self.session_prefix}{session_token}"
        return bool(self.redis.delete(session_key))
    
    def is_user_online(self, username: str) -> bool:
        """Проверить онлайн ли пользователь"""
        if not self.redis:
            return False
            
        user_key = f"{self.user_prefix}{username}"
        last_activity = self.redis.hget(user_key, 'last_activity')
        
        if not last_activity:
            return False
            
        last_activity = datetime.fromisoformat(last_activity.decode('utf-8'))
        return datetime.now() - last_activity < timedelta(minutes=5)

# Инициализация менеджера авторизации
auth_manager = AuthManager(redis_client)

# Декораторы
def login_required(f):
    """Улучшенный декоратор для защиты маршрутов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get('session_token')
        
        if not session_token:
            return redirect(url_for('login', next=request.url))
            
        session_data = auth_manager.get_session(session_token)
        if not session_data:
            session.clear()
            return redirect(url_for('login', next=request.url))
            
        # Добавляем данные сессии в request
        request.current_user = session_data['username']
        request.session_data = session_data
        
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    """Улучшенный декоратор для защиты API маршрутов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get('session_token')
        
        if not session_token:
            return jsonify({'error': 'Требуется авторизация'}), 401
            
        session_data = auth_manager.get_session(session_token)
        if not session_data:
            session.clear()
            return jsonify({'error': 'Сессия истекла'}), 401
            
        # Добавляем данные сессии в request
        request.current_user = session_data['username']
        request.session_data = session_data
        
        return f(*args, **kwargs)
    return decorated_function

# Утилиты
def generate_demo_username() -> str:
    """Генерация имени для демо-пользователя"""
    import random
    adjectives = ['Быстрый', 'Умный', 'Смелый', 'Ловкий', 'Мудрый', 'Сильный']
    nouns = ['Волк', 'Орел', 'Лев', 'Тигр', 'Медведь', 'Ястреб']
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(100, 999)}"

# Основные маршруты
@app.route('/')
def index():
    """Главная страница"""
    stats = data_store.get_stats()
    return render_template('index.html', stats=stats)

@app.route('/lobby')
@login_required
def lobby():
    """Страница лобби"""
    username = request.current_user
    return render_template('lobby.html', username=username)

@app.route('/game/<game_id>')
@login_required
def game(game_id: str):
    """Страница игры"""
    game = data_store.get_game(game_id)
    if not game:
        flash('Игра не найдена', 'error')
        return redirect(url_for('lobby'))
        
    username = request.current_user
    if username not in game['players'] and game['status'] != 'waiting':
        flash('Вы не участвуете в этой игре', 'error')
        return redirect(url_for('lobby'))
        
    return render_template('game.html', game_id=game_id, username=username, game=game)

# Маршруты авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа с улучшенной системой авторизации"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not username or not password:
            flash('Заполните все поля', 'error')
            return render_template('login.html')
            
        user = data_store.get_user(username)
        if not user or not check_password_hash(user['password_hash'], password):
            flash('Неверное имя пользователя или пароль', 'error')
            return render_template('login.html')
            
        # Успешный вход - создаем новую сессию
        session_token = auth_manager.create_session(username, remember_me)
        session['session_token'] = session_token
        session.permanent = remember_me
        
        # Обновляем данные пользователя
        data_store.update_user_login(username)
        data_store.add_online_user(username)
        
        flash(f'Добро пожаловать, {username}!', 'success')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('lobby'))
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        terms = request.form.get('terms') == 'on'
        
        # Валидация
        if not username or not password:
            flash('Заполните обязательные поля', 'error')
            return render_template('register.html')
            
        if len(username) < 3 or len(username) > 20:
            flash('Имя пользователя должно быть от 3 до 20 символов', 'error')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('register.html')
            
        if len(password) < 6:
            flash('Пароль должен быть не менее 6 символов', 'error')
            return render_template('register.html')
            
        if not terms:
            flash('Необходимо согласие с условиями использования', 'error')
            return render_template('register.html')
            
        # Проверка существующего пользователя
        if data_store.get_user(username):
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register.html')
            
        # Создание пользователя
        password_hash = generate_password_hash(password)
        if data_store.add_user(username, email, password_hash):
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ошибка регистрации', 'error')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Выход из системы с улучшенной системой авторизации"""
    session_token = session.get('session_token')
    
    if session_token:
        # Получаем данные сессии перед удалением
        session_data = auth_manager.get_session(session_token)
        if session_data:
            username = session_data.get('username')
            if username:
                data_store.remove_online_user(username)
        
        # Удаляем сессию из Redis
        auth_manager.delete_session(session_token)
        
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# API маршруты
@app.route('/api/stats')
def api_stats():
    """API: Получить статистику"""
    stats = data_store.get_stats()
    return jsonify({
        'active_games': stats['active_games'],
        'total_players': stats['total_players'],
        'complete_games': stats['complete_games']
    })

@app.route('/api/games/active')
def api_active_games():
    """API: Получить активные игры"""
    games = data_store.get_active_games()
    return jsonify(games)

@app.route('/api/health')
def api_health():
    """API: Проверка состояния сервера"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'redis_connected': redis_client is not None,
        'online_users': len(data_store.online_users)
    })

@app.route('/api/auth/demo', methods=['POST'])
def api_demo_login():
    """API: Вход в демо-режим с улучшенной системой авторизации"""
    try:
        data = request.get_json() or {}
        demo_type = data.get('type', 'player')
        
        # Генерация демо-пользователя
        username = generate_demo_username()
        
        # Проверка существующего имени
        while data_store.get_user(username):
            username = generate_demo_username()
            
        # Создание демо-пользователя
        password_hash = generate_password_hash(secrets.token_hex(16))
        if data_store.add_user(username, '', password_hash):
            data_store.users[username]['is_demo'] = True
            
            # Авторизация с созданием сессии
            session_token = auth_manager.create_session(username, remember_me=False)
            session['session_token'] = session_token
            session.permanent = False  # Демо-сессия временная
            data_store.update_user_login(username)
            data_store.add_online_user(username)
            
            return jsonify({
                'success': True,
                'message': f'Добро пожаловать, {username}!',
                'username': username,
                'is_demo': True
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось создать демо-пользователя'
            })
            
    except Exception as e:
        print(f"Ошибка демо-входа: {e}")
        return jsonify({
            'success': False,
            'message': 'Ошибка сервера'
        }), 500

# WebSocket обработчики
@socketio.on('connect')
def handle_connect():
    """Обработчик подключения WebSocket"""
    print(f"WebSocket клиент подключен: {request.sid}")
    emit('connected', {'status': 'connected', 'sid': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    """Обработчик отключения WebSocket"""
    print(f"WebSocket клиент отключен: {request.sid}")
    
    # Удаление пользователя из всех комнат
    username = session.get('username')
    if username:
        data_store.remove_online_user(username)
        leave_room(f'user_{username}')
        
        # Уведомление других пользователей
        emit('player_offline', {'username': username}, broadcast=True, include_self=False)

@socketio.on('join_lobby')
def handle_join_lobby():
    """Присоединение к лобби"""
    username = session.get('username')
    if not username:
        emit('error', {'message': 'Требуется авторизация'})
        return
        
    join_room('lobby')
    data_store.update_user_login(username)
    
    # Отправка текущих данных
    emit('lobby_data', {
        'games': data_store.get_active_games(),
        'online_users': list(data_store.online_users)
    })
    
    # Уведомление других пользователей
    emit('player_online', {'username': username}, room='lobby', include_self=False)
    
@socketio.on('leave_lobby')
def handle_leave_lobby():
    """Покидание лобби"""
    username = session.get('username')
    if username:
        leave_room('lobby')
        emit('player_offline', {'username': username}, room='lobby', include_self=False)

@socketio.on('create_game')
def handle_create_game(data):
    """Создание новой игры"""
    username = session.get('username')
    if not username:
        emit('error', {'message': 'Требуется авторизация'})
        return
        
    max_players = data.get('max_players', 6)
    if not isinstance(max_players, int) or max_players < 2 or max_players > 10:
        max_players = 6
        
    game_id = data_store.create_game(username, max_players)
    
    # Присоединение создателя к игре
    join_room(f'game_{game_id}')
    
    # Уведомление лобби о новой игре
    emit('game_created', {
        'game_id': game_id,
        'creator': username,
        'max_players': max_players
    }, room='lobby')
    
    emit('game_created_success', {'game_id': game_id})

@socketio.on('join_game')
def handle_join_game(data):
    """Присоединение к игре"""
    username = session.get('username')
    if not username:
        emit('error', {'message': 'Требуется авторизация'})
        return
        
    game_id = data.get('game_id')
    if not game_id:
        emit('error', {'message': 'ID игры обязателен'})
        return
        
    game = data_store.get_game(game_id)
    if not game:
        emit('error', {'message': 'Игра не найдена'})
        return
        
    if game['status'] != 'waiting':
        emit('error', {'message': 'Игра уже началась'})
        return
        
    if not data_store.add_player_to_game(game_id, username):
        emit('error', {'message': 'Не удалось присоединиться к игре'})
        return
        
    # Присоединение к комнате игры
    join_room(f'game_{game_id}')
    
    # Уведомление игры о новом игроке
    emit('player_joined', {
        'game_id': game_id,
        'username': username,
        'players': game['players']
    }, room=f'game_{game_id}')
    
    # Уведомление лобби об обновлении игры
    emit('game_updated', {
        'game_id': game_id,
        'current_players': game['current_players']
    }, room='lobby')

@socketio.on('leave_game')
def handle_leave_game(data):
    """Покидание игры"""
    username = session.get('username')
    if not username:
        return
        
    game_id = data.get('game_id')
    if not game_id:
        return
        
    game = data_store.get_game(game_id)
    if not game:
        return
        
    if data_store.remove_player_from_game(game_id, username):
        leave_room(f'game_{game_id}')
        
        # Уведомление игры об уходе игрока
        emit('player_left', {
            'game_id': game_id,
            'username': username,
            'players': game['players']
        }, room=f'game_{game_id}')
        
        # Уведомление лобби об обновлении игры
        emit('game_updated', {
            'game_id': game_id,
            'current_players': game['current_players']
        }, room='lobby')

@socketio.on('game_chat_message')
def handle_game_chat_message(data):
    """Сообщение в чате игры"""
    username = session.get('username')
    if not username:
        emit('error', {'message': 'Требуется авторизация'})
        return
        
    game_id = data.get('game_id')
    message = data.get('message', '').strip()
    
    if not game_id or not message:
        return
        
    game = data_store.get_game(game_id)
    if not game or username not in game['players']:
        return
        
    # Добавление сообщения в чат
    chat_message = {
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    game['chat'].append(chat_message)
    
    # Ограничение размера чата
    if len(game['chat']) > 100:
        game['chat'] = game['chat'][-100:]
        
    # Отправка сообщения всем игрокам в игре
    emit('chat_message', chat_message, room=f'game_{game_id}')

@socketio.on('game_log_message')
def handle_game_log_message(data):
    """Сообщение в логе игры"""
    username = session.get('username')
    if not username:
        return
        
    game_id = data.get('game_id')
    log_message = data.get('message', '').strip()
    
    if not game_id or not log_message:
        return
        
    game = data_store.get_game(game_id)
    if not game or username not in game['players']:
        return
        
    # Добавление сообщения в лог
    log_entry = {
        'type': data.get('type', 'info'),
        'message': log_message,
        'timestamp': datetime.now().isoformat()
    }
    game['logs'].append(log_entry)
    
    # Ограничение размера лога
    if len(game['logs']) > 200:
        game['logs'] = game['logs'][-200:]
        
    # Отправка лога всем игрокам в игре
    emit('log_message', log_entry, room=f'game_{game_id}')

@socketio.on('game_vote')
def handle_game_vote(data):
    """Голосование в игре"""
    username = session.get('username')
    if not username:
        return
        
    game_id = data.get('game_id')
    vote_target = data.get('target')
    
    if not game_id or not vote_target:
        return
        
    game = data_store.get_game(game_id)
    if not game or username not in game['players']:
        return
        
    # Сохранение голоса
    game['votes'][username] = vote_target
    
    # Отправка обновления голосов
    emit('vote_updated', {
        'game_id': game_id,
        'voter': username,
        'target': vote_target,
        'votes': game['votes']
    }, room=f'game_{game_id}')

# Запуск приложения
if __name__ == '__main__':
    print(f"🚀 Запуск {app.config['SITE_NAME']}...")
    print(f"📊 Статистика: {data_store.get_stats()}")
    
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True,
        allow_unsafe_werkzeug=True
    )