from flask import Flask, render_template

from WebsiteEasiest1.web_errors import *
from WebsiteEasiest1.web_loggers import log_response, log_request

app = Flask(__name__)
app.debug = True

app.secret_key = 'your_secret_key_here'
if not app.debug:
    from Website_featetures.error_handler.undefined import SilentUndefined
    app.jinja_env.undefined = SilentUndefined
    from Website_featetures.error_handler.safe_functions import (
    safe_render_template as render_template,
    safe_url_for as url_for)
else:
    from flask import render_template, url_for

app.before_request(log_request)
app.after_request(log_response)
app.errorhandler(400)(bad_request_error)
app.errorhandler(401)(unauthorized_error)
app.errorhandler(403)(forbidden_error)
app.errorhandler(404)(not_found_error)
app.errorhandler(405)(method_not_allowed_error)
app.errorhandler(429)(too_many_requests_error)
app.errorhandler(500)(internal_server_error)
app.errorhandler(501)(not_implemented_error)
# app.errorhandler(502)(bad_gateway_error)
app.errorhandler(503)(service_unavailable_error)

