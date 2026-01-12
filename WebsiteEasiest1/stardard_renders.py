from flask import request

from WebsiteEasiest1.logger import logger
from WebsiteEasiest1.web_config import is_debug
from Website_featetures.error_handler.safe_functions import safe_render_template



def render_error_page(error_code,
                      error_message=None,
                      error_description=None,
                      error_comment=None,
                      suggestion=None,
                      debug_info=None):
    logger.debug(f'''render_error_page {error_code= },
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
                               config={'DEBUG': is_debug})
    except Exception as e:
        logger.error(f"Error rendering error page: {e}")
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

# Custom error route for manual error display

def error():
    """Manual error display route"""
    error_code = request.args.get('error_code', request.args.get('code', 500, type=int), type=int)
    error_message = request.args.get('error_message', request.args.get('message'))
    error_description = request.args.get('error_description', request.args.get('description'))
    error_comment = request.args.get('error_comment', request.args.get('comment'))
    suggestion = request.args.get('suggestion')
    debug_info = request.args.get('debug_info')

    return render_error_page(
        error_code=error_code,
        error_message=error_message,
        error_description=error_description,
        error_comment=error_comment,
        suggestion=suggestion,
        debug_info=debug_info
    ), error_code

