"""Module for helper functions."""


import logging


def get_logger():
    """Get logger with basic setup."""
    logger = logging.getLogger('')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('run.log')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger