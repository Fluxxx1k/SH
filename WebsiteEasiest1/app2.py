from flask import session, request

from WebsiteEasiest1.logger import logger
from Website_featetures.error_handler.safe_functions import safe_url_for
from app_globs import app, render_template, url_for

@app.route('/favicon.ico')
def favicon():
    return safe_url_for('static', filename='favicon.ico')

@app.route('/')
def index():
    logger.debug(f'index  |  [{request.remote_addr}] {"not logged in" if "username" not in session else session["username"]}')
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f'index  |  [{request.remote_addr}] {e}')
        return render_template('error.html', error=e), 500
