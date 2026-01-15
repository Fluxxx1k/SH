from flask import session, redirect, request
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.data.database_py.players import exists_player, create_player
from WebsiteEasiest.settings.web_config import denied_literals
from WebsiteEasiest.settings.website_settings import MIN_NAME_LEN, MAX_NAME_LEN


def register():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('register.html',
                           min_name_len = MIN_NAME_LEN,
                           max_name_len = MAX_NAME_LEN)

def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if any(char in username for char in denied_literals):
        return {'error': 'Username contains invalid characters'}, 400
    if password != confirm_password:
        return {'error': 'Passwords do not match'}, 400
    if exists_player(username):
        return {'error': 'Username already exists'}, 400
    cr_pl = create_player(username, password)
    if not cr_pl[0]:
        return {'error': cr_pl[1]}, 400
    else:
        session['username'] = username
        return {'redirect': url_for('lobby')}