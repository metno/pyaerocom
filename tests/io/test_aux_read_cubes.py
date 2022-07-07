from __future__ import annotations

import numpy as np
import pytest
from iris.coords import DimCoord
from iris.cube import Cube

from pyaerocom.io.aux_read_cubes import (
    add_cubes,
    compute_angstrom_coeff_cubes,
    divide_cubes,
    mmr_from_vmr,
    multiply_cubes,
    rho_from_ts_ps,
    subtract_cubes,
)


@pytest.fixture
def simple_cube():
    latitude = DimCoord(np.linspace(-90, 90, 4), standard_name="latitude", units="degrees")
    longitude = DimCoord(np.linspace(45, 360, 8), standard_name="longitude", units="degrees")
    cube = Cube(np.ones((4, 8), np.float32), dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
    return cube


def test_add_cubes(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    summed_cube = add_cubes(cube1, cube2)
    assert np.all(cube1.data + cube2.data == summed_cube.data)


def test_subract_cubes(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    differenced_cube = subtract_cubes(cube1, cube2)
    assert np.all(cube1.data - cube2.data == differenced_cube.data)


def test_multiple_cubes(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    multiplied_cube = multiply_cubes(cube1, cube2)
    assert np.all(cube1.data * cube2.data == multiplied_cube.data)


def test_divide_cubes(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    divided_cube = divide_cubes(cube1, cube2)
    assert np.all(cube1.data / cube2.data == divided_cube.data)


def test_compute_angstrom_coeff_cubes(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    ang_cube = compute_angstrom_coeff_cubes(cube1, cube2, lambda1=1, lambda2=2)
    assert np.all(ang_cube.data) == 0


def test_rho_from_ts_ps(simple_cube):
    cube1, cube2 = simple_cube, simple_cube
    rho = rho_from_ts_ps(cube1, cube2)
    assert np.all(rho.data == pytest.approx(287.058, rel=1e-4))


@pytest.mark.parametrize(
    "var_name, expected_result",
    [("air_dry", 1), ("o3", 1.6571896), ("glyox", 2.0036802)],
)
def test_mmr_from_vmr(simple_cube, var_name, expected_result):
    cube = simple_cube
    cube.var_name = var_name
    mmr_cube = mmr_from_vmr(cube)
    assert np.all(mmr_cube.data == pytest.approx(expected_result, rel=1e-4))
