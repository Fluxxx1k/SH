"""
Пример использования функции обновления логов из SH2

Этот файл показывает, как можно использовать функцию обновления логов
на веб-сайте из основного приложения SH2.
"""

# Пример 1: Простое обновление логов
# from Website.sh2_integration import update_website_logs
# 
# def end_of_turn_sh2():
#     """Функция, вызываемая в конце хода в SH2"""
#     # Ваш существующий код...
#     
#     # Обновляем логи на сайте
#     if hasattr(globs, 'GAME_LOGS'):
#         success = update_website_logs(globs.GAME_LOGS)
#         if success:
#             print("Логи успешно обновлены на сайте")
#         else:
#             print("Не удалось обновить логи на сайте")

# Пример 2: Обновление с проверкой
# import sys
# sys.path.append('Website')
# from sh2_integration import update_website_logs
# 
# def update_game_logs_on_website():
#     """Функция для обновления логов игры на веб-сайте"""
#     try:
#         # Проверяем, есть ли логи
#         if hasattr(globs, 'GAME_LOGS') and globs.GAME_LOGS:
#             # Берем последние 20 записей
#             recent_logs = globs.GAME_LOGS[-20:]
#             
#             # Обновляем логи на сайте
#             success = update_website_logs(recent_logs)
#             
#             if success:
#                 print(f"✓ Логи игры обновлены на сайте ({len(recent_logs)} записей)")
#             else:
#                 print("✗ Не удалось обновить логи на сайте")
#                 
#     except Exception as e:
#         print(f"Ошибка при обновлении логов на сайте: {e}")

# Пример 3: Использование в конце хода
# def process_turn_end():
#     """Обработка конца хода с обновлением сайта"""
#     # Ваш код завершения хода...
#     
#     # Обновляем логи на сайте
#     try:
#         from Website.sh2_integration import update_website_logs
#         update_website_logs(globs.GAME_LOGS)
#     except:
#         pass  # Игнорируем ошибки веб-сайта, чтобы не прерывать игру

print("Примеры использования функции обновления логов для SH2:")
print("1. Импортируйте функцию: from Website.sh2_integration import update_website_logs")
print("2. Вызовите функцию в конце хода: update_website_logs(globs.GAME_LOGS)")
print("3. Функция вернет True при успешном обновлении, False при ошибке")