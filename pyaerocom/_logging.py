"""
Logging configuration and package metadata helpers

NOTE: 
All pyaerocom child modules share the logging configuration
- all logging messages are time stamped and writen out to file
- some messages are also printed to the console
- log files are kept up to 14 days
- logging configuration is read from pyaerocom/data/logging.ini
  with default values from LOGGING_CONFIG
"""
from __future__ import annotations

import logging
import os
from logging.config import fileConfig

from pyaerocom.data import resources

LOGGING_CONFIG = dict(
    # root logger
    file_name=os.getenv("PYAEROCOM_LOG_FILE", default="pyaerocom.log"),
    file_days="14",
    file_level="DEBUG",
    # pyaerocom logger
    console_level="INFO",
)

with resources.path("pyaerocom.data", "logging.ini") as path:
    fileConfig(path, defaults=LOGGING_CONFIG, disable_existing_loggers=False)


def change_verbosity(level: str | int) -> None:
    """
    Change logging verbosity (to console)

    Parameters
    ----------
    level: str or int
        new `logging level<https://docs.python.org/3/library/logging.html#logging-levels>`_

    Returns
    -------
    None

    """
    if isinstance(level, str):
        level = level.upper()

    if isinstance(level, int) and not (logging.DEBUG <= level <= logging.CRITICAL):
        raise ValueError(
            f"invalid logging level {level}, choose a value between {logging.DEBUG} and {logging.CRITICAL}"
        )

    logger = logging.getLogger(__package__)
    assert logger.handlers, f"{logger.name} logger has not been configured correctly"
    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            handler.setLevel(level)
