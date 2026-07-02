import logging
import functools
import time
from pathlib import Path
from src.config import dir_config
from logging.handlers import RotatingFileHandler

def setup_log(name="Fraud_detection", filename="app"):
    
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.INFO)

    log_file = dir_config.logs_dir / f"{filename}.log"

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def auto_logger(logger: logging.Logger):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            curr_logger = logger
            curr_logger.info(f"Starting execution of: {func.__name__}", stacklevel=2)
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                duration = time.time() - start_time

                curr_logger.info(f"Successfully finished: {func.__name__} in {duration:.4f} seconds", stacklevel=2)
                return result         
            except Exception as e:
                duration = time.time() - start_time
                curr_logger.exception(f"CRASH in {func.__name__} after {duration:.4f} seconds. Error: {str(e)}", stacklevel=2)
                raise e
        return wrapper
    return decorator

