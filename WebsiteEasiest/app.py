from flask import Flask, request, redirect

from Website_featetures.error_handler.safe_functions import *
from Website_featetures.error_handler.undefined import SilentUndefined
from WebsiteEasiest.data.database_work import exists_player, create_player, login_player
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.jinja_env.undefined = SilentUndefined



@app.route('/')
def index():
    return safe_render_template('index.html')
@app.route('/game')
def game():
    return safe_render_template('game.html')

@app.route('/login')
def login():
    return safe_render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    logging_in_player = login_player(username, password)
    if not logging_in_player[0]:
        return render_error_page(400, logging_in_player[1])
    else:
        return redirect(safe_url_for('lobby'))
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if exists_player(username):
        return render_error_page(400, 'Username already exists')
    if password != confirm_password:
        return render_error_page(400, 'Passwords do not match')
    if len(password) < 3:
        return render_error_page(400, 'Password must be at least 3 characters long')
    # if not any(char.isdigit() for char in password):
    #     return render_error_page(400, 'Password must contain at least one digit')
    # if not any(char.isupper() for char in password):
    #     return render_error_page(400, 'Password must contain at least one uppercase letter')
    # if not any(char.islower() for char in password):
    #     return render_error_page(400, 'Password must contain at least one lowercase letter')
    # if not any(char in '!@#$%^&*()-_=+[]{}|;:\'",.<>/?' for char in password):
    #     return render_error_page(400, 'Password must contain at least one special character')
    creating_player = create_player(username, password)
    if creating_player[0]:
        return redirect(safe_url_for('login'))
    else:
        return render_error_page(400, creating_player[1])
@app.route('/logout')
def logout():
    return safe_render_template('logout.html')
@app.route('/register')
def register():
    return safe_render_template('register.html')
@app.route('/lobby')
def lobby():
    return safe_render_template('lobby.html')


def render_error_page(error_code, error_message=None, error_description=None, error_comment=None, suggestion=None,
                      debug_info=None):
    """Render error page with comprehensive error information"""
    try:
        return safe_render_template('error.html',
                               error_code=error_code,
                               error_message=error_message,
                               error_description=error_description,
                               error_comment=error_comment,
                               suggestion=suggestion,
                               debug_info=debug_info,
                               config={'DEBUG': app.debug})
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


# HTTP Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    return render_error_page(
        error_code=404,
        error_message="Страница не найдена",
        error_description="Запрошенная страница не существует или была перемещена.",
        error_comment="Возможно, вы ввели неправильный адрес или страница была удалена.",
        suggestion="Проверьте правильность URL-адреса или вернитесь на главную страницу."
    ), 404


@app.errorhandler(500)
def internal_error(handled_error: Exception):
    """Handle 500 Internal Server errors"""
    import traceback
    debug_info = None
    if app.debug:
        debug_info = traceback.format_exc()

    return render_error_page(
        error_code=500,
        error_message="Внутренняя ошибка сервера",
        error_description="Произошла ошибка на сервере при обработке вашего запроса.",
        error_comment="Мы уже работаем над решением этой проблемы.",
        suggestion="Попробуйте обновить страницу через несколько минут. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=f"{debug_info} | {handled_error}"
    ), 500


@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors"""
    return render_error_page(
        error_code=403,
        error_message="Доступ запрещен",
        error_description="У вас нет прав для доступа к этой странице или ресурсу.",
        error_comment="Возможно, вам нужно войти в систему или у вас недостаточно прав.",
        suggestion="Попробуйте войти в систему или обратитесь к администратору для получения необходимых прав."
    ), 403


@app.errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized errors"""
    return render_error_page(
        error_code=401,
        error_message="Необходима авторизация",
        error_description="Для доступа к этой странице необходимо войти в систему.",
        error_comment="Пожалуйста, авторизуйтесь, чтобы продолжить.",
        suggestion="Используйте форму входа или зарегистрируйтесь, если у вас еще нет аккаунта."
    ), 401


@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors"""
    return render_error_page(
        error_code=400,
        error_message="Неверный запрос",
        error_description="Запрос содержит неверные данные или параметры.",
        error_comment="Проверьте правильность введенных данных.",
        suggestion="Попробуйте выполнить действие еще раз, проверив все введенные данные."
    ), 400


@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle 405 Method Not Allowed errors"""
    return render_error_page(
        error_code=405,
        error_message="Метод не разрешен",
        error_description="Используемый метод HTTP не разрешен для этого ресурса.",
        error_comment="Например, попытка отправить POST-запрос на страницу, которая принимает только GET-запросы.",
        suggestion="Попробуйте использовать другой метод или обратитесь к документации API."
    ), 405


# Custom error route for manual error display
@app.route('/error')
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
        debug_info=error_message if app.debug else None
    ), 500

if __name__ == '__main__':
    app.run(debug=True)
