from flask import request

from WebsiteEasiest.logger import logger
from cli.colors import (YELLOW_TEXT_BRIGHT,
                        RESET_TEXT,
                        GREEN_TEXT_BRIGHT,
                        RED_TEXT_BRIGHT,
                        GREEN_TEXT,
                        YELLOW_TEXT)


def log_request():
    logger.debug(f"[{request.method}] {request.path} - {request.remote_addr}")
    print(f"[{YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}] {request.path} - {request.remote_addr}")


def log_response(response):
    match response.status_code // 100:
        case 2:
            color = GREEN_TEXT_BRIGHT
            logger.debug(f"Response: {response.status}")
        case 3:
            if response.status_code == 304:
                color = GREEN_TEXT
            else:
                color = YELLOW_TEXT
            logger.debug(f"Response: {response.status}")
        case 4 | 5:
            color = RED_TEXT_BRIGHT
        case _:
            color = YELLOW_TEXT_BRIGHT
            logger.debug(f"Response: {response.status}")
    print(f"Response: {f'{color}{response.status}{RESET_TEXT}'}")

    return response