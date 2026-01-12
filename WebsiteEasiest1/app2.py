from flask import session, request, redirect, abort

from WebsiteEasiest1.data.database_py.games import count_games
from WebsiteEasiest1.data.database_py.players import count_players, login_player
from WebsiteEasiest1.logger import logger
from Website_featetures.error_handler.safe_functions import safe_url_for
from WebsiteEasiest1.app_globs import app, render_template, url_for

@app.route('/favicon.ico')
def favicon():
    return safe_url_for('static', filename='favicon.ico')

@app.route('/')
def index():
    logger.debug(f'index  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    stats = {
        'active_games': count_games(),
        'complete_games': count_games(active=False),
        'total_players': count_players(),
        }
    return render_template('index.html', stats=stats)

@app.route('/login')
def login():
    logger.debug(f'login  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    logger.debug(f'login_post  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    if 'username' in session:
        return redirect(safe_url_for('lobby'))
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        abort(400, logging_in_player[1])
    else:
        session['username'] = username
        return redirect(safe_url_for('lobby'))

@app.route('/register')
def register():
    logger.debug(f'register  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    return render_template('register.html')

def profile():
    logger.debug(f'profile  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
