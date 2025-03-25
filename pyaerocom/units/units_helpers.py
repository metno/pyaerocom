from pyaerocom.units.exceptions import UnitConversionError

from .unit import PyaerocomUnit

#: default frequency for rates variables (e.g. deposition, precip)
RATES_FREQ_DEFAULT = "d"

# may be used to specify alternative names for custom units  defined
# in UCONV_MUL_FACS

UALIASES = {
    # mass concentrations
    "ug S m-3": "ug S/m3",
    "ug C m-3": "ug C/m3",
    "ug N m-3": "ug N/m3",
    "ugC/m3": "ug C m-3",
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


def get_unit_conversion_fac(from_unit: str, to_unit: str, var_name=None, ts_type=None):
    try:
        factor = PyaerocomUnit(from_unit, aerocom_var=var_name, ts_type=ts_type).convert(
            1, other=PyaerocomUnit(to_unit, aerocom_var=var_name, ts_type=ts_type)
        )
    except ValueError as e:
        raise UnitConversionError(
            f"failed to convert unit from {str(from_unit)} to {to_unit}"
        ) from e

    return factor


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
    try:
        factor = PyaerocomUnit(from_unit, aerocom_var=var_name, ts_type=ts_type).convert(
            1, other=PyaerocomUnit(to_unit, aerocom_var=var_name, ts_type=ts_type)
        )
    except ValueError as e:
        raise UnitConversionError(
            f"failed to convert unit from {str(from_unit)} to {to_unit}"
        ) from e

    return data * factor
