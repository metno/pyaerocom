from __future__ import annotations
import pytest

import iris
import numpy as np


from pyaerocom.colocation_3d import (
    colocate_vertical_profile_gridded,
    ColocatedDataLists,
)


@pytest.fixture(scope="module")
def fake_model_data_with_altitude(data_tm5):
    # Idea is to just hack together GriddedData object with this data that already is in CI. fine if nonsense
    data1 = data_tm5
    data2 = data_tm5
    data3 = data_tm5
    cube_list = iris.cube.CubeList([data1.cube, data2.cube, data3.cube])
    data = cube_list.concatenate()
    altitude = iris.coords.DimCoord(
        np.linspace(0, 60000, 1000), standard_name="altitude", units="meters"
    )
    breakpoint()
    return data1


def create_fake_vertical_profile_data(aeronetsunv3lev2_subset):
    # breakpoint()
    pass


def test_colocate_vertical_profile_gridded(fake_model_data_with_altitude):
    model_data = fake_model_data_with_altitude
    breakpoint()
    pass
