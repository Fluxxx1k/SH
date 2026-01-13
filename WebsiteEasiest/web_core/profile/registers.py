from flask import session, redirect, request, abort
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for, render_template_abort_500 as render_template
from WebsiteEasiest.data.database_py.players import exists_player, create_player


def register():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('register.html')

def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password != confirm_password:
        abort(400, 'Passwords do not match')
    if exists_player(username):
        abort(400, 'Username already exists')
    cr_pl = create_player(username, password)
    if not cr_pl[0]:
        abort(400, cr_pl[1])
    else:
        session['username'] = username
        return redirect(url_for('lobby'))
