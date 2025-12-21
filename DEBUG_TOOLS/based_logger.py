from user_settings import DIRECTORY_FOR_CONSOLE_LOGS, NAME_FOR_CONSOLE_LOGS, EXTENSION_FOR_CONSOLE_LOGS, DATE_FORMAT
from console_logger import start_logging

full_path = start_logging(
    log_directory=DIRECTORY_FOR_CONSOLE_LOGS,
    log_name_prefix=NAME_FOR_CONSOLE_LOGS,
    log_extension=EXTENSION_FOR_CONSOLE_LOGS,
    date_format=DATE_FORMAT
)
