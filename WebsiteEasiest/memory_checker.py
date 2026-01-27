import os
import time

from WebsiteEasiest.logger import logger
from WebsiteEasiest.web_core.server_spec.shutdown import shutdown_force

memory_info = 0

def mem_check():
    from psutil import Process
    curr_process = Process(os.getpid())
    global memory_info
    memory_info = curr_process.memory_info().rss
    mem_check_count = 0
    mem_check_max_value = -1
    mem_check_min_value = 8589934592
    mem_check_log_num = 5
    while memory_info < 1610612736:
        memory_info = curr_process.memory_info().rss
        mem_check_max_value = max(mem_check_max_value, memory_info)
        mem_check_min_value = min(mem_check_min_value, memory_info)
        if mem_check_count % mem_check_log_num == 0:
            logger.info(f"Memory check №{mem_check_count}: max {(mem_check_max_value >> 10) / 1024:.2f} MB, min {(mem_check_min_value >> 10) / 1024:.2f} MB, current {(memory_info >> 10) / 1024:.2f} MB")
            mem_check_max_value = -1
            mem_check_min_value = 1 << 33
        logger.debug(f"Memory usage №{mem_check_count}: {(memory_info >> 10) / 1024:.2f} MB")
        mem_check_count += 1
        if memory_info > 536870912: # 1 << 29
            if memory_info > 1342177280: # (1 << 30) * 1.25
                logger.critical(f"Memory usage exceeded 1.25 GB ({(memory_info >> 10) / 1024:.2f} MB)")
                shutdown_force(30)
            elif memory_info > 1073741824: # 1 << 30
                logger.error(f"Memory usage exceeded 1 GB ({(memory_info >> 10) / 1024:.2f} MB)")
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
            else:
                logger.warning(f"Memory usage exceeded 0.5 GB ({(memory_info >> 10) / 1024:.2f} MB)")
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
        # Динамический интервал в зависимости от занятости памяти
        # Базовый интервал 600 секунд (10 минут)
        base_interval = 600
        # Порог критической памяти (1.25 GB)
        critical_threshold = 1342177280
        # Коэффициент: чем ближе к порогу, тем меньше интервал
        # Используем линейную зависимость: interval = base_interval * (1 - memory_info / critical_threshold)
        # Но не меньше минимального интервала (например, 60 секунд)
        min_interval = 60
        # Вычисляем коэффициент занятости (от 0 до 1)
        occupancy_ratio = memory_info / critical_threshold
        # Интервал уменьшается с ростом занятости
        dynamic_interval = base_interval * (1 - occupancy_ratio)
        # Ограничиваем снизу минимальным интервалом
        dynamic_interval = max(min_interval, dynamic_interval)
        logger.debug(f"Dynamic sleep interval: {dynamic_interval:.2f} seconds (occupancy: {occupancy_ratio:.2%})")
        time.sleep(dynamic_interval)
    logger.critical(f"Memory usage is greater than 1.5 GB ({(memory_info >> 10) / 1024:.2f} MB)")
    shutdown_force(30)