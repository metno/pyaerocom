LOGLEVELS = {'debug': 10,
             'info': 20,
             'warning': 30,
             'error': 40,
             'critical': 50}

def _init_logger():
    import logging
    ### LOGGING
    # Note: configuration will be propagated to all child modules of
    # pyaerocom, for details see
    # http://eric.themoritzfamily.com/learning-python-logging.html
    logger = logging.getLogger('pyaerocom')

    default_formatter = logging.Formatter(\
       "%(asctime)s:%(levelname)s:\n%(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(default_formatter)

    logger.addHandler(console_handler)

    logger.setLevel(logging.CRITICAL)

    print_log = logging.getLogger('pyaerocom_print')

    print_handler = logging.StreamHandler()
    print_handler.setFormatter(logging.Formatter("%(message)s"))

    print_log.addHandler(print_handler)

    print_log.setLevel(logging.INFO)
    return (logger, print_log)

def change_verbosity(new_level='debug', log=None):
    """
    Change verbosity of one of the pyaerocom loggers

    Parameters
    ----------
    new_level : str or int
        choose from either keys, or values of :attr:`LOGLEVELS`.
    log
        either `pyaerocom.logger` or `pyaerocom.print_log`.

    Returns
    -------
    None

    """
    if log is None:
        from pyaerocom import logger
        log = logger
    if isinstance(new_level, str):
        if not new_level in LOGLEVELS:
            raise ValueError(f'invalid log level {new_level}, choose from '
                             f'keys or values of {LOGLEVELS}')
        new_level = LOGLEVELS[new_level]
    else:
        if not new_level in LOGLEVELS.values():
            raise ValueError(f'invalid log level {new_level}, choose from '
                             f'keys or values of {LOGLEVELS}')
    log.setLevel(new_level)

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
    from pkg_resources import get_distribution
    import os
    dist = get_distribution('pyaerocom')
    return (dist.version, os.path.join(dist.location, 'pyaerocom'))


