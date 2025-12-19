from flask import Flask, render_template, jsonify, request
from jinja2 import Undefined
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import globs
    from HTML_logs import GameLog, create_HTML_logs_cards_for_Website
except ImportError:
    # Заглушки для тестирования без SH2 модулей
    globs = None
    GameLog = None
    create_HTML_logs_cards_for_Website = lambda: "<p>Логи временно недоступны</p>"

app = Flask(__name__, static_folder='static')

# Глобальная переменная для кэширования логов
game_logs_cache = []
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
@app.route('/')
@app.route('/index.html')
@app.route('/index')
@app.route('/main.html')
@app.route('/main')
def index():
    return render_template('index.html',
                           )

# Функция для обновления логов с внешнего источника (SH2)
def update_website_logs(new_logs):
    """Функция для обновления логов игры из SH2"""
    global game_logs_cache
    if new_logs and isinstance(new_logs, list):
        game_logs_cache = new_logs
        return True
    return False

@app.route('/game')
@app.route('/game.html')
def game():
    return render_template('account.html',
                           safelog = create_HTML_logs_cards_for_Website(),


    )

@app.route('/game_logs')
def game_logs():
    game_table = ""
    # Используем кэшированные логи или globs.GAME_LOGS
    logs_source = game_logs_cache if game_logs_cache else (globs.GAME_LOGS if hasattr(globs, 'GAME_LOGS') else [])
    
    if logs_source:
        recent_logs = logs_source[-20:]  # Показываем последние 20 записей
        game_table = "<table>"
        game_table += "<thead><tr><th>N</th><th>Президент</th><th>Канцлер</th><th>Карты президента</th><th>Сказал президент</th><th>Карты канцлера</th><th>Сказал канцлер</th><th>Положил канцлер</th><th>Особое действие</th></tr></thead>"
        game_table += "<tbody>"
        for log in recent_logs:
            if hasattr(log, 'to_HTML_row_Website'):
                game_table += log.to_HTML_row_Website()
            else:
                game_table += f"<tr><td colspan='9'>Лог: {str(log)}</td></tr>"
        game_table += "</tbody></table>"
    else:
        game_table = '<div class="no-logs"><h3>🎮 Логи игры пока не доступны</h3><p>Игра ещё не началась или логи ещё не были загружены.</p><p>Логи появятся здесь автоматически, как только начнётся игра.</p></div>'
    return render_template('game_logs.html', game_table=game_table)

@app.route('/get_game_logs')
def get_game_logs():
    """Функция для AJAX запросов на получение обновленных логов"""
    game_table = ""
    # Используем кэшированные логи или globs.GAME_LOGS
    logs_source = game_logs_cache if game_logs_cache else (globs.GAME_LOGS if hasattr(globs, 'GAME_LOGS') else [])
    
    if logs_source:
        recent_logs = logs_source[-20:]  # Показываем последние 20 записей
        game_table = "<table>"
        game_table += "<thead><tr><th>N</th><th>Президент</th><th>Канцлер</th><th>Карты президента</th><th>Сказал президент</th><th>Карты канцлера</th><th>Сказал канцлер</th><th>Положил канцлер</th><th>Особое действие</th></tr></thead>"
        game_table += "<tbody>"
        for log in recent_logs:
            if hasattr(log, 'to_HTML_row_Website'):
                game_table += log.to_HTML_row_Website()
            else:
                game_table += f"<tr><td colspan='9'>Лог: {str(log)}</td></tr>"
        game_table += "</tbody></table>"
    else:
        game_table = '<div class="no-logs"><h3>🎮 Логи игры пока не доступны</h3><p>Игра ещё не началась или логи ещё не были загружены.</p><p>Логи появятся здесь автоматически, как только начнётся игра.</p></div>'
    return jsonify({"success": True, "game_table": game_table})

@app.route('/update_game_logs', methods=['POST'])
def update_game_logs():
    """Маршрут для обновления логов игры из SH2"""
    try:
        data = request.get_json()
        if data and 'logs' in data:
            success = update_website_logs(data['logs'])
            return jsonify({"success": success, "message": "Логи обновлены" if success else "Ошибка при обновлении логов"})
        else:
            return jsonify({"success": False, "message": "Нет данных для обновления"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Ошибка: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)