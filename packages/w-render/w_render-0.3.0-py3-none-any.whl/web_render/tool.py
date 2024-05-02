"""
Copyright (c) 2024 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import os
import logging


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def log(name, filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(int(os.environ.get('LOGGING_LEVEL', 10)))
    # logger.propagate = False

    if filename:
        ch = logging.FileHandler(filename)
    else:
        ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s : %(lineno)d : %(name)s : %(levelname)s : %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    return logger
