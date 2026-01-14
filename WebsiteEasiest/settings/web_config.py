is_debug = True

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
