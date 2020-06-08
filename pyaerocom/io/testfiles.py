#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyaerocom test files
"""
def get():
    """Load test files of models and observations stored in test_files.ini file

    The file should be available at the relative location:

        ./pyaerocom/data/test_files.ini

    Parameters
    ----------
    proj_dir : str
        project base directory (i.e. pyaerocom.__dir__)

    Returns
    -------
    dict
        dictionary containing two keys (`models`, `observations`), with
        values being 2 dictionaries that contain pairs of `name` and
        test paths.

    Raises
    ------
    IOError
        if the test_files.ini file cannot be found in the specified loaction

    Examples
    --------

    >>> from os.path import basename
    >>> all_files = get()
    >>> example_file = all_files["models"]["aatsr_su_v4.3"]
    >>> filename = basename(example_file)
    >>> print(filename=="aerocom.AATSR_SU_v4.3.daily.od550aer.2008.nc")
    True
    """
    try:
        from ConfigParser import ConfigParser
    except Exception:
        from configparser import ConfigParser
    from collections import OrderedDict
    from os.path import join, exists
    from warnings import warn
    from pyaerocom import __dir__
    fpath = join(__dir__, "data", "test_files.ini")
    if not exists(fpath):
        raise IOError("File %s does not exist" %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)
    result = OrderedDict()
    result["models"] = OrderedDict()
    result["observations"] = OrderedDict()

    for key, val in conf_reader["models"].items():
        result["models"][key] = val
        if not exists(val):
            warn("Default test path for model %s could not be found: %s"
                 %(key, val))
    for key, val in conf_reader["observations"].items():
        result["observations"][key] = val
        if not exists(val):
            warn("Default test path for model %s could not be found: %s"
                 %(key, val))
    return result

if __name__=="__main__":
    import doctest
    doctest.testmod()
