# Error handling functions
import functools

from flask import render_template, request, abort
from WebsiteEasiest.Website_featetures.error_handler.safe_functions import safe_url_for

def render_error_page(error_code, error_message=None, error_description=None, error_comment=None, suggestion=None,
                      debug_info=None):
    """Render error page with comprehensive error information"""
    try:
        return render_template('error.html',
                               error_code=error_code,
                               error_message=error_message,
                               error_description=error_description,
                               error_comment=error_comment,
                               suggestion=suggestion,
                               debug_info=debug_info,
                               config={'DEBUG': True},
                               safe_url_for=safe_url_for,)
    except Exception as e:
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
            <a href="{safe_url_for('index')}">На главную</a>
        </body>
        </html>
        """, error_code

# Custom error route for manual error display

def error():
    """Manual error display route"""
    try:
        error_code = request.args.get('error_code', request.args.get('code', 500, type=int), type=int)
        error_message = request.args.get('error_message', request.args.get('message'))
        error_description = request.args.get('error_description', request.args.get('description'))
        error_comment = request.args.get('error_comment', request.args.get('comment'))
        suggestion = request.args.get('suggestion')
        debug_info = request.args.get('debug_info')
    except:
        return render_error_page(error_code=500,
                                 error_message="Error code or error message",
                                 error_description="Error description or error comment",
                                 error_comment="Error description or error comment",
                                 suggestion="Error description or error comment",
                                 debug_info="Error description for debug or error comment")
    return render_error_page(
        error_code=error_code,
        error_message=error_message,
        error_description=error_description,
        error_comment=error_comment,
        suggestion=suggestion,
        debug_info=debug_info
    ), error_code


# Application-specific error handlers
def handle_game_error(error_message, error_code=400):
    """Handle games-specific errors"""
    return render_error_page(
        error_code=error_code,
        error_message="Ошибка в игре",
        error_description=error_message,
        error_comment="Проверьте правильность действий в игре.",
        suggestion="Попробуйте вернуться в лобби и начать заново."
    ), error_code


def handle_database_error(error_message):
    """Handle database errors"""
    return render_error_page(
        error_code=500,
        error_message="Ошибка базы данных",
        error_description="Произошла ошибка при работе с базой данных.",
        error_comment="Возможно, проблема с соединением или данными.",
        suggestion="Попробуйте обновить страницу. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=error_message
    ), 500



def safe_wrapper(func):
    """Wrapper for safe functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return render_error_page(
                error_code=500,
                error_message="Ошибка при вызове функции",
                error_description=str(e),
                error_comment="Возможно, проблема с параметрами функции.",
                suggestion="Попробуйте обновить страницу. Если ошибка повторяется, обратитесь к администратору.",
                debug_info=repr(e)
            ), 500
    return wrapper

def abort_on_exception(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            abort(500, repr(e))
    return wrapper

if __name__ == '__main__':
    print(error())