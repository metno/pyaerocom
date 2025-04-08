from copy import deepcopy
from pyaerocom import const

_UNIT_OVERRIDES: None | dict[str, str] = None


def set_unit_overrides(units: dict[str, str]) -> None:
    global _UNIT_OVERRIDES
    units = deepcopy(units)
    if _UNIT_OVERRIDES is None:
        _UNIT_OVERRIDES = units
        return

    if _UNIT_OVERRIDES != units:
        raise ValueError(
            "Units have already been set, and new units dict does not match the old one."
        )

    _UNIT_OVERRIDES = units


def get_standard_unit(var_name: str) -> str:
    """Gets standard unit of AeroCom variable

    Also handles alias names for variables, etc. or strings corresponding to
    older conventions (e.g. names containing 3D).

    Parameters
    ----------
    var_name : str
        AeroCom variable name
    unit_overrides : Optional dict of non-default units, which will be picked first.

    Returns
    -------
    str
        corresponding standard unit

    Units are picked based on the following order (highest priority to lowest):
    1. The units configuration from the user's experiment config.
    2. The default unit configured in variables.ini
    """
    if _UNIT_OVERRIDES is not None:
        if var_name in _UNIT_OVERRIDES:
            return _UNIT_OVERRIDES[var_name]

    return const.VARS[var_name].units
