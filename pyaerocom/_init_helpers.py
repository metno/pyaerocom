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
from importlib import resources
from logging.config import fileConfig

LOGGING_CONFIG = dict(
    # root logger
    file_name="pyaerocom.log",
    file_days=14,
    file_level="DEBUG",
    # pyaerocom logger
    console_level="INFO",
)

with resources.path("pyaerocom.data", "logging.ini") as path:
    fileConfig(path, defaults=LOGGING_CONFIG, disable_existing_loggers=False)

logger = logging.getLogger("pyaerocom")


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

    assert logger.handlers, f"{logger.name} logger has not been configured correctly"
    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            handler.setLevel(level)


### Functions for package initialisation
def _init_supplemental():
    """
    Get version and pyaerocom installation path

    Returns
    -------
    str
        version string
    str
        path to source code base directory (
        <installed_basedir>/pyaerocom/pyaerocom)


    """
    import os

    from pkg_resources import get_distribution

    dist = get_distribution("pyaerocom")
    return (dist.version, os.path.join(dist.location, "pyaerocom"))
