from flask import session, request, redirect, abort

from WebsiteEasiest.data.database_py.games import count_games
from WebsiteEasiest.data.database_py.players import count_players, login_player
from WebsiteEasiest.web_config import is_debug
from WebsiteEasiest.app_globs import app, render_template, url_for
from Website_featetures.error_handler.render_error import abort_on_exception


@app.route('/favicon.ico')
@abort_on_exception
def favicon():
    raise FileNotFoundError('Favicon not found')
    return url_for('static', filename='favicon.ico')

@app.route('/')
@abort_on_exception
def index():
    stats = {
        'active_games': count_games(),
        'complete_games': count_games(active=False),
        'total_players': count_players(),
        }
    return render_template('index.html', stats=stats)

@app.route('/login')
@abort_on_exception
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
@abort_on_exception
def login_post():
    if 'username' in session:
        return redirect(url_for('lobby'))
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        abort(400, logging_in_player[1])
    else:
        session['username'] = username
        return redirect(url_for('lobby'))

@app.route('/register')
@abort_on_exception
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=is_debug)
