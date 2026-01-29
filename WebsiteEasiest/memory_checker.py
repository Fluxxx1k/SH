import os
import time

from WebsiteEasiest.logger import logger
from WebsiteEasiest.web_core.server_spec.shutdown import shutdown_force, save_cache

memory_info = 0
cpu_percent = 0.0
def clear_cache():
    save_cache()
    try:
        from WebsiteEasiest.data.database_py.players import players_data_dict
        players_data_dict.clear()
    except Exception as e:
        logger.error(f"Could not clear players_data_dict: {repr(e)}")
    else:
        logger.debug(f"Successfully cleared players_data_dict")
    try:
        from WebsiteEasiest.data.database_py.games import games_data_dict
        games_data_dict.clear()
    except Exception as e:
        logger.error(f"Could not clear games_data_dict: {repr(e)}")
    else:
        logger.debug(f"Successfully cleared games_data_dict")


def mem_check():
    from psutil import Process, cpu_percent as psutil_cpu_percent
    curr_process = Process(os.getpid())
    global memory_info, cpu_percent
    memory_info = curr_process.memory_info().rss
    mem_check_count = 0
    mem_check_max_value = -1
    mem_check_min_value = 8589934592
    mem_check_log_num = 5
    cpu_check_log_num = 5  # логировать CPU каждые N проверок
    while memory_info < 1610612736 and cpu_percent < 40:
        memory_info = curr_process.memory_info().rss
        cpu_percent = psutil_cpu_percent(interval=0.5)  # замер за 0.5 секунды
        mem_check_max_value = max(mem_check_max_value, memory_info)
        mem_check_min_value = min(mem_check_min_value, memory_info)
        if mem_check_count % mem_check_log_num == 0:
            logger.info(f"Memory check №{mem_check_count}: max {(mem_check_max_value >> 10) / 1024:.2f} MB, min {(mem_check_min_value >> 10) / 1024:.2f} MB, current {(memory_info >> 10) / 1024:.2f} MB")
            mem_check_max_value = -1
            mem_check_min_value = 1 << 33
        if mem_check_count % cpu_check_log_num == 0:
            logger.info(f"CPU check №{mem_check_count}: {cpu_percent:.1f}%")
        logger.debug(f"Memory usage №{mem_check_count}: {(memory_info >> 10) / 1024:.2f} MB; CPU: {cpu_percent:.1f}%")
        mem_check_count += 1
        if memory_info > 536870912: # 1 << 29
            if memory_info > 1342177280: # (1 << 30) * 1.25
                logger.critical(f"Memory usage exceeded 1.25 GB ({(memory_info >> 10) / 1024:.2f} MB)")
                clear_cache()
                shutdown_force(30)
            elif memory_info > 1073741824: # 1 << 30
                logger.error(f"Memory usage exceeded 1 GB ({(memory_info >> 10) / 1024:.2f} MB)")
                clear_cache()
            else:
                logger.warning(f"Memory usage exceeded 0.5 GB ({(memory_info >> 10) / 1024:.2f} MB)")
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
        # Проверка CPU
        if cpu_percent > 40.0:
            logger.critical(f"CPU usage exceeded 40% ({cpu_percent:.1f}%)")
            # Можно добавить действия, например, ограничить создание игр
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
        elif cpu_percent > 25.0:
            logger.error(f"CPU usage exceeded 25% ({cpu_percent:.1f}%)")
        elif cpu_percent > 15.0:
            logger.warning(f"CPU usage exceeded 15% ({cpu_percent:.1f}%)")
        # Динамический интервал в зависимости от занятости памяти и CPU
        # Базовый интервал 600 секунд (10 минут)
        base_interval = 600
        # Порог критической памяти (1.25 GB)
        critical_memory_threshold = 1342177280
        # Порог критической CPU (40%)
        critical_cpu_threshold = 40.0
        # Коэффициент занятости памяти (от 0 до 1)
        memory_ratio = memory_info / critical_memory_threshold
        # Коэффициент занятости CPU (от 0 до 1)
        cpu_ratio = cpu_percent / critical_cpu_threshold if critical_cpu_threshold > 0 else 0.0
        # Общий коэффициент занятости (берём максимум)
        occupancy_ratio = memory_ratio + cpu_ratio
        # Интервал уменьшается с ростом занятости
        dynamic_interval = base_interval * (1 - occupancy_ratio)
        # Минимальный интервал 60 секунд
        min_interval = 60
        dynamic_interval = max(min_interval, dynamic_interval)
        logger.debug(f"Dynamic sleep interval: {dynamic_interval:.2f} seconds (memory: {memory_ratio:.2%}, cpu: {cpu_ratio:.2%})")
        time.sleep(dynamic_interval)
    logger.critical(f"Memory usage is greater than 1.5 GB ({(memory_info >> 10) / 1024:.2f} MB) or CPU usage is greater than 40% ({cpu_percent: .1f}%)")
    shutdown_force(30)