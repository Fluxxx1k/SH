from flask import session, request, redirect, abort

from WebsiteEasiest.data.database_py.games import count_games
from WebsiteEasiest.data.database_py.players import count_players, login_player, exists_player, create_player
from WebsiteEasiest.profile.logins import login_post, login
from WebsiteEasiest.profile.logouts import logout
from WebsiteEasiest.profile.registers import register, register_post
from WebsiteEasiest.web_config import is_debug
from WebsiteEasiest.app_globs import app, render_template, url_for
from Website_featetures.error_handler.render_error import abort_on_exception


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

app.route('/login')(abort_on_exception(login))
app.route('/login', methods=['POST'])(abort_on_exception(login_post))
app.route('/register')(abort_on_exception(register))
app.route('/register', methods=['POST'])(abort_on_exception(register_post))
app.route('/logout')(abort_on_exception(logout))



if __name__ == '__main__':
    app.run(debug=is_debug)
