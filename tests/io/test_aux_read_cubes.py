from __future__ import annotations

from typing import Optional
import pytest
import numpy as np
from iris.coords import DimCoord
from iris.cube import Cube

from pyaerocom.io.aux_read_cubes import(
    CUBE_MATHS,
    compute_angstrom_coeff_cubes,
    add_cubes,
    subtract_cubes,
    multiply_cubes,
    divide_cubes,
    rho_from_ts_ps,

)


def _simple_cube():

    latitude = DimCoord(np.linspace(-90, 90, 4), standard_name='latitude', units='degrees')
    longitude = DimCoord(np.linspace(45, 360, 8), standard_name='longitude', units='degrees')
    cube = Cube(np.ones((4, 8), np.float32), dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
    return cube


def test_add_cubes():
    cube1, cube2 = _simple_cube(), _simple_cube()
    summed_cube = add_cubes(cube1, cube2)
    assert np.all(cube1.data + cube2.data == summed_cube.data)

def test_subract_cubes():
    cube1, cube2 = _simple_cube(), _simple_cube()
    differenced_cube = subtract_cubes(cube1, cube2)
    assert np.all(cube1.data - cube2.data == differenced_cube.data)

def test_multiple_cubes():
    cube1, cube2 = _simple_cube(), _simple_cube()
    multiplied_cube = multiply_cubes(cube1, cube2)
    assert np.all(cube1.data * cube2.data == multiplied_cube.data)

def test_divide_cubes():
    cube1, cube2 = _simple_cube(), _simple_cube()
    divided_cube = divide_cubes(cube1, cube2)
    assert np.all(cube1.data / cube2.data == divided_cube.data)

def test_compute_angstrom_coeff_cubes():
    cube1, cube2 = _simple_cube(), _simple_cube()
    ang_cube = compute_angstrom_coeff_cubes(cube1, cube2, lambda1=1, lambda2=2)
    assert np.all(ang_cube.data) == 0

def test_rho_from_ts_ps():
    ts = _simple_cube()
    ps = _simple_cube()
    rho = rho_from_ts_ps(ts, ps)
    assert np.all(rho.data == pytest.approx(287.058, rel=1e-4))



