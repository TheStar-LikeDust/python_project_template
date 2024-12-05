# coding: utf-8
"""A basic logger module base on logging

feature:
1. build logger in single function
2. stream/file handler


Demo:

    ```python
    import logger

    # minial
    _logger = logger.build_logger('testlogger')

    # with file handler
    _logger = logger.build_logger('default', file_handler=True)
    ```

"""
import logging
import os
import warnings

LOGGER_CURRENT_MSG_FORMATTER = '%(asctime)s | (%(name)s) [%(levelname)s] %(message)s'
"""str: current message formatter"""
LOGGER_CURRENT_TIME_FORMATTER = '%Y-%m-%d %H:%M:%S'
"""str: current time formatter"""

LOGGER_FORMATTER = logging.Formatter(LOGGER_CURRENT_MSG_FORMATTER, LOGGER_CURRENT_TIME_FORMATTER)
"""logging.Formatter: logger formatter"""

# handler mark
LOGGER_STREAM_HANDLER_MARK = 'logger_stream'

LOGGER_FILE_FOLDER = 'output'
"""str: logger file folder. will be created by os.makedirs"""


def get_logger_file_path(logger_name):
    return f'{LOGGER_FILE_FOLDER}/{logger_name}.log'


def mark_handler_check(logger: logging.Logger, handler_type: """type(logging.Handler)""" = logging.Handler) -> bool:
    """check if the logger has the mark handler.

    The build handler will be marked by LOGGER_STREAM_HANDLER_MARK

    Args:
        logger: logger to check
        handler_type: handler type to check

    Returns:
        bool: True if the logger has the mark handler, False otherwise
    """

    exist_handler = [handler for handler in logger.handlers if isinstance(handler, handler_type)]
    mark_handler = [handler for handler in exist_handler if handler.name == LOGGER_STREAM_HANDLER_MARK]

    return bool(mark_handler)


def add_stream_handler(
        looger_name: str,
        handler_level: int = logging.DEBUG,
        handler_formatter_str: str = LOGGER_CURRENT_MSG_FORMATTER,
        handler_time_formatter_str: str = LOGGER_CURRENT_TIME_FORMATTER,
        unique_handler: bool = True
):
    logger = logging.getLogger(looger_name)
    stream_handler = logging.StreamHandler()
    stream_handler.name = LOGGER_STREAM_HANDLER_MARK
    stream_handler.setFormatter(logging.Formatter(handler_formatter_str, handler_time_formatter_str))
    stream_handler.setLevel(handler_level)

    if not unique_handler or not mark_handler_check(logger, logging.StreamHandler):
        logger.addHandler(stream_handler)


def add_file_handler(
        logger_name: str,
        handler_level: int = logging.DEBUG,
        handler_formatter_str: str = LOGGER_CURRENT_MSG_FORMATTER,
        handler_time_formatter_str: str = LOGGER_CURRENT_TIME_FORMATTER,
        file_handler_filename: str = None,
        file_handler_mode: str = 'a',
        unique_handler: bool = True,
):
    file_path = get_logger_file_path(file_handler_filename or logger_name)

    try:
        logger = logging.getLogger(logger_name)
        file_handler = logging.FileHandler(file_path, mode=file_handler_mode, encoding='utf-8')
        file_handler.name = LOGGER_STREAM_HANDLER_MARK
        file_handler.setFormatter(logging.Formatter(handler_formatter_str, handler_time_formatter_str))
        file_handler.setLevel(handler_level)

        if not unique_handler or not mark_handler_check(logger, logging.FileHandler):
            logger.addHandler(file_handler)
    except FileNotFoundError:
        # warning
        warnings.warn(f'cannot create file handler in path: <{file_path}>')


def build_logger(logger_name: str,
                 level: int = logging.DEBUG,
                 stream_handler: bool = True,
                 stream_handler_kwargs: dict = None,
                 file_handler: bool = False,
                 file_handler_kwargs: dict = None,
                 ):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if stream_handler:
        stream_handler_kwargs = stream_handler_kwargs or {}
        add_stream_handler(logger_name, **stream_handler_kwargs)

    if file_handler:
        file_handler_kwargs = file_handler_kwargs or {}
        add_file_handler(logger_name, **file_handler_kwargs)

    return logger


os.makedirs(LOGGER_FILE_FOLDER, exist_ok=True)

if __name__ == '__main__':
    build_logger('testlogger').info('testlogger')
    build_logger('test_file_logger', file_handler=True).info('test_file_logger')
