import pandas as pd
from cf_units import Unit

from pyaerocom.exceptions import UnitConversionError
from pyaerocom.time_config import SI_TO_TS_TYPE
from pyaerocom.tstype import TsType
from pyaerocom.variable_helpers import get_variable

#: default frequency for rates variables (e.g. deposition, precip)
RATES_FREQ_DEFAULT = "d"

# 1. DEFINITION OF ATOM and MOLECULAR MASSES

# Atoms
M_O = 15.999  # u
M_S = 32.065  # u
M_N = 14.0067  # u
M_H = 1.00784  # u

# Molecules
M_SO2 = M_S + 2 * M_O
M_SO4 = M_S + 4 * M_O

M_NO2 = M_N + 2 * M_O
M_NO3 = M_N + 3 * M_O

M_NH3 = M_N + 3 * M_H
M_NH4 = M_N + 4 * M_H

# Unit conversion and custom units definitions

# 2.1 Other conversion factors
HA_TO_SQM = 10000  # hectar to square metre.

# 3. LOOKUP TABLE FOR CONVERSION FACTORS

#: Custom unit conversion factors for certain variables
#: columns: variable -> from unit -> to_unit -> conversion
#: factor
UCONV_MUL_FACS = pd.DataFrame(
    [
        # ["dryso4", "mg/m2/d", "mgS m-2 d-1", M_S / M_SO4],
        # ["drynh4", "mg/m2/d", "mgN m-2 d-1", M_N/ M_NH4],
        # ["concso4", "ug S/m3", "ug m-3", M_SO4 / M_S],
        # ["SO4ugSm3", "ug/m3", "ug S m-3", M_S / M_SO4],
        # ["concso4pm25", "ug S/m3", "ug m-3", M_SO4 / M_S],
        # ["concso4pm10", "ug S/m3", "ug m-3", M_SO4 / M_S],
        ["concso2", "ug S/m3", "ug m-3", M_SO2 / M_S],
        ["concbc", "ug C/m3", "ug m-3", 1.0],
        ["concoa", "ug C/m3", "ug m-3", 1.0],
        ["concoc", "ug C/m3", "ug m-3", 1.0],
        ["conctc", "ug C/m3", "ug m-3", 1.0],
        # a little hacky for ratpm10pm25...
        # ["ratpm10pm25", "ug m-3", "1", 1.0],
        ["concpm25", "ug m-3", "1", 1.0],
        ["concpm10", "ug m-3", "1", 1.0],
        ["concno2", "ug N/m3", "ug m-3", M_NO2 / M_N],
        # ["concno3", "ug N/m3", "ug m-3", M_NO3 / M_N],
        ["concnh3", "ug N/m3", "ug m-3", M_NH3 / M_N],
        # ["concnh4", "ug N/m3", "ug m-3", M_NH4 / M_N],
        ["wetso4", "kg S/ha", "kg m-2", M_SO4 / M_S / HA_TO_SQM],
        ["concso4pr", "mg S/L", "g m-3", M_SO4 / M_S],
    ],
    columns=["var_name", "from", "to", "fac"],
).set_index(["var_name", "from"])

# may be used to specify alternative names for custom units  defined
# in UCONV_MUL_FACS

UALIASES = {
    # mass concentrations
    "ug S m-3": "ug S/m3",
    "ug C m-3": "ug C/m3",
    "ug N m-3": "ug N/m3",
    "ugC/m3": "ug C/m3",
    # deposition rates (implicit)
    ## sulphur species
    "mgS/m2": "mg S m-2",
    "mgSm-2": "mg S m-2",
    ## nitrogen species
    "mgN/m2": "mg N m-2",
    "mgNm-2": "mg N m-2",
    # deposition rates (explicit)
    ## sulphur species
    "mgS/m2/h": "mg S m-2 h-1",
    "mg/m2/h": "mg m-2 h-1",
    "mgS/m**2/h": "mg S m-2 h-1",
    "mgSm-2h-1": "mg S m-2 h-1",
    "mgSm**-2h-1": "mg S m-2 h-1",
    "mgS/m2/d": "mg S m-2 d-1",
    ## nitrogen species
    "mgN/m2/h": "mg N m-2 h-1",
    "mgN/m**2/h": "mg N m-2 h-1",
    "mgNm-2h-1": "mg N m-2 h-1",
    "mgNm**-2h-1": "mg N m-2 h-1",
    "mgN/m2/d": "mg N m-2 d-1",
    ## others
    "MM/H": "mm h-1",
    # others
    "/m": "m-1",
}


def _check_unit_endswith_freq(unit):
    """
    Check if input unit ends with an SI frequency string

    Considered SI base periods are defined in :attr:`SI_TO_TS_TYPE` (keys)
    and accepted specifications as frequency in unit string are either via
    "/<period>" or "<period>-1" (e.g. "/d" "d-1").

    Parameters
    ----------
    unit : str
        unit to be checked

    Returns
    -------
    bool
        True if input unit ends with valid frequency string, else False
    """
    if isinstance(unit, Unit):
        unit = str(unit)
    for si_unit in SI_TO_TS_TYPE:
        if unit.endswith(f"/{si_unit}") or unit.endswith(f"{si_unit}-1"):
            return True
    return False


