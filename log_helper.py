import logging


def create_logger_instance(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def create_file_for_logging(filename):
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    return fh


def add_file_support_to_logger(logger, file_handler):
    logger.addHandler(file_handler)
