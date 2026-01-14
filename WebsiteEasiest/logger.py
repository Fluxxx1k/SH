import logging
import sys, os
from logging.handlers import RotatingFileHandler
# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_text = "%(asctime)s - %(message)s"
log_dir = os.path.join(os.path.dirname(__file__),"logger_logs")
debug_path = os.path.join(log_dir, "debug.log")
info_path = os.path.join(log_dir, "info.log")
warning_path = os.path.join(log_dir, "warning.log")
error_path = os.path.join(log_dir, "error.log")
fatal_path = os.path.join(log_dir, "fatal.log")
all_path = os.path.join(log_dir, "all.log")
warning_error_fatal_path = os.path.join(log_dir, "warning_error_fatal.log")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.DEBUG

class InfoFilter(logging.Filter):
    def filter(self, record):
        return logging.DEBUG < record.levelno <= logging.INFO

class WarningFilter(logging.Filter):
    def filter(self, record):
        return logging.INFO < record.levelno <= logging.WARNING

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return logging.WARNING < record.levelno <= logging.ERROR

class FatalFilter(logging.Filter):
    def filter(self, record):
        return logging.ERROR < record.levelno



debug_handler = logging.StreamHandler(sys.stdout)
debug_handler.setLevel(logging.DEBUG)
debug_handler.addFilter(DebugFilter())
debug_handler.setFormatter(logging.Formatter(
    f'\033[90m{log_text}\033[39m'
))

info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.addFilter(InfoFilter())
info_handler.setFormatter(logging.Formatter(
    f'\033[39m{log_text}\033[39m'
))

warning_handler = logging.StreamHandler(sys.stderr)
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(WarningFilter())
warning_handler.setFormatter(logging.Formatter(
    f'\033[93m{log_text}\033[39m'
))

error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(ErrorFilter())
error_handler.setFormatter(logging.Formatter(
    f'\033[31m{log_text}\033[39m'
))

fatal_handler = logging.StreamHandler(sys.stderr)
fatal_handler.setLevel(logging.CRITICAL)
fatal_handler.addFilter(FatalFilter())
fatal_handler.setFormatter(logging.Formatter(
    f'\033[101m{log_text}\033[49m'
))

logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(fatal_handler)


debug_file_handler = RotatingFileHandler(
maxBytes=5*1024*1024,  # 5MB
    backupCount=3,
    mode='a',
    filename=debug_path,
    encoding='utf-8')
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.addFilter(DebugFilter())
debug_file_handler.setFormatter(logging.Formatter(
    f'DEBUG | {log_text}'
))

info_file_handler = RotatingFileHandler(
maxBytes=10*1024*1024,  # 20MB
    backupCount=3,
    mode='a',
    filename=info_path,
    encoding='utf-8')
info_file_handler.setLevel(logging.INFO)
info_file_handler.addFilter(InfoFilter())
info_file_handler.setFormatter(logging.Formatter(
    f'INFO  | {log_text}'
))
warning_file_handler = RotatingFileHandler(
maxBytes=5*1024*1024,  # 5MB
    backupCount=3,
    mode='a',
    filename=warning_path,
    encoding='utf-8')
warning_file_handler.setLevel(logging.WARNING)
warning_file_handler.addFilter(WarningFilter())
warning_file_handler.setFormatter(logging.Formatter(
    f'WARNING| {log_text}'
))
error_file_handler = RotatingFileHandler(
maxBytes=5*1024*1024,  # 5MB
    backupCount=3,
    mode='a',
    filename=error_path,
    encoding='utf-8')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.addFilter(ErrorFilter())
error_file_handler.setFormatter(logging.Formatter(
    f'ERROR | {log_text} {{%(filename)s - %(funcName)s - %(lineno)d}}'))
fatal_file_handler = RotatingFileHandler(
maxBytes=5*1024*1024,  # 5MB
    backupCount=3,
    mode='a',
    filename=fatal_path,
    encoding='utf-8')
fatal_file_handler.setLevel(logging.CRITICAL)
fatal_file_handler.addFilter(FatalFilter())
fatal_file_handler.setFormatter(logging.Formatter(
    f'FATAL | {log_text} {{%(filename)s - %(funcName)s - %(lineno)d}}'
))


logger.addHandler(debug_file_handler)
logger.addHandler(info_file_handler)
logger.addHandler(warning_file_handler)
logger.addHandler(error_file_handler)
logger.addHandler(fatal_file_handler)


all_file_handler = RotatingFileHandler(
    maxBytes=20*1024*1024,  # 20MB
    backupCount=3,
    mode='a',
    filename=all_path,
    encoding='utf-8')
all_file_handler.setLevel(logging.DEBUG)
all_file_handler.setFormatter(logging.Formatter(f'%(levelname)s | {log_text}'))
logger.addHandler(all_file_handler)

warning_error_fatal_path_file_handler = RotatingFileHandler(
    maxBytes=20*1024*1024,  # 20MB
    backupCount=3,
    mode='a',
    filename=warning_error_fatal_path,
    encoding='utf-8')
warning_error_fatal_path_file_handler.setLevel(logging.WARNING)
warning_error_fatal_path_file_handler.setFormatter(
    logging.Formatter(
        f'%(levelname)s | {log_text} {{%(filename)s - %(funcName)s - %(lineno)d}}'
    )
)
logger.addHandler(warning_error_fatal_path_file_handler)




logger.debug("Logger created and loaded")



