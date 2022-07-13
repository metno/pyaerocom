from __future__ import annotations

from configparser import ConfigParser
from importlib import resources

VARS_INI = "emep_variables.ini"


def __parser():
    """Returns instance of ConfigParser to access information"""

    parser = ConfigParser()
    # added 12.7.21 by jgliss for EMEP trends processing. See here:
    # https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    parser.optionxform = str

    assert resources.is_resource(__package__, VARS_INI), f"{VARS_INI} not found in {__package__}"
    with resources.path(__package__, "emep_variables.ini") as path:
        parser.read(path)
    return parser


def emep_variables():
    """Read variable definitions from emep_variables.ini file

    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are EMEP variables
    """
    parser = __parser()
    variables = {}
    for key, value in parser["emep_variables"].items():
        _variables = (x.strip() for x in value.strip().split(","))
        for variable in _variables:
            variables[key] = variable
    return variables