def rate_unit_implicit(unit):
    """
    Check whether input rate unit is implicit

    Implicit rate units do not contain frequency string, e.g. "mg m-2"
    instead of "mg m-2 d-1". Such units are, e.g. used in EMEP output where
    the frequency corresponds to the output frequency, e.g. "mg m-2" per day if
    output is daily.

    Note
    ----
    For now, this is just a wrapper for :func:`_check_unit_endswith_freq`,
    but there may be more sophisticated options in the future, which may be
    added to this function.

    Parameters
    ----------
    unit : str
        unit to be tested

    Returns
    -------
    bool
        True if input unit appears to be implicit, else False.

    """
    return not _check_unit_endswith_freq(unit)


def _unit_conversion_fac_custom(var_name, from_unit):
    """Get custom conversion factor for a certain unit

    Tries to determine custom conversion factor for a variable, relative to
    that variables pyaerocom default unit. These are typically conversions
    that cannot be handled by :mod:`cf_units` (e.g. if variable is `concno3`
    which should be in units of "ug m-3" but is given in units of "ug N
    m-3", that is, nitrogen mass and not molecular NO3 mass. Since such atomar
    units are not supported by `cf_units` which is based on SI (it would think
    the "N" is Newton), pyaerocom provides a simple interface to circumvent
    these issues for such variables by providing explicit conversion factors to
    convert from e.g. "ug N m-3" to "ug m-3", for affected variables, such as
    concno3.

    Parameters
    ----------
    var_name : str
        name of variable for which factor is to be determined (needs to be
        registered in global attr. :attr:`UCONV_MUL_FACS`
    from_unit : str
        input unit (e.g. "ug N m-3")

    Raises
    ------
    UnitConversionError
        if no or no unique unit conversion factor could be retrieved for
        input from global attr. :attr:`UCONV_MUL_FACS`

    Returns
    -------
    str
        output unit
    float
        corresponding converison factor
    """
    if from_unit in UALIASES:
        from_unit = UALIASES[from_unit]
    try:
        info = UCONV_MUL_FACS.loc[(var_name, str(from_unit)), :]
        if not isinstance(info, pd.Series):
            raise UnitConversionError(
                "FATAL: Could not find unique conversion factor in table  "
                "UCONV_MUL_FACS in units_helpers.py. Please check for "
                "dulplicate entries"
            )
    except KeyError:
        raise UnitConversionError(
            f"Failed to convert unit {from_unit} (variable {var_name}). "
            f"Reason: no custom conversion factor could be inferred from table "
            f"pyaerocom.units_helpers.UCONV_MUL_FACS"
        )
    return (info.to, info.fac)


def _unit_conversion_fac_si(from_unit, to_unit):
    """Retrieve multiplication factor for unit conversion

    Works only for standard units that are supported by :mod:`cf_units`
    library. See also :func:`get_unit_conversion_factor` for more general
    cases.

    Parameters
    ----------
    from_unit : Unit or str
        input unit
    to_unit : Unit or str
        output unit

    Raises
    ------
    UnitConversionError
        if units cannot be converted into each other using cf_units package

    Returns
    --------
    float
        multiplicative conversion factor


    """
    if isinstance(from_unit, str):
        from_unit = Unit(from_unit)
    try:
        return from_unit.convert(1, to_unit)
    except ValueError:
        raise UnitConversionError(f"Failed to convert unit from {from_unit} to {to_unit}")


def _get_unit_conversion_fac_helper(from_unit, to_unit, var_name=None):
    """
    Helper for unit conversion

    Parameters
    ----------
    from_unit : str
        input unit
    to_unit : str
        output unit
    var_name : str, optional
        associated variable

    Returns
    -------
    float
        multiplication factor to convert data with input unit to output unit
        (e.g. 1000 if input unit is kg and output unit g).

    """
    pre_conv_fac = 1.0
    if from_unit == to_unit:
        # nothing to do
        return 1.0
    elif var_name is not None and var_name in UCONV_MUL_FACS.index:
        try:
            from_unit, pre_conv_fac = _unit_conversion_fac_custom(var_name, from_unit)
        except UnitConversionError:
            # from_unit is likely not custom but standard... and if not
            # call of unit_conversion_fac_si below will crash
            pass

    return _unit_conversion_fac_si(from_unit, to_unit) * pre_conv_fac


def get_unit_conversion_fac(from_unit, to_unit, var_name=None, ts_type=None):
    try:
        return _get_unit_conversion_fac_helper(from_unit, to_unit, var_name)
    except UnitConversionError:
        if (
            ts_type is not None
            and var_name is not None
            and get_variable(var_name).is_rate
            and rate_unit_implicit(from_unit)
        ):
            freq_si = TsType(ts_type).to_si()
            from_unit = f"{from_unit} {freq_si}-1"
            return _get_unit_conversion_fac_helper(from_unit, to_unit, var_name)

    raise UnitConversionError(f"failed to convert unit from {from_unit} to {to_unit}")


def convert_unit(data, from_unit, to_unit, var_name=None, ts_type=None):
    """Convert unit of data

    Parameters
    ----------
    data : np.ndarray or similar
        input data
    from_unit : cf_units.Unit or str
        current unit of input data
    to_unit : cf_units.Unit or str
        new unit of input data
    var_name : str, optional
        name of variable. If provided, and standard conversion with
        :mod:`cf_units` fails, then custom unit conversion is attempted.
    ts_type : str, optional
        frequency of data. May be needed for conversion of rate variables
        such as precip, deposition, etc, that may be defined implictly
        without proper frequency specification in the unit string.

    Returns
    -------
    data
        data in new unit
    """
    conv_fac = get_unit_conversion_fac(from_unit, to_unit, var_name, ts_type)
    if conv_fac != 1:
        data *= conv_fac
    return data
