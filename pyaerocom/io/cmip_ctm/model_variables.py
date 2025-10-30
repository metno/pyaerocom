from __future__ import annotations

import sys

from pyaerocom.data import resources

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

_VARIABLES = "variables.toml"


def cmip_variables() -> dict[str, str]:
    """Read variable definitions from variables.toml file

    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are cmip variables
    """
    assert resources.is_resource(__package__, _VARIABLES), f"{_VARIABLES} missing in {__package__}"
    variables = tomllib.loads(resources.read_text(__package__, _VARIABLES))
    return variables["cmip_variables"]
