import os, time

from WebsiteEasiest.data.database_py.games import count_games, exists_game
from WebsiteEasiest.data.database_py.players import count_players
from WebsiteEasiest.logger import logger
from WebsiteEasiest.app_globs import app, socketio
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.Website_featetures.error_handler.render_error import abort_on_exception


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




app.route('/game/<game_name>/start', methods=['POST'])(abort_on_exception(game_base.game_start))

from WebsiteEasiest.web_core.server_spec.shutdown import shutdown_server


def mem_check():
    from psutil import Process
    curr_process = Process(os.getpid())
    memory_info = curr_process.memory_info().rss
    mem_check_count = 0
    mem_check_max_value = -1
    mem_check_min_value = 1 << 33
    mem_check_log_num = 3
    while memory_info < 1610612736:
        memory_info = curr_process.memory_info().rss
        mem_check_max_value = max(mem_check_max_value, memory_info)
        mem_check_min_value = min(mem_check_min_value, memory_info)
        if mem_check_count % mem_check_log_num == 0:
            logger.info(f"Memory check №{mem_check_count}: max {(mem_check_max_value >> 10) / 1024:.2f} MB, min {(mem_check_min_value >> 10) / 1024:.2f} MB, current {(memory_info >> 10) / 1024:.2f} MB")
            mem_check_max_value = -1
            mem_check_min_value = 1 << 33
        logger.debug(f"Memory usage №{mem_check_count}: {(memory_info >> 10) / 1024:.2f} MB")
        mem_check_count += 1
        if memory_info > 536870912: # 1 << 29
            if memory_info > 1342177280: # (1 << 30) * 1.25
                logger.critical(f"Memory usage exceeded 1.25 GB ({(memory_info >> 10) / 1024:.2f} MB)")
                try:
                    shutdown_server()
                    time.sleep(30)
                except BaseException as E:
                    logger.critical(f"Shutdown server failed with {(memory_info >> 10) / 1024: .2f} MB: {repr(E)}")
                else:
                    logger.critical(f"Shutdown server failed with {(memory_info >> 10) / 1024: .2f} MB with no response, hard kill!")
                finally:
                    os._exit(1)
            elif memory_info > 1073741824: # 1 << 30
                logger.error(f"Memory usage exceeded 1 GB ({(memory_info >> 10) / 1024:.2f} MB)")
            else:
                logger.warning(f"Memory usage exceeded 0.5 GB ({(memory_info >> 10) / 1024:.2f} MB)")
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
        time.sleep(600)
    try:
        shutdown_server()
        time.sleep(30)
    except BaseException as E:
        logger.critical(f"Shutdown server failed with {(memory_info >> 10) / 1024: .2f} MB: {repr(E)}")
    else:
        logger.critical(f"Shutdown server failed with {(memory_info >> 10) / 1024: .2f} MB with no response, hard kill!")
    finally:
        os._exit(1)


if __name__ == '__main__':
    import threading
    threading.Thread(target=mem_check, daemon=True).start()
    app.run(debug=False,
            host='0.0.0.0',
            port=20050,
            use_reloader=False)