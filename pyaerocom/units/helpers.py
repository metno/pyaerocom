from pyaerocom import const


def get_standard_unit(var_name: str, *, unit_overrides: dict[str, str] | None = None) -> str:
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
    if unit_overrides is None:
        unit_overrides = {}

    if var_name in unit_overrides:
        return unit_overrides[var_name]

    return const.VARS[var_name].units
