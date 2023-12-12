import xarray as xr
from geonum.atmosphere import T0_STD, p0

from pyaerocom.aux_var_helpers import concx_to_vmrx
from pyaerocom.molmasses import get_molmass


def add_dataarrays(*arrs: xr.DataArray) -> xr.DataArray:
    """
    Add a bunch of :class:`xarray.DataArray` instances

    Parameters
    ----------
    *arrs
        input arrays (instances of :class:`xarray.DataArray` with same shape)

    Returns
    -------
    xarray.DataArray
        Added array

    """
    if not len(arrs) > 1:  # pragma: no cover
        raise ValueError("Need at least 2 input arrays to add")
    result = arrs[0].copy(deep=True)
    for arr in arrs[1:]:
        result += arr
    return result


def subtract_dataarrays(*arrs: xr.DataArray) -> xr.DataArray:
    """
    Subtract a bunch of :class:`xarray.DataArray` instances from an array

    Parameters
    ----------
    *arrs
        input arrays (instances of :class:`xarray.DataArray` with same shape).
        Subtraction is performed with respect to the first input array.


    Returns
    -------
    xarray.DataArray
        Diff array (all additional ones are subtracted from first array)

    """
    if not len(arrs) > 1:  # pragma: no cover
        raise ValueError("Need at least 2 input arrays to add")
    result = arrs[0].copy(deep=True)
    for arr in arrs[1:]:
        result -= arr
    return result


def calc_concNhno3(*arrs: xr.DataArray) -> xr.DataArray:
    if len(arrs) > 1:  # pragma: no cover
        raise ValueError("Shoul only be given 1 array")

    M_N = 14.006
    M_O = 15.999
    M_H = 1.007

    conchno3 = arrs[0].copy(deep=True)
    fac = M_N / (M_H + M_N + M_O * 3)
    concNhno3 = conchno3 * fac
    concNhno3.attrs["units"] = "ug N m-3"
    return concNhno3


# ToDo: add docstring
def calc_concNno3pm10(concno3f: xr.DataArray, concno3c: xr.DataArray) -> xr.DataArray:
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + 3 * M_O)
    concno3pm10 = concno3f + concno3c
    concNno3pm10 = concno3pm10 * fac
    concNno3pm10.attrs["var_name"] = "concNno3pm10"
    concNno3pm10.attrs["units"] = "ug N m-3"
    return concNno3pm10


# ToDo: add docstring
def calc_concNno3pm25(
    concno3f: xr.DataArray, concno3c: xr.DataArray, fine_from_coarse_fraction: float = 0.134
) -> xr.DataArray:
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + 3 * M_O)
    concno3pm25 = concno3f + fine_from_coarse_fraction * concno3c
    concNno3pm25 = concno3pm25 * fac
    concNno3pm25.attrs["var_name"] = "concNno3pm25"
    concNno3pm25.attrs["units"] = "ug N m-3"
    return concNno3pm25


# ToDo: add docstring
def calc_concno3pm10(concno3f, concno3c):
    concno3pm10 = concno3f + concno3c

    concno3pm10.attrs["var_name"] = "concno3pm10"
    concno3pm10.attrs["units"] = "ug m-3"

    return concno3pm10


# ToDo: add docstring
def calc_concno3pm25(concno3f, concno3c, fine_from_coarse_fraction=0.134):
    concno3pm25 = concno3f + fine_from_coarse_fraction * concno3c

    concno3pm25.attrs["var_name"] = "concno3pm25"
    concno3pm25.attrs["units"] = "ug m-3"
    return concno3pm25


def calc_conNtno3(
    conchno3: xr.DataArray, concno3f: xr.DataArray, concno3c: xr.DataArray
) -> xr.DataArray:
    concNhno3 = calc_concNhno3(conchno3)
    concNno3pm10 = calc_concNno3pm10(concno3f, concno3c)

    concNtno3 = concNhno3 + concNno3pm10
    concNtno3.attrs["units"] = "ug N m-3"
    return concNtno3


# ToDo: add docstring
def calc_concNnh3(*arrs: xr.DataArray) -> xr.DataArray:
    if len(arrs) > 1:  # pragma: no cover
        raise ValueError("Shoul only be given 1 array")

    M_N = 14.006
    M_H = 1.007

    concnh3 = arrs[0].copy(deep=True)
    concNnh3 = concnh3 * (M_N / (M_H * 3 + M_N))
    concNnh3.attrs["units"] = "ug N m-3"
    return concNnh3


# ToDo: add docstring
def calc_concNnh4(*arrs: xr.DataArray) -> xr.DataArray:
    if len(arrs) > 1:  # pragma: no cover
        raise ValueError("Shoul only be given 1 array")

    M_N = 14.006
    M_H = 1.007

    concnh4 = arrs[0].copy(deep=True)
    concNnh4 = concnh4 * (M_N / (M_H * 4 + M_N))
    concNnh4.attrs["units"] = "ug N m-3"
    return concNnh4


# ToDo: add docstring
def calc_concNtnh(concnh3: xr.DataArray, concnh4: xr.DataArray) -> xr.DataArray:
    concNnh3 = calc_concNnh3(concnh3)
    concNnh4 = calc_concNnh4(concnh4)

    concNtnh = concNnh3 + concNnh4
    concNtnh.attrs["units"] = "ug N m-3"
    return concNtnh


# ToDo: add docstring
def update_EC_units(concecpm25: xr.DataArray) -> xr.DataArray:
    concCecpm25 = concecpm25
    concCecpm25.attrs["units"] = "ug C m-3"

    return concCecpm25


