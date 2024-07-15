from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from pyaerocom.data import resources
from pyaerocom.exceptions import VariableDefinitionError


def parse_variables_ini(fpath: str | Path | None = None):
    """Returns instance of ConfigParser to access information"""

    if fpath is None:
        with resources.path("pyaerocom.data", "variables.ini") as path:
            fpath = path

    if isinstance(fpath, str):
        fpath = Path(fpath)
    if not fpath.exists():
        raise FileNotFoundError(f"FATAL: variables.ini file could not be found at {fpath}")

    parser = ConfigParser()
    parser.read(fpath)
    return parser


def parse_aliases_ini():
    """Returns instance of ConfigParser to access information"""
    with resources.path("pyaerocom.data", "aliases.ini") as path:
        fpath = path

    parser = ConfigParser()
    parser.read(fpath)
    return parser


def _read_alias_ini(parser: ConfigParser | None = None):
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
    items = parser["aliases"]
    for var_name in items:
        _aliases = [x.strip() for x in items[var_name].strip().split(",")]
        for alias in _aliases:
            aliases[alias] = var_name
    for var_fam, alias_fam in parser["alias_families"].items():
        if "," in alias_fam:
            raise Exception(
                f"Found invalid definition of alias family {var_fam}: {alias_fam}. "
                f"Only one family can be mapped to a variable name"
            )
    return aliases


def get_aliases(var_name: str, parser: ConfigParser | None = None):
    """Get aliases for a certain variable"""
    if parser is None:
        parser = ConfigParser()
        with resources.path("pyaerocom.data", "aliases.ini") as path:
            parser.read(path)

    info = parser["aliases"]
    aliases = []
    if var_name in info:
        aliases.extend([a.strip() for a in info[var_name].split(",")])
    for var_fam, alias_fam in parser["alias_families"].items():
        if var_name.startswith(var_fam):
            alias = var_name.replace(var_fam, alias_fam)
            aliases.append(alias)
    return aliases


def _check_alias_family(var_name: str, parser: ConfigParser):
    for var_fam, alias_fam in parser["alias_families"].items():
        if var_name.startswith(alias_fam):
            var_name_aerocom = var_name.replace(alias_fam, var_fam)
            return var_name_aerocom
    raise VariableDefinitionError(
        "Input variable could not be identified as "
        "belonging to either of the available alias "
        "variable families"
    )


def get_variable(var_name: str):
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
