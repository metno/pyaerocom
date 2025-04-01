import logging

import numpy as np
from geonum.atmosphere import T0_STD, p0

from pyaerocom.io.aux_read_cubes import (
    CUBE_MATHS,
    _check_input_iscube,
    _check_same_units,
    add_cubes,
)
from pyaerocom.units.molecular_mass import get_molmass

from pyaerocom.units import Unit


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
    T_kelvin = T0_STD  # 15 deg celsius (US standard atm)

    mmol_air = get_molmass("air_dry")
    mmol_var = get_molmass(var_name)

    if component_unit is not None and to_unit is not None:
        component_mass = single_component_mass[component_unit.lower()]
        component_unit_fac = component_mass / mmol_var
    else:
        component_unit_fac = 1
    Rspecific = 287.058  # J kg-1 K-1

    conversion_fac = 1 / Unit("mol mol-1").convert(1, vmr_unit)

    airdensity = p_pascal / (Rspecific * T_kelvin)  # kg m-3
    mulfac = mmol_var / mmol_air * airdensity  # kg m-3

    mult_fun = CUBE_MATHS["multiply"]
    conc = mult_fun(data, mulfac)  # kg m-3
    if to_unit is not None:
        conversion_fac *= Unit("kg m-3").convert(1, to_unit) * component_unit_fac
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


def calc_concNnh3_from_vmr(data):
    return vmr_to_conc(
        data, vmr_unit="nmol mol-1", var_name="nh3", to_unit="ug m-3", component_unit="N"
    )


def convert_to_ugN(data, var_name):
    mult_fun = CUBE_MATHS["multiply"]
    data = _check_input_iscube(data)[0]
    mmol_var = get_molmass(var_name)

    component_mass = single_component_mass["n"]
    component_unit_fac = component_mass / mmol_var
    unit = data.units
    unit_conversion = Unit(str(unit)).convert(1, "ug m-3")
    if not np.isclose(unit_conversion, 1, rtol=1e-7):
        data = mult_fun(data, unit_conversion)

    data = mult_fun(data, component_unit_fac)
    data.units = "ug N m-3"

    return data


def calc_concNnh4(concnh4):
    return convert_to_ugN(concnh4, "nh4")


def calc_concno3pm25(concno3f, concno3c, fine_from_coarse_fraction: float = 0.134):
    # mult_fun = CUBE_MATHS["multiply"]
    # concno3pm25 = add_cubes(concno3f, mult_fun(concno3c, fine_from_coarse_fraction))

    return concno3f


def calc_concno3pm10(concno3f, concno3c):
    concno3pm10 = add_cubes(concno3f, concno3c)

    return concno3pm10


def calc_concNno3pm25(concno3f, concno3c, fine_from_coarse_fraction: float = 0.134):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + M_O * 3)
    mult_fun = CUBE_MATHS["multiply"]
    concno3f, concno3c = _check_input_iscube(concno3f, concno3c)
    concno3f, concno3c = _check_same_units(concno3f, concno3c)
    concno3pm25 = add_cubes(concno3f, mult_fun(concno3c, fine_from_coarse_fraction))
    concno3pm25.units = "ug N m-3"
    return mult_fun(concno3pm25, fac)


def calc_concNno3pm10(concno3f, concno3c):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + M_O * 3)
    mult_fun = CUBE_MATHS["multiply"]
    concno3f, concno3c = _check_input_iscube(concno3f, concno3c)
    concno3f, concno3c = _check_same_units(concno3f, concno3c)
    concno3pm10 = add_cubes(concno3f, concno3c)
    concno3pm10.units = "ug N m-3"
    return mult_fun(concno3pm10, fac)


def calc_sspm25(concssfine, concsscoarse):
    mult_fun = CUBE_MATHS["multiply"]
    concssfine, concsscoarse = _check_input_iscube(concssfine, concsscoarse)
    concssfine, concsscoarse = _check_same_units(concssfine, concsscoarse)

    return add_cubes(concssfine, mult_fun(concsscoarse, 0.16))


def calc_concNtno3(concno3f, concno3c, vmrhno3):
    concno3f, concno3c, vmrhno3 = _check_input_iscube(concno3f, concno3c, vmrhno3)
    concno3f, concno3c = _check_same_units(concno3f, concno3c)
    concNhno3 = calc_concNhno3_from_vmr(vmrhno3)
    concNno3pm10 = calc_concNno3pm10(concno3f, concno3c)

    return add_cubes(concNhno3, concNno3pm10)


def calc_concNtnh(concnh4, vmrnh3):
    concNnh3 = calc_concNnh3_from_vmr(vmrnh3)
    concNnh4 = calc_concNnh4(concnh4)
    concNnh3, concNnh4 = _check_same_units(concNnh3, concNnh4)

    return add_cubes(concNnh3, concNnh4)
