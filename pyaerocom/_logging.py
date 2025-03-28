"""
Logging configuration and package metadata helpers

NOTE:
All pyaerocom child modules share the logging configuration
- all logging messages are time stamped and written out to file
- some messages are also printed to the console
- log files are kept up to 14 days
- logging configuration is read from pyaerocom/data/logging.ini
  with default values from LOGGING_CONFIG
"""

from __future__ import annotations

import logging
import os
import pathlib
import resource
import sys
import time
from logging.config import fileConfig

import psutil

from pyaerocom.data import resources


class MemUsageFilter(logging.Filter):
    """
    This is a filter which injects mem_usage information
    """

    def filter(self, record):
        mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        curmem = psutil.Process().memory_info().rss / (1024 * 1024)
        if mem < 1024:
            record.mem_usage = f"{curmem:.0f}/{mem:.0f}M"
        else:
            record.mem_usage = f"{curmem / 1024:.1f}/{mem / 1024:.1f}G"
        return True


def _add_memusage_filter():
    logger = logging.getLogger("")
    muf = MemUsageFilter()
    for h in logger.handlers:
        h.addFilter(muf)


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

    logger = logging.getLogger("")
    assert logger.handlers, f"{logger.name} logger has not been configured correctly"
    for handler in logger.handlers:
        if type(handler) is logging.StreamHandler:
            handler.setLevel(level)


LOGGING_CONFIG = dict(
    # root logger
    file_name=os.getenv("PYAEROCOM_LOG_FILE", default=f"logs/pyaerocom.log.{os.getpid()}"),
    pid=os.getpid(),
)
cwd_log_path = pathlib.Path.cwd() / "logging.ini"
if cwd_log_path.exists():
    fileConfig(cwd_log_path, defaults=LOGGING_CONFIG, disable_existing_loggers=True)
    _add_memusage_filter()
else:
    file_name = pathlib.Path(LOGGING_CONFIG["file_name"])
    log_path = file_name.parent
    log_path.mkdir(exist_ok=True, parents=True)
    with resources.path("pyaerocom", "logging.ini") as path:
        fileConfig(path, defaults=LOGGING_CONFIG, disable_existing_loggers=False)
    _add_memusage_filter()
    if not sys.stdout.isatty():  # disable stdout when non-interactive
        change_verbosity(logging.CRITICAL)
    # cleanup of old default logging files
    now = time.time()
    logger = logging.getLogger(__name__)
    for f in log_path.glob("pyaerocom.log.*"):
        age = now - f.lstat().st_mtime
        if age > (7 * 24 * 60 * 60):
            logger.info(f"deleting log-file older than 7 days: {f}")
            f.unlink()
    old_logfile = pathlib.Path("pyaerocom.log")
    if old_logfile.exists():
        logger.warning(
            f"no longer used old default logfile '{old_logfile}' exist, please consider deleting"
        )
