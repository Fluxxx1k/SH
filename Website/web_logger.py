def log_event(event: str):
    with open('web_log.txt', 'a') as file:
        file.write(f"{event}\n")

def error_log(error: BaseException, event: str):
    with open('web_logs/error_log.txt', 'a') as file:
        file.write(f"{repr(error)} raised during {event}\n")

