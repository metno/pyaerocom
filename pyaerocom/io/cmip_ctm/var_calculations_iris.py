import logging

import iris.cube
import xarray as xr

logger = logging.getLogger(__name__)


def add_dataarrays(arr0: xr.DataArray, *arrs: xr.DataArray) -> xr.DataArray:
    """
    Add a bunch of :class:`xarray.DataArray` instances

    Parameters
    ----------
    *arr0
        first input array (instance of :class:`xarray.DataArray` with same shape).
    *arrs
        Additional input arrays (instances of :class:`xarray.DataArray` with same shape)

    Returns
    -------
    xarray.DataArray
        Added array
    """
    result = arr0.copy(deep=True)
    for arr in arrs:
        result += arr
    return result


def subtract_dataarrays(arr0: xr.DataArray, *arrs: xr.DataArray) -> xr.DataArray:
    """
    Subtract a bunch of :class:`xarray.DataArray` instances from an array

    Parameters
    ----------
    arr0
        Input array (instance of :class:`xarray.DataArray` with same shape).
    *arrs
        input arrays (instances of :class:`xarray.DataArray` with same shape).
        Subtraction is performed with respect to `arr0`.

    Returns
    -------
    xarray.DataArray
        Diff array (all additional ones are subtracted from `arr0`)
    """
    result = arr0.copy(deep=True)
    for arr in arrs:
        result -= arr
    return result


def calc_concso4(
    mmrso4_surf: iris.cube.Cube, ps: iris.cube.Cube, tas: iris.cube.Cube
) -> iris.cube.Cube:
    # calculate concso4 from mmrso4
    # x.ps/287.0/x.tas)*x.mmrso4_surf*1e9
    res_cube = ps / 287.0 / tas * mmrso4_surf * 1.0e9
    res_cube.standard_name = "mass_concentration_of_sulfate_ambient_aerosol_particles_in_air"
    res_cube.var_name = "concso4"
    res_cube.units = "ug m-3"
    return res_cube
