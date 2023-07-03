import logging
import time

import os
import logging
import time

def Logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        logger = logging.getLogger("FunctionLogger")
        logger.setLevel(logging.INFO)

        log_folder = "resources/logger"
        os.makedirs(log_folder, exist_ok=True)

        log_file = os.path.join(log_folder, "logginginfo.log")
        file_handler = logging.FileHandler(log_file)

        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.info(f"Function: {func.__name__} - Execution Time: {execution_time} seconds")

        return result

    return wrapper
