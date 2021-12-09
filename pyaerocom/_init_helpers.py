"""
Logging configuration and package metadata helpers

NOTE: logging configuration will be propagated to all child pyaerocom modules
"""


from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

root_logger = logging.getLogger()
pya_logger = logging.getLogger("pyaerocom")


def __configure_file_logger(
    logger: logging.Logger, filename: str | Path, *, level: int, backup_days: int
):
    """keep the up to backup_days days of daily log files"""
    handler = TimedRotatingFileHandler(filename, when="D", backupCount=backup_days)
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(levelname)s:%(message)s", datefmt="%F %T"
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)


def __configuure_console_logger(logger: logging.Logger, *, level: int):

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)

    return logger


__configure_file_logger(root_logger, "pyaerocom.log", level=logging.DEBUG, backup_days=14)
__configuure_console_logger(pya_logger, level=logging.INFO)


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

    if not pya_logger.handlers:
        __configuure_console_logger(pya_logger, level=level)
        return

    for handler in pya_logger.handlers:
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
