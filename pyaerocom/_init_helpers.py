from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler

# Note: configuration will be propagated to all child modules of
# pyaerocom, for details see
# http://eric.themoritzfamily.com/learning-python-logging.html
logger = logging.getLogger("pyaerocom")


def _init_logger(logger: logging.Logger = logger, backup_days: int = 14) -> logging.Logger:

    # keep the up to backup_days days of daily log files
    file_handler = TimedRotatingFileHandler("pyaerocom.log", when="D", backupCount=backup_days)
    file_formatter = logging.Formatter(
        "%(asctime)s:%(module)s:%(levelname)s:%(message)s", datefmt="%F %T"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger


_init_logger()


def change_verbosity(level: str | int = "debug", logger: logging.Logger = logger) -> None:
    """
    Change logging verbosity to the console

    Parameters
    ----------
    level : str or int
        new `logging level<https://docs.python.org/3/library/logging.html#logging-levels>`_
    logger:
        `pyaerocom.logger` by default

    Returns
    -------
    None

    """
    if isinstance(level, str):
        level = level.upper()

    if isinstance(level, int) and not (logging.DEBUG <= level <= logging.CRITICAL):
        raise ValueError(
            f"invalid log level {level}, choose a value between {logging.DEBUG} and {logging.CRITICAL}"
        )

    if not logger.hasHandlers():
        logger.setLevel(level)
        return

    for handler in logger.handlers:
        if not isinstance(handler, logging.StreamHandler):
            continue
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
