import logging

from config.config import LOG_FILE


def _setup_logger():
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(LOG_FILE)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = _setup_logger()
