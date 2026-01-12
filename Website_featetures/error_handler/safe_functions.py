import flask
from flask import abort


def safe_url_for(endpoint, **values):
    """Helper function to generate safe URLs"""
    try:
        return flask.url_for(endpoint, _external=True, **values)
    except Exception as e:
        print(f"Error in safe_url_for: {e}")
        return '#'

def safe_render_template(template_name, **context):
    """Helper function to render templates safely"""
    try:
        return flask.render_template(template_name, safe_url_for=safe_url_for,**context)
    except Exception as e:
        print(f"Error in safe_render_template: {repr(e)}\n"
              f"Template: {template_name}\n"
              f"Context: {context}")
        from Website_featetures.error_handler.render_error import render_error_page
        abort(500, repr(e))
