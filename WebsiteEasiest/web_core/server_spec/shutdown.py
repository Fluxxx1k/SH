from flask import request

from WebsiteEasiest.settings.web_config import SHUTDOWN_SERVER_TOKEN


def shutdown():
    if request.remote_addr not in ('127.0.0.1', '::1'):
        return "Access denied", 403
    if request.headers.get('X-Shutdown-Token') != SHUTDOWN_SERVER_TOKEN:
        return "Invalid token", 403
    shutdown_server()
    return "Shutting down...", 200

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()