from flask import session, redirect, request
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.data.database_py.players import login_player
from WebsiteEasiest.settings.website_settings import MIN_NAME_LEN, MAX_NAME_LEN


def login():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('login.html',
                           min_name_len = MIN_NAME_LEN,
                           max_name_len = MAX_NAME_LEN)


def login_post():
    if 'username' in session:
        return {'redirect': url_for('lobby')}
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        return {'error': logging_in_player[1]}, 400
    else:
        session['username'] = username
        return {'redirect': url_for('lobby')}