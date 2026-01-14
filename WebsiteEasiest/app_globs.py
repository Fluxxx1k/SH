from flask import Flask

from WebsiteEasiest.settings.web_config import is_debug
from WebsiteEasiest.web_errors import *
from WebsiteEasiest.web_loggers import log_response, log_request

app = Flask(__name__)
app.debug = is_debug

app.secret_key = 'your_secret_key_here'
from WebsiteEasiest.Website_featetures.error_handler.undefined import SilentUndefined
app.jinja_env.undefined = SilentUndefined

app.before_request(log_request)
app.after_request(log_response)
app.errorhandler(400)(bad_request_error)
app.errorhandler(401)(unauthorized_error)
app.errorhandler(403)(forbidden_error)
app.errorhandler(404)(not_found_error)
app.errorhandler(405)(method_not_allowed_error)
app.errorhandler(429)(too_many_requests_error)


for code in {406, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 428, 431, 451,}:
    try:
        app.errorhandler(code)(client_error)
    except Exception as e:
        logger.warning(f'Error registering error handler for code {code}: {e}')

app.errorhandler(500)(internal_server_error)
app.errorhandler(501)(not_implemented_error)
app.errorhandler(502)(bad_gateway_error)
app.errorhandler(503)(service_unavailable_error)