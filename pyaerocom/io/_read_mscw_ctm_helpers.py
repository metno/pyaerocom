from geonum.atmosphere import p0, T0_STD
from pyaerocom.aux_var_helpers import concx_to_vmrx
from pyaerocom.molmasses import get_molmass
from pyaerocom.units_helpers import get_unit_conversion_fac


def add_dataarrays(*arrs):
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
    if not len(arrs) > 1:
        raise ValueError('Need at least 2 input arrays to add')
    result = arrs[0].copy(deep=True)
    for arr in arrs[1:]:
        result += arr
    return result


def subtract_dataarrays(*arrs):
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
    if not len(arrs) > 1:
        raise ValueError('Need at least 2 input arrays to add')
    result = arrs[0].copy(deep=True)
    for arr in arrs[1:]:
        result -= arr
    return result


def calc_concNhno3(*arrs):
    if len(arrs)>1:
        raise ValueError('Shoul only be given 1 array')

    M_N = 14.006
    M_O = 15.999
    M_H = 1.007

    conchno3 = arrs[0].copy(deep=True)
    fac = (M_N / (M_H + M_N + M_O * 3))
    concNhno3 = conchno3*fac
    concNhno3.attrs['units'] = 'ug N m-3'
    return concNhno3

# ToDo: add docstring
def calc_concNno3pm10(concno3f,concno3c):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + 3*M_O)
    concno3pm10 = concno3f + concno3c
    concNno3pm10 = concno3pm10*fac
    concNno3pm10.attrs['var_name'] = 'concNno3pm10'
    concNno3pm10.attrs['units'] = 'ug N m-3'
    return concNno3pm10

# ToDo: add docstring
def calc_concNno3pm25(concno3f,concno3c,fine_from_coarse_fraction=0.134):
    M_N = 14.006
    M_O = 15.999

    fac = M_N / (M_N + 3*M_O)
    concno3pm25 = concno3f + fine_from_coarse_fraction*concno3c
    concNno3pm25 = concno3pm25*fac
    concNno3pm25.attrs['var_name'] = 'concNno3pm25'
    concNno3pm25.attrs['units'] = 'ug N m-3'
    return concNno3pm25

# ToDo: add docstring
def calc_conNtno3(conchno3,concno3f,concno3c):
    concNhno3 = calc_concNhno3(conchno3)
    concNno3pm10 = calc_concNno3pm10(concno3f,concno3c)

    concNtno3 = concNhno3 + concNno3pm10
    concNtno3.attrs['units'] = 'ug N m-3'
    return concNtno3

# ToDo: add docstring
def calc_concNnh3(*arrs):
    if len(arrs)>1:
        raise ValueError('Shoul only be given 1 array')

    M_N = 14.006
    M_H = 1.007

    concnh3 = arrs[0].copy(deep=True)
    concNnh3 = concnh3*(M_N / (M_H * 3 + M_N))
    concNnh3.attrs['units'] = 'ug N m-3'
    return concNnh3

# ToDo: add docstring
def calc_concNnh4(*arrs):
    if len(arrs)>1:
        raise ValueError('Shoul only be given 1 array')

    M_N = 14.006
    M_H = 1.007

    concnh4 = arrs[0].copy(deep=True)
    concNnh4 = concnh4*(M_N / (M_H * 4 + M_N))
    concNnh4.attrs['units'] = 'ug N m-3'
    return concNnh4

# ToDo: add docstring
def calc_concNtnh(concnh3,concnh4):
    concNnh3 = calc_concNnh3(concnh3)
    concNnh4 = calc_concNnh4(concnh4)

    concNtnh = concNnh3 + concNnh4
    concNtnh.attrs['units'] = 'ug N m-3'
    return concNtnh

# ToDo: add docstring
def update_EC_units(concecpm25):
    concCecpm25 = concecpm25
    concCecpm25.attrs['units'] = 'ug C m-3'

    return concCecpm25


def calc_concsspm25(concssf, concssc, coarse_fraction=0.13):
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
    concsspm25 = concssf + coarse_fraction*concssc

    concsspm25.attrs['units'] = 'ug m-3'
    return concsspm25


def calc_vmrox(concno2, vmro3):
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
    o3mulfac = get_unit_conversion_fac(1, vmro3.attrs['units'], 'nmole mole-1')
    if o3mulfac != 1:
        vmro3 = vmro3.copy(deep=True)
        vmro3 *= o3mulfac
        vmro3.attrs['units'] = 'nmole mole-1'

    vmrno2 = concx_to_vmrx(
        data=concno2,
        p_pascal=p0, # 1013 hPa (US standard atm)
        T_kelvin=T0_STD, #15 deg celcius (US standard atm)
        conc_unit=str(concno2.attrs['units']),
        mmol_var=get_molmass('no2'), # g/mol NO2
        to_unit="nmol mol-1"
    )

    vmrox = vmrno2 + vmro3
    vmrox.attrs["units"] = "nmol mol-1"
    return vmrox