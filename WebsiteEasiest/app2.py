from WebsiteEasiest.data.database_py.games import count_games, exists_game, save_data_of_game
from WebsiteEasiest.data.database_py.players import count_players
from WebsiteEasiest.app_globs import app
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
app.route('/lobby/leave', methods=['POST'])(abort_on_exception(lobbies.game_leave))



from WebsiteEasiest.web_core.games_work import game_creation
app.route('/create_game')(abort_on_exception(game_creation.create_game))
app.route('/create_game', methods=['POST'])(abort_on_exception(game_creation.create_game_post))

from WebsiteEasiest.web_core.games_work import game_base
app.route('/game/<game_name>')(abort_on_exception(game_base.game))
app.route('/game/<game_name>', methods=['POST'])(abort_on_exception(game_base.game_post))
app.route('/game/<game_name>/vote', methods=['POST'])(abort_on_exception(game_base.game_vote))
app.route('/game/<game_name>/join', methods=['POST'])(abort_on_exception(game_base.game_join))
# app.route('/game/<game_name>/start', methods=['POST'])(abort_on_exception(game_base.game_start))

from WebsiteEasiest.memory_checker import mem_check, memory_info


if __name__ == '__main__':
    import threading
    threading.Thread(target=mem_check, daemon=True).start()
    app.run(debug=False,
            host='0.0.0.0',
            port=20050,
            use_reloader=False)