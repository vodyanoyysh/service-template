import logging


def set_logger_config(config) -> logging:
    logging.basicConfig(
        level=config.level,
        format=config.format,
        datefmt=config.datefmt,
    )
    other_loggers_config(config.other_loggers)
    logger = logging.getLogger(config.name)
    return logger


def other_loggers_config(config):
    for logger_config in config:
        logger = logging.getLogger(logger_config.name)
        logger.setLevel(logger_config.level)


def get_logger(logger_name: str) -> logging:
    return logging.getLogger(logger_name)
