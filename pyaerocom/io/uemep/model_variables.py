from __future__ import annotations

import sys

from pyaerocom.data import resources

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

_VARIABLES = "uemep_variables.toml"


def uemep_variables() -> dict[str, str]:
    """Read variable definitions from uemep_variables.yaml file

    Returns
    -------
    dict
        keys are AEROCOM standard names of variable, values are uEMEP variables
    """
    assert resources.is_resource(__package__, _VARIABLES), f"{_VARIABLES} missing in {__package__}"
    variables = tomllib.loads(resources.read_text(__package__, _VARIABLES))
    return variables["uemep_variables"]
