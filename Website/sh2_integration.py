"""
Модуль для интеграции с SH2.
Содержит функции для обновления логов игры на веб-сайте
"""

import requests
import json
from typing import List, Any

def update_website_logs(game_logs: List[Any]) -> bool:
    """
    Функция для обновления логов игры на веб-сайте из SH2
    
    Args:
        game_logs: Список объектов GameLog из globs.GAME_LOGS
        
    Returns:
        bool: True если обновление прошло успешно, False в противном случае
    """
    try:
        # Подготавливаем данные для отправки
        logs_data = [log.__dict__ for log in game_logs]
        
        # Отправляем POST запрос на сервер Flask
        response = requests.post(
            'http://127.0.0.1:5000/update_game_logs',
            json={'logs': logs_data},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('success', False)
        else:
            print(f"Ошибка при обновлении логов: статус {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при обновлении логов: {e}")
        return False
    except Exception as e:
        print(f"Ошибка при обновлении логов: {e}")
        return False

def get_website_logs() -> str:
    """
    Функция для получения текущих логов с веб-сайта
    
    Returns:
        str: HTML таблица с логами или сообщение об ошибке
    """
    try:
        response = requests.get('http://127.0.0.1:5000/get_game_logs', timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result.get('game_table', '')
        else:
            return f"<p>Ошибка получения логов: статус {response.status_code}</p>"
    except Exception as e:
        return f"<p>Ошибка получения логов: {e}</p>"

# Пример использования:
# from sh2_integration import update_website_logs
# update_website_logs(globs.GAME_LOGS)