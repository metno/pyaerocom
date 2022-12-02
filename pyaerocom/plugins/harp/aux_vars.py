from geonum import atmosphere as atm

from pyaerocom.aux_var_helpers import concx_to_vmrx
from pyaerocom.molmasses import get_molmass

P_STD = atm.p0  # standard atmosphere pressure
T_STD = atm.T0_STD  # standard atmosphere temperature


def conc_to_vmr(data, to_var, to_unit, from_unit, p_pascal=None, T_kelvin=None, mmol_air=None):
    if p_pascal is None:
        p_pascal = P_STD
    if T_kelvin is None:
        T_kelvin = T_STD
    if mmol_air is None:
        mmol_air = get_molmass("air_dry")

    mmol_var = get_molmass(to_var[0])

    return concx_to_vmrx(
        data,
        p_pascal=p_pascal,
        T_kelvin=T_kelvin,
        mmol_var=mmol_var,
        mmol_air=mmol_air,
        conc_unit=from_unit,
        to_unit=to_unit,
    )
