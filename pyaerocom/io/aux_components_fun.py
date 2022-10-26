import logging
from traceback import format_exc

import cf_units
import iris
import numpy as np
from geonum.atmosphere import T0_STD, p0

from pyaerocom._lowlevel_helpers import merge_dicts
from pyaerocom.helpers import copy_coords_cube
from pyaerocom.io.aux_read_cubes import (
    CUBE_MATHS,
    _check_input_iscube,
    _check_same_units,
    add_cubes,
)
from pyaerocom.molmasses import get_mmr_to_vmr_fac, get_molmass
from pyaerocom.units_helpers import get_unit_conversion_fac

logger = logging.getLogger(__name__)


single_component_mass = {"n": 14.0067, "c": 12.011, "s": 32.065}


def vmr_to_conc(data, vmr_unit, var_name, to_unit, component_unit=None):
    """
    Convert volume mixing ratio (vmr) to mass concentration

    Parameters
    ----------
    data : cube or GriddedData
        array containing vmr values

    vmr_unit : str
        unit of input data
    var_name: str
        name of variable, used to fund molar mass
    to_unit : str, optional
        Unit to which output data is converted. If None, output unit is
        kg m-3. The default is None.
    component_unit : str, optional
        If none, the to_unit unit is returned. If, e.g. n or N, then ug m-3 -> ug N m-3 is returned

    Returns
    -------
    cube
        input data converted to mass concentration

    """

    data = _check_input_iscube(data)[0]

    p_pascal = p0  # 1013 hPa (US standard atm)
    T_kelvin = T0_STD  # 15 deg celcius (US standard atm)

    mmol_air = get_molmass("air_dry")
    mmol_var = get_molmass(var_name)

    if component_unit is not None and to_unit is not None:
        component_mass = single_component_mass[component_unit.lower()]
        component_unit_fac = component_mass / mmol_var
    else:
        component_unit_fac = 1
    Rspecific = 287.058  # J kg-1 K-1

    conversion_fac = 1 / cf_units.Unit("mol mol-1").convert(1, vmr_unit)

    airdensity = p_pascal / (Rspecific * T_kelvin)  # kg m-3
    mulfac = mmol_var / mmol_air * airdensity  # kg m-3

    mult_fun = CUBE_MATHS["multiply"]
    conc = mult_fun(data, mulfac)  # kg m-3
    if to_unit is not None:
        conversion_fac *= cf_units.Unit("kg m-3").convert(1, to_unit) * component_unit_fac
    if not np.isclose(conversion_fac, 1, rtol=1e-7):
        conc = mult_fun(conc, conversion_fac)

    if to_unit is not None:
        unit = to_unit

        if component_unit is not None:
            unit_list = unit.split(" ")
            unit = unit_list[0] + f" {component_unit.upper()} " + unit_list[1]

        conc.units = unit
    else:
        conc.units = "kg m-3"

    return conc


def calc_concNhno3_from_vmr(data):

    return vmr_to_conc(
        data, vmr_unit="nmol mol-1", var_name="hno3", to_unit="ug m-3", component_unit="N"
    )


def calc_concno3pm25(concno3f, concno3c, fine_from_coarse_fraction: float = 0.134):
    mult_fun = CUBE_MATHS["multiply"]
    concno3pm25 = add_cubes(concno3f, mult_fun(concno3c, fine_from_coarse_fraction))

    return concno3pm25


def calc_concno3pm10(concno3f, concno3c):
    mult_fun = CUBE_MATHS["multiply"]
    concno3pm10 = add_cubes(concno3f, concno3c)

    return concno3pm10


def calc_sspm25(concssfine, concsscoarse):
    mult_fun = CUBE_MATHS["multiply"]
    concssfine, concsscoarse = _check_input_iscube(concssfine, concsscoarse)
    concssfine, concsscoarse = _check_same_units(concssfine, concsscoarse)

    return add_cubes(concssfine, mult_fun(concsscoarse, 0.16))
