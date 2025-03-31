from .units import Unit
from typing import TypeVar
from pyaerocom.units.exceptions import UnitConversionError


T = TypeVar("T")
#: default frequency for rates variables (e.g. deposition, precip)
RATES_FREQ_DEFAULT = "d"


def get_unit_conversion_fac(
    from_unit: str, to_unit: str, var_name: str | None = None, ts_type: str | None = None
) -> float:
    return convert_unit(
        1, from_unit=from_unit, to_unit=to_unit, var_name=var_name, ts_type=ts_type
    )


def convert_unit(
    data: T, from_unit: str, to_unit: str, var_name: str | None = None, ts_type: str | None = None
) -> T:
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
        such as precip, deposition, etc, that may be defined implicitly
        without proper frequency specification in the unit string.

    Returns
    -------
    data
        data in new unit
    """
    try:
        data = Unit(from_unit, aerocom_var=var_name, ts_type=ts_type).convert(
            data, other=Unit(to_unit, aerocom_var=var_name, ts_type=ts_type)
        )
    except ValueError as e:
        raise UnitConversionError(
            f"failed to convert unit from {str(from_unit)} to {to_unit}"
        ) from e

    return data
