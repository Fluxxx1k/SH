import os
from functools import cache
import subprocess

@cache
def get_color_count():
    """Получает количество поддерживаемых цветов"""
    try:
        result = subprocess.run(
            ['tput', 'colors'],
            capture_output=True,
            text=True,
            check=True
        )
        color_count = int(result.stdout.strip())
        return color_count
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return 0

@cache
def supports_256_colors():
    if get_color_count() >= 256:
        return True
    """Проверяет поддержку 256 цветов"""
    # Проверяем переменные окружения
    term = os.environ.get('TERM', '').lower()
    # Терминалы с поддержкой 256 цветов обычно содержат:
    # - '256color' в TERM
    # - Или являются известными терминалами с поддержкой
    if '256color' in term or 'rgb' in term:
        return True

    # Список терминалов, которые обычно поддерживают 256 цветов
    known_256_terms = [
        'alacritty',
        'kitty',
        'wezterm',
        'gnome-terminal',
        'konsole',
        'terminator',
    ]

    return any(t in term for t in known_256_terms)


def get_best_color_code(base_color_16, color_256):
    """Возвращает лучший доступный цвет"""
    if True or supports_256_colors():
        return color_256
    else:
        return base_color_16
