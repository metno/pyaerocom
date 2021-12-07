from __future__ import annotations

import logging


def _init_logger():
    ### LOGGING
    # Note: configuration will be propagated to all child modules of
    # pyaerocom, for details see
    # http://eric.themoritzfamily.com/learning-python-logging.html

    logger = logging.getLogger("pyaerocom")
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s:%(levelname)s:\n%(message)s")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.CRITICAL)
    logger.addHandler(console_handler)

    print_log = logging.getLogger("pyaerocom_print")
    print_handler = logging.StreamHandler()
    print_formatter = logging.Formatter("%(message)s")
    print_handler.setFormatter(print_formatter)
    print_handler.setLevel(logging.INFO)
    print_log.addHandler(print_handler)

    return (logger, print_log)


def change_verbosity(level: str | int = "debug", log: logging.Logger = None) -> None:
    """
    Change logging verbosity to the console

    Parameters
    ----------
    level : str or int
        new `logging level<https://docs.python.org/3/library/logging.html#logging-levels>`_
    log
        either `pyaerocom.logger` or `pyaerocom.print_log`.

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

    if log is None:
        from pyaerocom import logger

        log = logger

    if not log.hasHandlers():
        log.setLevel(level)
        return

    for handler in log.handlers:
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
