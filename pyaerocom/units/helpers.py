from pyaerocom import const


def get_standard_unit(var_name: str) -> str:
    """Gets standard unit of AeroCom variable

    Also handles alias names for variables, etc. or strings corresponding to
    older conventions (e.g. names containing 3D).

    Parameters
    ----------
    var_name : str
        AeroCom variable name

    Returns
    -------
    str
        corresponding standard unit
    """
    return const.VARS[var_name].units
