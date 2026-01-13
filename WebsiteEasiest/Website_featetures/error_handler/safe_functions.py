import flask
from flask import abort

from WebsiteEasiest.logger import logger


def safe_url_for(endpoint, **values):
    """Helper function to generate safe URLs"""
    try:
        return flask.url_for(endpoint, _external=True, **values)
    except Exception as e:
        logger.warning(f"Error in safe_url_for: {e}")
        return '#'

def safe_render_template(template_name, **context):
    """Helper function to render templates safely"""
    try:
        return flask.render_template(template_name, safe_url_for=safe_url_for, url_for=safe_url_for, **context)
    except Exception as e:
        logger.warning(f"Error in safe_render_template: {repr(e)}\n"
              f"Template: {template_name}\n"
              f"Context: {context}")
        abort(500, repr(e))
