import logging

import iris.cube

logger = logging.getLogger(__name__)

"""
This module contains calculations for new variables using iris

IMPORTANT:
One has to set the variable name and the unit to something pyaerocom understands by setting
var_name and units.
For new properties, setting the standard name is not strictly necessary, but helpful for understanding

The result has to be of the type iris.cube.Cube because that is the only thing pyaerocom's 
GriddedData object understands at the moment
"""


def calc_concso4(
    mmrso4_surf: iris.cube.Cube, ps: iris.cube.Cube, tas: iris.cube.Cube
) -> iris.cube.Cube:
    # calculate concso4 from mmrso4
    # x.ps/287.0/x.tas)*x.mmrso4_surf*1e9
    res_cube = ps / 287.0 / tas * mmrso4_surf * 1.0e9
    res_cube.standard_name = "mass_concentration_of_sulfate_ambient_aerosol_particles_in_air"
    res_cube.var_name = "concso4"
    res_cube.units = "ug m-3"
    logger.info(f"var_name {res_cube.var_name} successfully computed.")
    return res_cube


def calc_concso2(
    so2_surf: iris.cube.Cube, ps: iris.cube.Cube, tas: iris.cube.Cube
) -> iris.cube.Cube:
    # calculate concso4 from mmrso4
    # x.ps/287.0/x.tas)*x.mmrso4_surf*1e9
    res_cube = ps / 287.0 / tas * so2_surf * 1.0e9
    res_cube.standard_name = "mass_concentration_of_sulfur_dioxide_in_air"
    res_cube.var_name = "concso2"
    res_cube.units = "ug m-3"
    logger.info(f"var_name {res_cube.var_name} successfully computed.")
    return res_cube


def calc_vmro3(o3_surf: iris.cube.Cube) -> iris.cube.Cube:
    # the climate models store vmro3 in the unit mol mol-1
    # only the factor of 1.E9 is missing
    res_cube = o3_surf * 1.0e9
    res_cube.var_name = "vmro3"
    res_cube.units = "nmol mol-1"
    logger.info(f"var_name {res_cube.var_name} successfully computed.")
    return res_cube
