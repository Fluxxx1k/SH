from flask import request

from WebsiteEasiest.logger import logger
from WebsiteEasiest.web_config import is_debug
from Website_featetures.error_handler.safe_functions import safe_render_template
safe_errors = {404, 502, 429, 403, 401}


def render_error_page(error_code,
                      error_message=None,
                      error_description=None,
                      error_comment=None,
                      suggestion=None,
                      debug_info=None):
    (logger.debug if error_code in safe_errors else logger.warning)(f'''render_error_page {error_code= },
                               {error_message= },
                               {error_description= },
                               {error_comment= },
                               {suggestion= },
                               {debug_info= },
                               config= {{'DEBUG': {is_debug}}})''')
    """Render error page with comprehensive error information"""
    try:
        return safe_render_template('error.html',
                               error_code=error_code,
                               error_message=error_message,
                               error_description=error_description,
                               error_comment=error_comment,
                               suggestion=suggestion,
                               debug_info=debug_info,
                               config={'DEBUG': is_debug}), error_code
    except Exception as e:
        logger.fatal(f"Error rendering error page: {e}")
        # Fallback if error template fails
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Критическая ошибка {error_code}</title></head>
        <body>
            <h1>Критическая ошибка {e}</h1>
            <p>{error_message or 'Произошла ошибка'}</p>
            <p>{error_description or 'Произошла ошибка'}</p>
            <p>{error_comment or 'Нет дополнительной информации'}</p>
            <p>{suggestion or 'Нет совета'}</p>
            <p>{debug_info or 'Нет отладочной информации о изначальной ошибке'}</p>
            <p>{repr(e)}</p>
            <a href="/">На главную</a>
        </body>
        </html>
        """, error_code
