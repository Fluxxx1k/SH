from flask import request

from WebsiteEasiest.logger import logger
from WebsiteEasiest.settings.web_config import SHUTDOWN_SERVER_TOKEN


def shutdown():
    """
    Shutdown the server by POST request
    """
    logger.warning("Shutdown server requested by POST")
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if real_ip not in ('127.0.0.1', '::1'):
        return "Access denied", 403
    if request.headers.get('X-Shutdown-Token') != SHUTDOWN_SERVER_TOKEN:
        return "Invalid token", 403
    shutdown_server()
    return "Shutting down...", 200

def shutdown_server():
    logger.info("Shutting down server...")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()