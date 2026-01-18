import os
import time

from WebsiteEasiest.logger import logger
from WebsiteEasiest.web_core.server_spec.shutdown import shutdown, shutdown_force

memory_info = 0

def mem_check():
    from psutil import Process
    curr_process = Process(os.getpid())
    global memory_info
    memory_info = curr_process.memory_info().rss
    mem_check_count = 0
    mem_check_max_value = -1
    mem_check_min_value = 1 << 33
    mem_check_log_num = 3
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
            else:
                logger.warning(f"Memory usage exceeded 0.5 GB ({(memory_info >> 10) / 1024:.2f} MB)")
            from WebsiteEasiest.settings import web_config
            web_config.New_games_allowed = False
        time.sleep(600)
    shutdown_force(30)