from __future__ import annotations

import logging


def _init_logger():
    ### LOGGING
    # Note: configuration will be propagated to all child modules of
    # pyaerocom, for details see
    # http://eric.themoritzfamily.com/learning-python-logging.html
    logger = logging.getLogger("pyaerocom")

    default_formatter = logging.Formatter("%(asctime)s:%(levelname)s:\n%(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(default_formatter)

    logger.addHandler(console_handler)

    logger.setLevel(logging.CRITICAL)

    print_log = logging.getLogger("pyaerocom_print")

    print_handler = logging.StreamHandler()
    print_handler.setFormatter(logging.Formatter("%(message)s"))

    print_log.addHandler(print_handler)

    print_log.setLevel(logging.INFO)
    return (logger, print_log)


def change_verbosity(level: str | int = "debug", logger: logging.Logger = None) -> None:
    """
    Change verbosity of one of the pyaerocom loggers

    Parameters
    ----------
    level : str or int
        new `logging level<https://docs.python.org/3/library/logging.html#logging-levels>`_
    logger
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

    if logger is None:
        logger = logging.getLogger("pyaerocom")

    logger.setLevel(level)


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
