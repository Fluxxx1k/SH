import logging
import sys, os
from logging.handlers import RotatingFileHandler

try:
    import cli.colors as color
except Exception as e:
    print(f"Could not import colors: {repr(e)}, using compability mode")
    class color:
        GRAY_BACKGROUND = "\033[100m"
        WHITE_BACKGROUND_BRIGHT = "\033[107m"
        YELLOW_BACKGROUND = "\033[43m"
        YELLOW_BACKGROUND_BRIGHT = "\033[103m"
        RED_BACKGROUND = "\033[41m"
        RED_BACKGROUND_VERY_BRIGHT = "\033[101m"
        END = '\033[0m'
        RESET_TEXT = '\033[39m'
        GRAY_TEXT = '\033[90m'
        BLACK_TEXT = '\033[30m'
        RED_TEXT = '\033[31m'
        RED_TEXT_VERY_BRIGHT = '\033[91m'
        YELLOW_TEXT = '\033[33m'
        YELLOW_TEXT_BRIGHT = '\033[93m'
        YELLOW_TEXT_VERY_BRIGHT = '\033[93m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

try:
    is_server = os.uname().nodename == "SERVERNYA"
except AttributeError:
    is_server = True
    
log_text = "%(asctime)s - %(message)s"
log_dir = os.path.join(os.path.dirname(__file__),"logger_logs")
low_debug_path = os.path.join(log_dir, "low_debug.log")
debug_path = os.path.join(log_dir, "debug.log")
info_path = os.path.join(log_dir, "info.log")
warning_path = os.path.join(log_dir, "warning.log")
error_path = os.path.join(log_dir, "error.log")
fatal_path = os.path.join(log_dir, "fatal.log")
all_path = os.path.join(log_dir, "all.log")
warning_error_fatal_path = os.path.join(log_dir, "warning_error_fatal.log")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 1. Определяем новый уровень (значение 5, ниже DEBUG=10)
LOW_DEBUG_NUM = 5
logging.addLevelName(LOW_DEBUG_NUM, "LOW_DEBUG")

class LowDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == LOW_DEBUG_NUM

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



# 3. Добавляем метод в класс Logger

# 4. Создаем логгер и настраиваем
logger = logging.getLogger("my_logger")
logger.setLevel(LOW_DEBUG_NUM)  # Ловим события от LOW_DEBUG и выше
# 2. Функция для добавления метода low_debug() к логгерам
def low_debug(message, *args, **kwargs):
    if logger.isEnabledFor(LOW_DEBUG_NUM):
        logger._log(LOW_DEBUG_NUM, message, args, **kwargs)

logger.low_debug = low_debug


class ColoredFormatterFile(logging.Formatter):
    """
    Logging Formatter to add colors to log messages
    """
    format = "%(asctime)s - %(message)s"

    FORMATS = {
        LOW_DEBUG_NUM: f'{color.GRAY_DARK_BACKGROUND+color.BLACK_TEXT if is_server else ""}LOW_DEBUG{color.END if is_server else ""} | {color.GRAY_DARK_TEXT if is_server else ""}{log_text}{color.END if is_server else ""}',
        logging.DEBUG: f'{color.GRAY_BACKGROUND if is_server else ""}DEBUG{color.END if is_server else ""}     | {color.GRAY_TEXT if is_server else ""}{log_text}{color.END if is_server else ""}',
        logging.INFO: f'{color.WHITE_BACKGROUND_BRIGHT+color.BLACK_TEXT if is_server else ""}INFO{color.END if is_server else ""}      | {log_text}{color.END if is_server else ""}',
        logging.WARNING: f'{color.YELLOW_BACKGROUND_BRIGHT if is_server else ""}{color.RED_TEXT if is_server else ""}WARNING{color.END if is_server else ""}   | {color.YELLOW_TEXT_BRIGHT if is_server else ""}{log_text}{color.END if is_server else ""}',
        logging.ERROR: f'{color.RED_BACKGROUND if is_server else ""}{color.BLACK_TEXT if is_server else ""}ERROR{color.END if is_server else ""}     | {color.RED_TEXT if is_server else ""}{log_text}{color.END if  is_server else ""} {{%(filename)s - %(funcName)s - %(lineno)d}}',
        logging.CRITICAL: f'{color.BOLD+color.UNDERLINE+color.RED_BACKGROUND_VERY_BRIGHT+color.YELLOW_TEXT_VERY_BRIGHT if is_server else ""}FATAL{color.END if is_server else ""}     | {color.RED_TEXT_VERY_BRIGHT if is_server else ""}{log_text}{color.END if is_server else ""} {{%(filename)s - %(funcName)s - %(lineno)d}}',
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        if log_fmt is None and record.levelno !=  logging.WARNING:
            logger.warning(f"Unknown log level: {record.levelno}")
            import pprint
            pprint.pprint(self.FORMATS)
            log_fmt = self.FORMATS[logging.WARNING]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class ColoredFormatterConsole(ColoredFormatterFile):
    FORMATS = {
        LOW_DEBUG_NUM: f'{color.GRAY_DARK_BACKGROUND+color.BLACK_TEXT}LOW_DEBUG{color.END} | {color.GRAY_DARK_TEXT}{log_text}{color.END}',
        logging.DEBUG: f'{color.GRAY_BACKGROUND}DEBUG{color.END}     | {color.GRAY_TEXT}{log_text}{color.END}',
        logging.INFO: f'{color.WHITE_BACKGROUND_BRIGHT + color.BLACK_TEXT}INFO{color.END}      | {log_text}{color.END}',
        logging.WARNING: f'{color.YELLOW_BACKGROUND_BRIGHT + color.RED_TEXT}WARNING{color.END}   | {color.YELLOW_TEXT_BRIGHT}{log_text}{color.END}',
        logging.ERROR: f'{color.RED_BACKGROUND + color.BLACK_TEXT}ERROR{color.END}     | {color.RED_TEXT}{log_text}{color.END} {{%(filename)s - %(funcName)s - %(lineno)d}}',
        logging.CRITICAL: f'{color.BOLD + color.UNDERLINE + color.RED_BACKGROUND_VERY_BRIGHT + color.YELLOW_TEXT_VERY_BRIGHT}FATAL{color.END}     | {color.RED_TEXT_VERY_BRIGHT}{log_text}{color.END} {{%(filename)s - %(funcName)s - %(lineno)d}}',
    }

all_handler = logging.StreamHandler(sys.stdout)
all_handler.setLevel(LOW_DEBUG_NUM)
all_handler.setFormatter(ColoredFormatterConsole())
logger.addHandler(all_handler)


low_debug_handler = RotatingFileHandler(
maxBytes=5<<20,  # 5MB
    backupCount=3,
    mode='a',
    filename=low_debug_path,
    encoding='utf-8')
low_debug_handler.setLevel(LOW_DEBUG_NUM)
low_debug_handler.addFilter(LowDebugFilter())
low_debug_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[LOW_DEBUG_NUM]
))
logger.addHandler(low_debug_handler)

