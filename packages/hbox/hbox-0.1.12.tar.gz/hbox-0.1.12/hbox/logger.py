import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno != logging.INFO:
            self._style._fmt = "[%(levelname)s] %(message)s"
        else:
            self._style._fmt = "%(message)s"
        return super().format(record)


def get_logger(name: str):
    global log_level
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = CustomFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def set_log_level(level):
    global log_level
    log_level = level


log_level = logging.INFO
