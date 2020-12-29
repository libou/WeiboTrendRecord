import logging, datetime, logging.handlers
import os

def init_log(log_dir):
    #日志分割
    running_log = os.path.join(log_dir, "info.log")
    warning_log = os.path.join(log_dir, "warning.log")
    error_log = os.path.join(log_dir, "error.log")

    logger = logging.getLogger("webscraping_log")
    logger.setLevel(logging.INFO)

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
    LOG_FORMAT = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"

    running_log_handler = logging.handlers.TimedRotatingFileHandler(running_log, when='midnight',
                                                                    interval=1, backupCount=5)
    warning_log_handler = logging.handlers.TimedRotatingFileHandler(warning_log, when='midnight',
                                                                    interval=1, backupCount=5)
    error_log_handler = logging.handlers.TimedRotatingFileHandler(error_log, when='midnight',
                                                                    interval=1, backupCount=5)

    running_log_handler.setLevel(logging.INFO)
    running_log_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    warning_log_handler.setLevel(logging.WARNING)
    warning_log_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    error_log_handler.setLevel(logging.ERROR)
    error_log_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(running_log_handler)
    logger.addHandler(warning_log_handler)
    logger.addHandler(error_log_handler)

    return logger
