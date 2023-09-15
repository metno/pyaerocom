from __future__ import annotations
import pytest

import iris
import numpy as np

from pyaerocom import GriddedData
from pyaerocom.colocation_3d import (
    colocate_vertical_profile_gridded,
    ColocatedDataLists,
)

from pyaerocom.io import ReadAeronetSdaV3, ReadAeronetSunV3
from pyaerocom.ungriddeddata import UngriddedData


# from tests.fixtures.stations import create_fake_station_data
# from tests.fixtures.data_access import TEST_DATA
# from tests.fixtures.aeronet import aeronetsdav3lev2_subset

# import tests.fixtures.aeronet


@pytest.fixture(scope="module")
def fake_model_data_with_altitude():
    longitude = iris.coords.DimCoord(
        np.linspace(-180, 180, 20), standard_name="longitude", units="degrees"
    )
    latitude = iris.coords.DimCoord(
        np.linspace(-90, 90, 10), standard_name="latitude", units="degrees"
    )
    altitude = iris.coords.DimCoord(
        np.linspace(0, 60000, 10000), standard_name="altitude", units="meters"
    )
    time = iris.coords.DimCoord(
        np.arange(19600, 19600 + 7, 1), standard_name="time", units="days since epoch"
    )
    dummy = iris.cube.Cube(
        np.ones((time.shape[0], longitude.shape[0], latitude.shape[0], altitude.shape[0]))
    )
    dummy.name = "extinction"
    data = GriddedData(dummy)
    return data


@pytest.fixture(scope="module")
def fake_obs_data_with_altitude(aeronetsunv3lev2_subset):
    breakpoint()
    pass


# S1 = create_fake_station_data(
#     "ec532aer",
#     {"ec532aer": {"units": "1/km"}},
#     10,
#     "2023-08-31",
#     "2023-09-06",
#     "d",
#     {"ts_type": "daily"},
# )


# @pytest.fixture(scope="module")
# def create_fake_vertical_profile_data(aeronetsunv3lev2_subset):
#     # breakpoint()
#     pass


@pytest.mark.parametrize(
    "data,data_ref,var,var_ref,ts_type,resample_how,min_num_obs,use_climatology_ref,num_valid,colocation_layer_limits,profile_layer_limits",
    [
        (
            fake_model_data_with_altitude,
            fake_obs_data_with_altitude,
            # aeronetsdav3lev2_subset,
            "ec532aer",
            "ec532aer",
            "daily",
            "mean",
            {"monthly": {"daily": 25}},
            False,
            1,
            [
                {"start": 0, "end": 2000},
                {"start": 2000, "end": 4000},
                {"start": 4000, "end": 6000},
            ],
            [
                {"start": 0, "end": 2000},
                {"start": 2000, "end": 4000},
                {"start": 4000, "end": 6000},
            ],
        )
    ],
)
def test_colocate_vertical_profile_gridded(
    data,
    data_ref,
    var,
    var_ref,
    ts_type,
    resample_how,
    min_num_obs,
    use_climatology_ref,
    num_valid,
    colocation_layer_limits,
    profile_layer_limits,
):
    breakpoint()
    # colocated_data_list = colocate_vertical_profile_gridded(
    #     data,
    #     data=data,
    #     data_ref=data_ref,
    #     ts_type=ts_type,
    #     resample_how=resample_how,
    #     min_num_obs=min_num_obs,
    #     use_climatology=use_climatology_ref,
    #     num_valid=num_valid,
    #     colocation_layer_limits=colocation_layer_limits,
    #     profile_layer_limits=profile_layer_limits,
    # )
    # assert colocated_data_list
    pass
