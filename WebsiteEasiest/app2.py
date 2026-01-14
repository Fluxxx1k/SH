import os, time

from flask import abort, session
from flask_socketio import emit

from WebsiteEasiest.data.database_py.games import count_games, exists_game
from WebsiteEasiest.data.database_py.players import count_players
from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import is_debug
from WebsiteEasiest.app_globs import app, socketio
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.Website_featetures.error_handler.render_error import abort_on_exception
from cli.colors import RED_BACKGROUND_BRIGHT, GREEN_BACKGROUND_BRIGHT, RESET


@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/main')
@app.route('/main.html')
@abort_on_exception
def index():
    stats = {
        'active_games': count_games(),
        'complete_games': count_games(active=False),
        'total_players': count_players(),
        }
    return render_template('index.html', stats=stats)

from WebsiteEasiest.web_core.profile import logins
app.route('/login')(abort_on_exception(logins.login))
app.route('/login', methods=['POST'])(abort_on_exception(logins.login_post))

from WebsiteEasiest.web_core.profile import registers
app.route('/register')(abort_on_exception(registers.register))
app.route('/register', methods=['POST'])(abort_on_exception(registers.register_post))

from WebsiteEasiest.web_core.profile import logouts
app.route('/logout')(abort_on_exception(logouts.logout))

from WebsiteEasiest.web_core.games_work import lobbies
app.route('/lobby')(abort_on_exception(lobbies.lobby))

from WebsiteEasiest.web_core.games_work import game_creation
app.route('/create_game')(abort_on_exception(game_creation.create_game))
app.route('/create_game', methods=['POST'])(abort_on_exception(game_creation.create_game_post))

from WebsiteEasiest.web_core.games_work import game_base
app.route('/game/<game_name>')(abort_on_exception(game_base.game))
app.route('/game/<game_name>', methods=['POST'])(game_base.game_post)
app.route('/game/<game_name>/vote', methods=['POST'])(game_base.game_vote)



# Handle WebSocket connections
@app.route('/game/<game_name>/ws')
def game_ws(game_name):
    if 'username' not in session:
        abort(401, description="Необходимо войти в систему")
    if game_name == '':
        abort(400, description="Имя игры не может быть пустым")
    if not exists_game(game_name):
        abort(404, description=f"Игра {game_name} не найдена")
    @socketio.on('connect', namespace=f'/game/{game_name}')
    def handle_connect():
        emit('status', {'message': 'Connected to game room'})

app.route('/game/<game_name>/start', methods=['POST'])(abort_on_exception(game_base.game_start))

from WebsiteEasiest.web_core.server_spec.shutdown import shutdown_server


def mem_check():
    from psutil import Process
    curr_process = Process(os.getpid())
    memory_info = curr_process.memory_info().rss
    while memory_info < (1 << 32):
        memory_info = curr_process.memory_info().rss
        time.sleep(5)
        logger.debug(f"Memory usage: {memory_info / (1 << 20):.2f} MB")
        if memory_info > (1 << 30):
            if memory_info > (1 << 31):
                logger.critical(f"Memory usage exceeded 2 GB ({memory_info / (1 << 20):.2f} MB)")
                try:
                    shutdown_server()
                    time.sleep(30)
                except BaseException as E:
                    logger.critical(f"Shutdown server failed: {repr(E)} 2 GB")
                else:
                    logger.critical(f"Shutdown server failed with no response, hard kill 2 GB")
                finally:
                    os._exit(1)
            if memory_info > ((1 << 30) + (1 << 29)):
                logger.error(f"Memory usage exceeded 1.5 GB ({memory_info / (1 << 20):.2f} MB)")
            else:
                logger.warning(f"Memory usage exceeded 1 GB ({memory_info / (1 << 20):.2f} MB)")
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
    try:
        shutdown_server()
        time.sleep(30)
    except BaseException as E:
        logger.critical(f"Shutdown server failed 4 GB: {repr(E)}")
    else:
        logger.critical(f"Shutdown server failed with no response, hard kill 4 GB")
    finally:
        os._exit(1)


if __name__ == '__main__':
    import threading
    threading.Thread(target=mem_check, daemon=True).start()
    app.run(debug=False,
            host='0.0.0.0',
            port=20050,
            use_reloader=False)