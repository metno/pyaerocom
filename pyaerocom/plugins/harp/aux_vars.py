from geonum import atmosphere as atm

from pyaerocom import const
from pyaerocom.aux_var_helpers import concx_to_vmrx
from pyaerocom.molmasses import get_molmass

P_STD = atm.p0  # standard atmosphere pressure
T_STD = atm.T0_STD  # standard atmosphere temperature


def _conc_to_vmr_single_value(
    data, to_var, to_unit, from_unit, p_pascal=None, T_kelvin=None, mmol_air=None
):
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


def _conc_to_vmr(data, to_var, to_unit, from_unit, p_pascal=None, T_kelvin=None, mmol_air=None):
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


def _conc_to_vmr_marcopolo_stats(
    data, to_var, from_var, p_pascal=None, T_kelvin=None, mmol_air=None
):
    if p_pascal is None:
        p_pascal = P_STD
    if T_kelvin is None:
        T_kelvin = T_STD
    if mmol_air is None:
        mmol_air = get_molmass("air_dry")

    for stat in data:
        if not from_var in stat:
            continue

        concdata = stat[from_var]

        mmol_var = get_molmass(to_var)
        from_unit = stat["var_info"][from_var]["units"]
        to_unit = const.VARS[to_var].units
        vmrvals = concx_to_vmrx(
            concdata,
            p_pascal=p_pascal,
            T_kelvin=T_kelvin,
            mmol_var=mmol_var,
            mmol_air=mmol_air,
            conc_unit=from_unit,
            to_unit=to_unit,
        )
        stat[to_var] = vmrvals
        vi = {}
        vi.update(stat["var_info"][from_var])
        vi["computed"] = True
        vi["units"] = to_unit
        vi["units_info"] = (
            f"The original data is provided as mass conc. in units of ug m-3 and "
            f"was converted to ppb assuming a standard atmosphere "
            f"(p={p_pascal/100}hPa, T={T_kelvin}K) assuming dry molar mass of air "
            f"M_Air_dry={mmol_air}g/mol and total molecular mass of "
            f"{from_var}={mmol_var}g/mol"
        )
        stat["var_info"][to_var] = vi

    return data
