import sys
import os
from datetime import datetime

from user_settings import DATE_FORMAT, EXTENSION_FOR_CONSOLE_LOGS, NAME_FOR_CONSOLE_LOGS, DIRECTORY_FOR_CONSOLE_LOGS


class Logger:
    def __init__(self, filename, old_stdout):
        self.terminal = old_stdout
        self.log = open(filename, "a", encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

def start_logging(log_directory=DIRECTORY_FOR_CONSOLE_LOGS,
    log_name_prefix=NAME_FOR_CONSOLE_LOGS,
    log_extension=EXTENSION_FOR_CONSOLE_LOGS,
    date_format=DATE_FORMAT):
    date = datetime.now().strftime(date_format)
    try:
        os.makedirs(log_directory, exist_ok=True)
        check_logs = os.listdir(log_directory)
    except Exception as e:
        sys.stderr.write(f"Error creating log directory: {e}\nLogs won't be created\n")
        return

    try:
        logs_nums = []
        for i in check_logs:
            if i.startswith(log_name_prefix + date):
                logs_nums.append(i)
        max_log_num = len(logs_nums) + 1
        full_path = os.path.join(log_directory, log_name_prefix + date + str(max_log_num) + log_extension)
        while os.path.exists(full_path):
            max_log_num += 1
            print(f"Log file {full_path} already exists, trying next number: {max_log_num}")
            full_path = os.path.join(log_directory, log_name_prefix + date + str(max_log_num) + log_extension)
        
        open(full_path, 'w+', encoding='utf-8').close()
        
        print(f"Console logs will be saved to: {full_path}")

    except Exception as e:
        sys.stderr.write(f"Error setting up log file: {e}\nConsole logging disabled.\n")
        full_path = None

    if full_path:
        original_stdout = sys.stdout
        sys.stdout = Logger(full_path, original_stdout)
        sys.stderr = sys.stdout
        print(0)
        try:
            if isinstance(__builtins__, dict):
                original_input = __builtins__['input']
            else:
                original_input = __builtins__.input

            def logged_input(prompt=""):
                user_input = original_input(prompt)
                sys.stdout.log.write(user_input + '\n')
                sys.stdout.log.flush()
                return user_input

            if isinstance(__builtins__, dict):
                __builtins__['input'] = logged_input
            else:
                __builtins__.input = logged_input
        except (AttributeError, KeyError) as e:
            sys.stderr.write(f"Failed to wrap input for logging: {e}\n")
        return full_path
    return None