import logging

LOG_LEVEL = logging.DEBUG
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(LOG_LEVEL)


def get_logger(logger_name):

    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(STREAM_HANDLER)

    return logger
