from pyaerocom.units.helpers import get_standard_unit
import logging

logger = logging.getLogger(__name__)


def harmonise_units(data, data_ref, *, var: str, var_ref: str, inplace=False) -> tuple:
    """Tries to perform unit conversion for the provided data object, so that
    the units of the data objects match for the given variable names.

    If var == var_ref, both data objects will be converted to the unit provided
    by pyaerocom.units.get_standard_unit.

    If var != var_ref, both data objects will be attempted converted to the unit
    provided by pyaerocom.units.get_standard_unit for var_ref.

    :param data: Data
    :param data: Reference data.
    :param var: Varname for data.
    :param var_ref: Varname for data_ref.
    :param inplace: Whether to perform conversion inplace.
    :return: tuple of length n, containing converted data and ref_data.
    """
    std_unit = get_standard_unit(var)
    std_unit_ref = get_standard_unit(var_ref)

    if std_unit != std_unit_ref:
        logger.info(
            f"'std_unit' ({std_unit}) and 'std_unit_ref' ({std_unit_ref}) do not match. Attempting to convert both data objects to {std_unit_ref}."
        )

    harmonised_unit = std_unit_ref

    try:
        data = data.convert_unit(harmonised_unit, inplace=inplace)
    except AttributeError:
        data = data.check_convert_var_units(var, to_unit=harmonised_unit, inplace=inplace)

    try:
        data_ref = data_ref.convert_unit(harmonised_unit, inplace=inplace)
    except AttributeError:
        data_ref = data_ref.check_convert_var_units(
            var_ref, to_unit=harmonised_unit, inplace=inplace
        )

    return data, data_ref
