from flask import session, redirect, request, abort
from WebsiteEasiest.app_globs import url_for, render_template
from WebsiteEasiest.data.database_py.players import login_player


def login():
    if 'username' in session:
        return redirect(url_for('lobby'))
    return render_template('login.html')


def login_post():
    if 'username' in session:
        return redirect(url_for('lobby'))
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        abort(404, logging_in_player[1])
    else:
        session['username'] = username
        return redirect(url_for('lobby'))

