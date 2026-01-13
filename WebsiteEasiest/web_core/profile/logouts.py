from flask import session, redirect
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for as url_for


def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