debug_file_handler = RotatingFileHandler(
maxBytes=5<<20,  # 5MB
    backupCount=3,
    mode='a',
    filename=debug_path,
    encoding='utf-8')
debug_file_handler.setLevel(logging.DEBUG)
debug_file_handler.addFilter(DebugFilter())
debug_file_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[logging.DEBUG]
))

info_file_handler = RotatingFileHandler(
maxBytes=10<<20,  # 20MB
    backupCount=3,
    mode='a',
    filename=info_path,
    encoding='utf-8')
info_file_handler.setLevel(logging.INFO)
info_file_handler.addFilter(InfoFilter())
info_file_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[logging.INFO]
))
warning_file_handler = RotatingFileHandler(
maxBytes=5<<20,  # 5MB
    backupCount=3,
    mode='a',
    filename=warning_path,
    encoding='utf-8')
warning_file_handler.setLevel(logging.WARNING)
warning_file_handler.addFilter(WarningFilter())
warning_file_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[logging.WARNING]
))
error_file_handler = RotatingFileHandler(
maxBytes=5<<20,  # 5MB
    backupCount=3,
    mode='a',
    filename=error_path,
    encoding='utf-8')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.addFilter(ErrorFilter())
error_file_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[logging.ERROR]
))
fatal_file_handler = RotatingFileHandler(
maxBytes=5<<20,  # 5MB
    backupCount=3,
    mode='a',
    filename=fatal_path,
    encoding='utf-8')
fatal_file_handler.setLevel(logging.CRITICAL)
fatal_file_handler.addFilter(FatalFilter())
fatal_file_handler.setFormatter(logging.Formatter(
    ColoredFormatterFile.FORMATS[logging.CRITICAL]
))


logger.addHandler(debug_file_handler)
logger.addHandler(info_file_handler)
logger.addHandler(warning_file_handler)
logger.addHandler(error_file_handler)
logger.addHandler(fatal_file_handler)

all_file_handler = RotatingFileHandler(
    maxBytes=20<<20,  # 20MB
    backupCount=3,
    mode='a',
    filename=all_path,
    encoding='utf-8')
all_file_handler.setLevel(logging.DEBUG)
all_file_handler.setFormatter(ColoredFormatterFile())
logger.addHandler(all_file_handler)

warning_error_fatal_path_file_handler = RotatingFileHandler(
    maxBytes=20<<20,  # 20MB
    backupCount=3,
    mode='a',
    filename=warning_error_fatal_path,
    encoding='utf-8')
warning_error_fatal_path_file_handler.setLevel(logging.WARNING)
warning_error_fatal_path_file_handler.setFormatter(
    ColoredFormatterFile()
)
logger.addHandler(warning_error_fatal_path_file_handler)




logger.debug("Logger created and loaded")

if isinstance(color, type):
    logger.warning("Compatibility colors not supported, using ANSI codes")

if __name__ == "__main__":
    # Testing logs
    logger.low_debug("Low Debug log")
    logger.debug("Debug log")
    logger.info("Info log")
    logger.warning("Warning log")
    logger.error("Error log")
    logger.critical("Critical log")

