from flask import session, redirect
from WebsiteEasiest.app_globs import url_for


def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
