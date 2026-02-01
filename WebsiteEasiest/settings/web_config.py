import os, subprocess as sp
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
try:
    limit_games_count = int(sp.getoutput('ulimit -u'))
except ValueError as e:
    try:
        from WebsiteEasiest.logger import logger
        logger.error(f"Failed to get ulimit -u: {repr(e)}, using default value")
    except ImportError as e1:
        print(f"ERROR: cannot import logger: {e1}"
              "\n"f"cannot get ulimit -u: {repr(e)}, using default value")
    limit_games_count = 10
limit_games_count = min(limit_games_count, 10)

import secrets, os
SHUTDOWN_SERVER_TOKEN = os.getenv('SHUTDOWN_SERVER_TOKEN') or secrets.token_urlsafe(32)
