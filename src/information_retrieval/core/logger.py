import logging

formatter = "[%(levelname)s] %(asctime)s %(filename)s %(lineno)d %(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter)


def get_logger(name: str = "app-logger", level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


app_logger = get_logger()
