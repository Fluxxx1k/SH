from flask import request, abort

from WebsiteEasiest.logger import logger
from cli.colors import (YELLOW_TEXT_BRIGHT,
                        RESET_TEXT,
                        GREEN_TEXT_BRIGHT,
                        RED_TEXT_BRIGHT,
                        GREEN_TEXT,
                        YELLOW_TEXT, RED_TEXT)

from bisect import bisect_right
from time import time
from WebsiteEasiest.data.data_paths import path_banned

ips_frequency: dict[str, list[float]] = {}
count_stops: dict[str, float] = {}
ban_stops_count = 3
forgot_about_responses_sec = 60
max_response_times_ban = 100
max_response_times_temp_stop = 75
temp_stop_sec = 30
import json
try:
    bans = set(json.load(open(path_banned, 'r', encoding='utf-8')))
except Exception as e:
    bans = set()
    logger.error(f"Could not load bans: {repr(e)}")
stops: dict[str, float] = {}


def log_request():
    kostyl = True
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if real_ip in bans:
        time_now = time()
        ips_frequency[real_ip] += [time_now]
        index = bisect_right(ips_frequency[real_ip], time_now - forgot_about_responses_sec)
        ips_frequency[real_ip] = ips_frequency[real_ip][index:]
        kostyl = False
        logger.debug(f"[{real_ip} -> {request.path}] ({request.method}) Banned")
        print(f"[{real_ip} -> {request.path}] ({RED_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {RED_TEXT_BRIGHT}Banned{RESET_TEXT}")
        abort(429, description="Your IP is banned, please, ask admin to unban it")
    if real_ip in stops:
        time_now = time()
        ips_frequency[real_ip] += [time_now]
        index = bisect_right(ips_frequency[real_ip], time_now - forgot_about_responses_sec)
        ips_frequency[real_ip] = ips_frequency[real_ip][index:]
        kostyl = False
        if time_now < stops[real_ip]:
            logger.debug(f"[{real_ip} -> {request.path}] ({request.method}) Temp Stop {stops[real_ip]}")
            print(f"[{real_ip} -> {request.path}] ({YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {YELLOW_TEXT_BRIGHT}Temp Stop{RESET_TEXT} {stops[real_ip]}")
            abort(429, description=f"Your IP is temporarily stopped, please, try again later in {stops[real_ip] - time()} seconds")
        else:
            logger.debug(f"[{real_ip} -> {request.path}] ({request.method}) Temp Stop End")
            print(f"[{real_ip} -> {request.path}] ({YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {GREEN_TEXT_BRIGHT}Temp Stop End{RESET_TEXT}")
            del stops[real_ip]

    if real_ip in ips_frequency:
        if kostyl:
            time_now = time()
            ips_frequency[real_ip] += [time_now]
            index = bisect_right(ips_frequency[real_ip], time_now - forgot_about_responses_sec)
            ips_frequency[real_ip] = ips_frequency[real_ip][index:]
        if len(ips_frequency[real_ip]) > max_response_times_ban or count_stops.get(real_ip, 0) >= ban_stops_count:
            bans.add(real_ip)
            logger.debug(f"[{real_ip} -> {request.path}] ({request.method}) Banned now")
            print(f"[{real_ip} -> {request.path}] ({RED_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {RED_TEXT_BRIGHT}Banned now{RESET_TEXT}")
            abort(429, description="Your IP is banned now, please, ask admin to unban it")
        if len(ips_frequency[real_ip]) > max_response_times_temp_stop:
            stops[real_ip] = time() + temp_stop_sec
            count_stops[real_ip] = count_stops.get(real_ip, 0) + 1
            logger.debug(f"[{real_ip} -> {request.path}] ({request.method}) Temp Stop now {stops[real_ip]}")
            print(f"[{real_ip} -> {request.path}] ({YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {YELLOW_TEXT_BRIGHT}Temp Stop now{RESET_TEXT} {stops[real_ip]}")
            abort(429, description=f"Your IP is temporarily stopped now, please, try again later in {temp_stop_sec} seconds")
    else:
        ips_frequency[real_ip] = [time()]

    logger.debug(f"[{real_ip} -> {request.path}] ({request.method})")
    print(f"[{real_ip} -> {request.path}] ({YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT})")


def log_response(response):
    match response.status_code // 100:
        case 2:
            color = GREEN_TEXT_BRIGHT
        case 3:
            if response.status_code == 304:
                color = GREEN_TEXT
            else:
                color = YELLOW_TEXT
        case 4 | 5:
            if response.status_code == 429:
                color = YELLOW_TEXT_BRIGHT
            elif response.status_code == 404:
                color = RED_TEXT
            else:
                color = RED_TEXT_BRIGHT
        case _:
            color = YELLOW_TEXT_BRIGHT
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logger.info(f"[{real_ip} -> {request.path}] ({request.method}) {response.status}")
    print(f"[{real_ip} -> {request.path}] ({YELLOW_TEXT_BRIGHT}{request.method}{RESET_TEXT}) {color}{response.status}{RESET_TEXT}")

    return response