from flask import request

from app_globs import app
from cli.colors import (YELLOW_TEXT_BRIGHT,
                        RESET_TEXT,
                        GREEN_TEXT_BRIGHT,
                        RED_TEXT_BRIGHT,
                        GREEN_TEXT,
                        YELLOW_TEXT)

@app.before_request
def log_request():
    print(f"[{YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}] {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    match response.status_code // 100:
        case 2:
            color = GREEN_TEXT_BRIGHT
        case 4 | 5:
            color = RED_TEXT_BRIGHT
        case 3:
            if response.status_code == 304:
                color = GREEN_TEXT
            else:
                color = YELLOW_TEXT
        case _:
            color = YELLOW_TEXT_BRIGHT
    print(f"Response: {f'{color}{response.status}{RESET_TEXT}'}")

    return response