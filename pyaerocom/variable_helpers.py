import os
from configparser import ConfigParser

from pyaerocom.exceptions import VariableDefinitionError


def parse_variables_ini(fpath=None):
    """Returns instance of ConfigParser to access information"""
    from pyaerocom import __dir__
    if fpath is None:
        fpath = os.path.join(__dir__, "data", "variables.ini")

    if not os.path.exists(fpath):
        raise FileNotFoundError("FATAL: variables.ini file could not be found "
                                "at {}".format(fpath))
    parser = ConfigParser()
    parser.read(fpath)
    return parser


def parse_aliases_ini():
    """Returns instance of ConfigParser to access information"""
    from pyaerocom import __dir__
    fpath = os.path.join(__dir__, "data", "aliases.ini")
    if not os.path.exists(fpath):
        raise FileNotFoundError("FATAL: aliases.ini file could not be found "
                                "at {}".format(fpath))
    parser = ConfigParser()
    parser.read(fpath)
    return parser


def get_emep_variables(parser=None):
    """Read variable definitions from emep_variables.ini file

    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are EMEP variables
    """
    if parser is None:
        parser = parse_emep_variables_ini()
    variables = {}
    items = parser['emep_variables']
    for var_name in items:
        _variables = [x.strip() for x in items[var_name].strip().split(',')]
        for variable in _variables:
            variables[var_name] = variable
    return variables


def parse_emep_variables_ini(fpath=None):
    """Returns instance of ConfigParser to access information"""
    from pyaerocom import __dir__
    if fpath is None:
        fpath = os.path.join(__dir__, "data", "emep_variables.ini")
    if not os.path.exists(fpath):
        raise FileNotFoundError("FATAL: emep_variables.ini file could not be found "
                        "at {}".format(fpath))
    parser = ConfigParser()
    # added 12.7.21 by jgliss for EMEP trends processing. See here:
    # https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
    parser.optionxform=str
    parser.read(fpath)
    return parser


def _read_alias_ini(parser=None):
    """Read all alias definitions from aliases.ini file and return as dict

    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are corresponding
        aliases
    """
    if parser is None:
        parser = parse_aliases_ini()
    aliases = {}
    items = parser['aliases']
    for var_name in items:
        _aliases = [x.strip() for x in items[var_name].strip().split(',')]
        for alias in _aliases:
            aliases[alias] = var_name
    for var_fam, alias_fam in parser['alias_families'].items():
        if ',' in alias_fam:
            raise Exception('Found invalid definition of alias family {}: {}. '
                            'Only one family can be mapped to a variable name'
                            .format(var_fam, alias_fam))
    return aliases


def get_aliases(var_name, parser=None):
    """Get aliases for a certain variable"""
    if parser is None:
        from pyaerocom import __dir__
        file = os.path.join(__dir__, "data", "aliases.ini")
        parser = ConfigParser()
        parser.read(file)

    info = parser['aliases']
    aliases = []
    if var_name in info:
        aliases.extend([a.strip() for a in info[var_name].split(',')])
    for var_fam, alias_fam in parser['alias_families'].items():
        if var_name.startswith(var_fam):
            alias = var_name.replace(var_fam, alias_fam)
            aliases.append(alias)
    return aliases


def _check_alias_family(var_name, parser):
    for var_fam, alias_fam in parser['alias_families'].items():
        if var_name.startswith(alias_fam):
            var_name_aerocom = var_name.replace(alias_fam, var_fam)
            return var_name_aerocom
    raise VariableDefinitionError('Input variable could not be identified as '
                                  'belonging to either of the available alias '
                                  'variable families')


def get_variable(var_name):
    """
    Get a certain variable

    Parameters
    ----------
    var_name : str
        variable name

    Returns
    -------
    Variable
    """
    from pyaerocom import const
    return const.VARS[var_name]