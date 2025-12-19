#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы обновления логов
"""

import requests
import json

def test_update_logs():
    """Тестируем обновление логов"""
    print("Тестируем обновление логов...")
    
    # Тестовые данные
    test_logs = [
        {
            'html_row': '<tr><td>1</td><td>Президент 1</td><td>Канцлер 1</td><td>красная, синяя</td><td>красную</td><td>синяя, красная</td><td>синюю</td><td>синюю</td><td>Нет</td></tr>',
            'data': 'Тестовый лог 1'
        },
        {
            'html_row': '<tr><td>2</td><td>Президент 2</td><td>Канцлер 2</td><td>синяя, красная</td><td>синюю</td><td>красная, синяя</td><td>красную</td><td>красную</td><td>Нет</td></tr>',
            'data': 'Тестовый лог 2'
        }
    ]
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/update_game_logs',
            json={'logs': test_logs},
            timeout=5
        )
        
        print(f"Статус ответа: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Результат: {result}")
            return result.get('success', False)
        else:
            print(f"Ошибка: статус {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что Flask сервер запущен.")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def test_get_logs():
    """Тестируем получение логов"""
    print("\nТестируем получение логов...")
    
    try:
        response = requests.get('http://127.0.0.1:5000/get_game_logs', timeout=5)
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Найдено записей: {len(result.get('game_table', ''))}")
            return True
        else:
            print(f"Ошибка: статус {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что Flask сервер запущен.")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("=== Тестирование интеграции SH2 с веб-сайтом ===")
    print("Убедитесь, что Flask сервер запущен (python app.py)")
    print()
    
    # Тестируем получение логов
    test_get_logs()
    
    # Тестируем обновление логов
    success = test_update_logs()
    
    if success:
        print("\n✓ Тест пройден успешно!")
        # Повторно получаем логи для проверки
        test_get_logs()
    else:
        print("\n✗ Тест не пройден.")