def calc_concsspm25(
    concssf: xr.DataArray, concssc: xr.DataArray, coarse_fraction: float = 0.13
) -> xr.DataArray:
    """
    Calculate PM2.5 seasalt

    Parameters
    ----------
    concssf : xr.DataArray
        EMEP output fine seasalt
    concssc : xr.DataArray
        EMEP output coarse seasalt
    coarse_fraction : float
        fraction of coarse supposed to be added to fine output, defaults to
        0.13.

    Returns
    -------
    xr.DataArray
        PM2.5 seasalt including input coarse fraction

    """
    concsspm25 = concssf + coarse_fraction * concssc

    concsspm25.attrs["units"] = "ug m-3"
    return concsspm25


def calc_vmrox(concno2: xr.DataArray, vmro3: xr.DataArray) -> xr.DataArray:
    """
    Calculate OX VMR from NO2 concentration and O3 VMR

    Converts NO2 conc to NO2 VMR assuming US standard atmosphere and adds
    that with VMR O3.

    Parameters
    ----------
    concno2 : xr.DataArray
        mass concentration of NO2
    vmro3 : xr.DataArray
        volume mixing ratio of O3

    Returns
    -------
    xr.DataArray
        volume mixing ratio of OX (O3 + NO2) in units of nmole mole-1

    """
    vmrno2 = concx_to_vmrx(
        data=concno2,
        p_pascal=p0,  # 1013 hPa (US standard atm)
        T_kelvin=T0_STD,  # 15 deg celcius (US standard atm)
        conc_unit=str(concno2.attrs["units"]),
        mmol_var=get_molmass("no2"),  # g/mol NO2
        to_unit="nmol mol-1",
    )

    vmrox = vmrno2 + vmro3
    vmrox.attrs["units"] = "nmol mol-1"
    return vmrox


def calc_vmrox_from_conc(concno2, conco3):
    """
    Calculate OX VMR from NO2 concentration and O3 VMR

    Converts NO2 conc to NO2 VMR assuming US standard atmosphere and adds
    that with VMR O3.

    Parameters
    ----------
    concno2 : xr.DataArray
        mass concentration of NO2
    vmro3 : xr.DataArray
        volume mixing ratio of O3

    Returns
    -------
    xr.DataArray
        volume mixing ratio of OX (O3 + NO2) in units of nmole mole-1

    """
    vmrno2 = concx_to_vmrx(
        data=concno2,
        p_pascal=p0,  # 1013 hPa (US standard atm)
        T_kelvin=T0_STD,  # 15 deg celcius (US standard atm)
        conc_unit=str(concno2.attrs["units"]),
        mmol_var=get_molmass("no2"),  # g/mol NO2
        to_unit="nmol mol-1",
    )

    vmro3 = concx_to_vmrx(
        data=conco3,
        p_pascal=p0,  # 1013 hPa (US standard atm)
        T_kelvin=T0_STD,  # 15 deg celcius (US standard atm)
        conc_unit=str(conco3.attrs["units"]),
        mmol_var=get_molmass("o3"),  # g/mol O3
        to_unit="nmol mol-1",
    )

    vmrox = vmrno2 + vmro3
    vmrox.attrs["units"] = "nmol mol-1"
    return vmrox


def calc_vmrno2(concno2: xr.DataArray) -> xr.DataArray:
    vmrno2 = concx_to_vmrx(
        data=concno2,
        p_pascal=p0,  # 1013 hPa (US standard atm)
        T_kelvin=T0_STD,  # 15 deg celcius (US standard atm)
        conc_unit=str(concno2.attrs["units"]),
        mmol_var=get_molmass("no2"),  # g/mol NO2
        to_unit="nmol mol-1",
    )

    vmrno2.attrs["units"] = "nmol mol-1"
    return vmrno2


def identity(arr):
    return arr


def calc_conNtno3_emep(*arrs):
    if len(arrs) > 1:
        raise ValueError("Should only be given 1 array")

    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + 3 * M_O)

    concNtno3 = arrs[0].copy(deep=True)
    concNtno3 = concNtno3 * fac
    concNtno3.attrs["units"] = "ug N m-3"

    return concNtno3


def calc_conNtnh_emep(*arrs):
    if len(arrs) > 1:
        raise ValueError("Should only be given 1 array")

    M_N = 14.006
    M_H = 1.007

    fac = M_N / (M_H * 4 + M_N)

    conNtnh = arrs[0].copy(deep=True)
    conNtnh = conNtnh * fac
    conNtnh.attrs["units"] = "ug N m-3"

    return conNtnh


def calc_concso4t(concso4, concss):
    factor = 0.007
    concso4t = concso4 + factor * concss
    concso4t.attrs["units"] = "ug m-3"

    return concso4t


def calc_concNno(concno):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + M_O)

    concno = concno.copy(deep=True)
    concNno = concno * fac
    concNno.attrs["units"] = "ug N m-3"

    return concNno


def calc_vmro3(conco3):
    vmro3 = concx_to_vmrx(
        data=conco3,
        p_pascal=p0,  # 1013 hPa (US standard atm)
        T_kelvin=T0_STD,  # 15 deg celcius (US standard atm)
        conc_unit=str(conco3.attrs["units"]),
        mmol_var=get_molmass("o3"),  # g/mol O3
        to_unit="nmol mol-1",
    )

    vmro3.attrs["units"] = "nmol mol-1"
    return vmro3


def calc_concNno2(concno2):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + M_O * 2)

    concno2 = concno2.copy(deep=True)
    concNno2 = concno2 * fac
    concNno2.attrs["units"] = "ug N m-3"

    return concNno2


def calc_concSso2(concso2):
    M_O = 15.999
    M_S = 32.065
    fac = M_S / (M_S + M_O * 2)

    concso2 = concso2.copy(deep=True)
    concSso2 = concso2 * fac
    concSso2.attrs["units"] = "ug S m-3"

    return concSso2
