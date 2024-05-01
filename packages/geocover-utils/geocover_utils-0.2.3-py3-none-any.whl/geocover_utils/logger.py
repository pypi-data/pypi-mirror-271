import logging


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.handlers.clear()
    if not len(logger.handlers):
        logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

    return logger
