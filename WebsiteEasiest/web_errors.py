# HTTP Error Handlers
import traceback

from flask import request, session

from WebsiteEasiest.stardard_renders import render_error_page
from logger import logger



def client_error(error):
    """Handle 4XX Client errors"""
    logger.error(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}\n{request.__dict__}\n{traceback.format_exc()}\n{session.__dict__}')
    return render_error_page(
        error_code=error.code,
        error_message=error.name,
        error_description=error.description,
        error_comment="Пожалуйста, проверьте ваш запрос и попробуйте еще раз.",
        suggestion="Если проблема persists, обратитесь к администратору сайта."
    ), error.code



def bad_request_error(error):
    """Handle 400 Bad Request errors"""
    logger.critical(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}\n{request.__dict__}, \n{traceback.format_exc()}\n{session.__dict__}')
    return render_error_page(
        error_code=400,
        error_message="Неверный запрос",
        error_description="Запрос содержит неверные данные или параметры.",
        error_comment="Проверьте правильность введенных данных.",
        suggestion="Попробуйте выполнить действие еще раз, проверив все введенные данные."
    ), 400


def unauthorized_error(error):
    """Handle 401 Unauthorized errors"""
    logger.debug(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=401,
        error_message="Необходима авторизация",
        error_description="Для доступа к этой странице необходимо войти в систему.",
        error_comment="Пожалуйста, авторизуйтесь, чтобы продолжить.",
        suggestion="Используйте форму входа или зарегистрируйтесь, если у вас еще нет аккаунта."
    ), 401

def forbidden_error(error):
    """Handle 403 Forbidden errors"""
    logger.debug(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=403,
        error_message="Доступ запрещен",
        error_description="У вас нет прав для доступа к этой странице или ресурсу.",
        error_comment="Возможно, вам нужно войти в систему или у вас недостаточно прав.",
        suggestion="Попробуйте войти в систему или обратитесь к администратору для получения необходимых прав."
    ), 403



def not_found_error(error):
    """Handle 404 Not Found errors"""
    logger.warning(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=404,
        error_message="Страница не найдена",
        error_description="Запрошенная страница не существует или была перемещена.",
        error_comment="Возможно, вы ввели неправильный адрес или страница была удалена.",
        suggestion="Проверьте правильность URL-адреса или вернитесь на главную страницу.",
        debug_info=repr(error),
    ), 404


def method_not_allowed_error(error):
    """Handle 405 Method Not Allowed errors"""
    if ('login' in str(request.path) or
        'register' in str(request.path)):
        logger.critical(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
        return render_error_page(
            error_code=405,
            error_message="Метод не разрешен",
            error_description="Используемый метод HTTP не разрешен для этого ресурса.",
            error_comment="Например, попытка отправить POST-запрос на страницу, которая принимает только GET-запросы.",
            suggestion="Вероятно, вы не можете войти или зарегистрироваться. Ошибка залогирована как критическая.",
            debug_info=repr(error),
        ), 405
    else:
        logger.error(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
        return render_error_page(
        error_code=405,
        error_message="Метод не разрешен",
        error_description="Используемый метод HTTP не разрешен для этого ресурса.",
        error_comment="Например, попытка отправить POST-запрос на страницу, которая принимает только GET-запросы.",
        suggestion="Попробуйте использовать другой метод или обратитесь к документации API."
    ), 405

def too_many_requests_error(error):
    """Handle 429 Too Many Requests errors"""
    logger.warning(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=429,
        error_message="Слишком много запросов",
        error_description="Вы превысили допустимое количество запросов в заданный период времени.",
        error_comment="Пожалуйста, повторите попытку позже.",
        suggestion="Попробуйте повторить запрос позже или обратитесь к администратору для увеличения лимита запросов."
    ), 429


def server_error(error):
    """Handle 5XX Server errors"""
    logger.error(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}\n{request.__dict__}\n{traceback.format_exc()}\n{session.__dict__}')
    return render_error_page(
        error_code=error.code,
        error_message=error.name,
        error_description=error.description,
        error_comment="Внутренняя ошибка сервера.",
        suggestion="Пожалуйста, попробуйте обновить страницу позже."
    ), error.code



def internal_server_error(handled_error: Exception) -> tuple[str, int]:
    """Handle 500 Internal Server errors"""
    import traceback
    logger.critical(f'[{request.remote_addr} -> {request.path}] ({request.method}) {handled_error}\n{request.__dict__}\n{traceback.format_exc()}\n{session.__dict__}')
    debug_info = traceback.format_exc()

    return render_error_page(
        error_code=500,
        error_message="Внутренняя ошибка сервера",
        error_description="Произошла ошибка на сервере при обработке вашего запроса.",
        error_comment="Мы уже работаем над решением этой проблемы.",
        suggestion="Попробуйте обновить страницу через несколько минут. Если ошибка повторяется, обратитесь к администратору.",
        debug_info=f"{debug_info} | {handled_error}"
    ), 500

def not_implemented_error(error):
    """Handle 501 Not Implemented errors"""
    logger.error(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=501,
        error_message="Функция не реализована",
        error_description="Запрошенный метод или функция не поддерживается сервером.",
        error_comment="Возможно, этот метод или функция еще не реализованы на сервере.",
        suggestion="Обратитесь к администратору для получения дополнительной информации."
    ), 501

def bad_gateway_error(error):
    """Handle 502 Bad Gateway errors"""
    logger.warning(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=502,
        error_message="Неверный шлюз",
        error_description="Сервер получает некорректный ответ от upstream-сервера.",
        error_comment="Возможно, проблема на стороне upstream-сервера или конфигурации прокси.",
        suggestion="Обратитесь к администратору для решения проблемы."
    ), 502

def service_unavailable_error(error):
    """Handle 503 Service Unavailable errors"""
    logger.warning(f'[{request.remote_addr} -> {request.path}] ({request.method}) {error}')
    return render_error_page(
        error_code=503,
        error_message="Сервис недоступен",
        error_description="Сервер временно недоступен, попробуйте позже.",
        error_comment="Возможно, сервер перегружен или находится в процессе обслуживания.",
        suggestion="Попробуйте повторить запрос позже."
    ), 503


