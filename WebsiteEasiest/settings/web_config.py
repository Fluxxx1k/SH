import os
is_debug = True
try:
    is_server = os.uname().nodename == "SERVERNYA"
except AttributeError:
    is_server = True

denied_literals = {'\\', '/',
                   ':', '*',
                   '?', '"',
                   '<', '>',
                   '#', '$',
                   "'", '&',
                   '^', '+',
                   '`', '~'}

New_games_allowed = True
import secrets, os
SHUTDOWN_SERVER_TOKEN = os.getenv('SHUTDOWN_SERVER_TOKEN') or secrets.token_urlsafe(32)
