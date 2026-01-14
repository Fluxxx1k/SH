from flask import session, redirect, request, abort
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.data.database_py.players import exists_player, create_player
from WebsiteEasiest.settings.web_config import denied_literals


def register():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('register.html')

def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if any(char in username for char in denied_literals):
        return render_template('register.html', error='Username contains invalid characters')
    if password != confirm_password:
        return render_template('register.html', error='Passwords do not match')
    if exists_player(username):
        return render_template('register.html', error='Username already exists')
    cr_pl = create_player(username, password)
    if not cr_pl[0]:
        return render_template('register.html', error=cr_pl[1])
    else:
        session['username'] = username
        return redirect(url_for('lobby'))