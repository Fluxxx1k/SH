from flask import request

from WebsiteEasiest1.logger import logger
from cli.colors import (YELLOW_TEXT_BRIGHT,
                        RESET_TEXT,
                        GREEN_TEXT_BRIGHT,
                        RED_TEXT_BRIGHT,
                        GREEN_TEXT,
                        YELLOW_TEXT)


def log_request():
    logger.debug(f"{YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}| {request.path} - {request.remote_addr}")


def log_response(response):
    match response.status_code // 100:
        case 2:
            logger.debug(f"Response: {f'{GREEN_TEXT_BRIGHT}{response.status}{RESET_TEXT}'}")
        case 4:
            logger.warning(f"Response: {f'{RED_TEXT_BRIGHT}{response.status}{RESET_TEXT}'}")
        case 5:
            logger.error(f"Response: {f'{RED_TEXT_BRIGHT}{response.status}{RESET_TEXT}'}")
        case 3:
            if response.status_code == 304:
                color = GREEN_TEXT
            else:
                color = YELLOW_TEXT
            logger.debug(f"Response: {f'{color}{response.status}{RESET_TEXT}'}")
        case _:
            logger.debug(f"Response: {f'{YELLOW_TEXT_BRIGHT}{response.status}{RESET_TEXT}'}")
    return response