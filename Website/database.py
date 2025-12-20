import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional

class JSONDatabase:
    def __init__(self, db_file='users.json'):
        self.db_file = os.path.join(os.path.dirname(__file__), db_file)
        self.data = self._load_db()
    
    def _load_db(self) -> Dict:
        """Загрузка данных из JSON файла"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки БД: {e}")
        
        # Возвращаем структуру по умолчанию
        return {
            "users": {},
            "games": {},
            "sessions": {}
        }
    
    def _save_db(self):
        """Сохранение данных в JSON файл"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения БД: {e}")
            return False
    
    def _hash_password(self, password: str) -> str:
        """Хеширование пароля с использованием werkzeug security"""
        try:
            from werkzeug.security import generate_password_hash
            return generate_password_hash(password, method='scrypt')
        except ImportError:
            # Fallback на простое хеширование
            return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, password: str, email: str = "") -> bool:
        """Создание нового пользователя"""
        if username in self.data["users"]:
            return False  # Пользователь уже существует
        
        self.data["users"][username] = {
            "password": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "games_played": 0,
            "wins": 0,
            "losses": 0
        }
        return self._save_db()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Аутентификация пользователя"""
        if username not in self.data["users"]:
            return False
        
        stored_hash = self.data["users"][username]["password"]
        return stored_hash == self._hash_password(password)
    
    def create_session(self, username: str) -> str:
        """Создание сессии для пользователя"""
        session_id = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()
        self.data["sessions"][session_id] = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        self._save_db()
        return session_id
    
    def get_user_by_session(self, session_id: str) -> Optional[str]:
        """Получение пользователя по сессии"""
        if session_id not in self.data["sessions"]:
            return None
        
        session = self.data["sessions"][session_id]
        expires_at = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires_at:
            # Сессия истекла
            del self.data["sessions"][session_id]
            self._save_db()
            return None
        
        return session["username"]
    
    def save_game(self, username: str, game_data: Dict) -> str:
        """Сохранение игры"""
        game_id = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()[:16]
        
        self.data["games"][game_id] = {
            "username": username,
            "game_data": game_data,
            "created_at": datetime.now().isoformat(),
            "status": "active"  # active, completed, abandoned
        }
        
        # Обновляем статистику пользователя
        if username in self.data["users"]:
            self.data["users"][username]["games_played"] += 1
        
        self._save_db()
        return game_id
    
    def get_user_games(self, username: str) -> List[Dict]:
        """Получение всех игр пользователя"""
        user_games = []
        for game_id, game_info in self.data["games"].items():
            if game_info["username"] == username:
                user_games.append({
                    "game_id": game_id,
                    "created_at": game_info["created_at"],
                    "status": game_info["status"]
                })
        return sorted(user_games, key=lambda x: x["created_at"], reverse=True)
    
    def get_game(self, game_id: str) -> Optional[Dict]:
        """Получение данных игры"""
        return self.data["games"].get(game_id)
    
    def update_game_status(self, game_id: str, status: str) -> bool:
        """Обновление статуса игры"""
        if game_id in self.data["games"]:
            self.data["games"][game_id]["status"] = status
            return self._save_db()
        return False
    
    def get_user_stats(self, username: str) -> Optional[Dict]:
        """Получение статистики пользователя"""
        if username in self.data["users"]:
            user_data = self.data["users"][username].copy()
            del user_data["password"]  # Удаляем пароль из ответа
            return user_data
        return None

# Создаем глобальный экземпляр БД
db = JSONDatabase()

# Пример использования
if __name__ == "__main__":
    # Создаем тестового пользователя
    db.create_user("test_user", "password123", "test@example.com")
    
    # Аутентификация
    if db.authenticate_user("test_user", "password123"):
        print("Аутентификация успешна!")
        session_id = db.create_session("test_user")
        print(f"Сессия создана: {session_id}")
        
        # Сохраняем тестовую игру
        game_id = db.save_game("test_user", {"test": "data"})
        print(f"Игра сохранена: {game_id}")
        
        # Получаем статистику
        stats = db.get_user_stats("test_user")
        print(f"Статистика: {stats}")
    else:
        print("Ошибка аутентификации")