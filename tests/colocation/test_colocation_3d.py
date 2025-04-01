from __future__ import annotations

import iris
import numpy as np
import pytest

from pyaerocom import GriddedData
from pyaerocom._lowlevel_helpers import LayerLimits
from pyaerocom.colocation.colocation_3d import (
    ColocatedDataLists,
    colocate_vertical_profile_gridded,
)
from pyaerocom.io.read_earlinet import ReadEarlinet
from tests.fixtures.data_access import TEST_DATA

ROOT = TEST_DATA["Earlinet-test"].path

TEST_FILE: list[str] = [
    f"{ROOT}/EARLINET_AerRemSen_waw_Lev02_b0532_202109221030_202109221130_v01_qc03.nc",
]


@pytest.fixture
def fake_model_data_with_altitude():
    longitude = iris.coords.DimCoord(
        np.linspace(-15, 25, 20),
        var_name="lon",
        standard_name="longitude",
        units="degrees",
    )
    latitude = iris.coords.DimCoord(
        np.linspace(50, 55, 10),
        var_name="lat",
        standard_name="latitude",
        units="degrees",
    )
    altitude = iris.coords.DimCoord(
        np.linspace(0, 60000, 10000),
        var_name="alt",
        standard_name="altitude",
        units="meters",
    )
    time = iris.coords.DimCoord(
        np.arange(18892, 18892 + 7, 1),
        var_name="time",
        standard_name="time",
        units="days since epoch",
    )
    dummy = iris.cube.Cube(
        np.ones((time.shape[0], longitude.shape[0], latitude.shape[0], altitude.shape[0]))
    )

    latitude.guess_bounds()
    longitude.guess_bounds()
    altitude.guess_bounds()

    dummy.add_dim_coord(time, 0)
    dummy.add_dim_coord(longitude, 1)
    dummy.add_dim_coord(latitude, 2)
    dummy.add_dim_coord(altitude, 3)

    dummy.var_name = "bsc532aer"

    data = GriddedData(dummy)

    return data


@pytest.fixture
def example_earlinet_ungriddeddata():
    reader = ReadEarlinet()
    return reader.read(vars_to_retrieve=["bsc532aer"], files=TEST_FILE[0])


@pytest.mark.parametrize(
    "ts_type,resample_how,min_num_obs,use_climatology_ref,colocation_layer_limits,profile_layer_limits",
    [
        pytest.param(
            "daily",
            "mean",
            {"monthly": {"daily": 25}},
            False,
            ({"start": 0, "end": 6000},),
            ({"start": 0, "end": 6000},),
            id="fake_data",
        )
    ],
)
def test_colocate_vertical_profile_gridded(
    fake_model_data_with_altitude,
    example_earlinet_ungriddeddata,
    ts_type,
    resample_how,
    min_num_obs,
    use_climatology_ref,
    colocation_layer_limits: tuple[LayerLimits, ...],
    profile_layer_limits: tuple[LayerLimits, ...],
):
    colocated_data_list = colocate_vertical_profile_gridded(
        data=fake_model_data_with_altitude,
        data_ref=example_earlinet_ungriddeddata,
        ts_type=ts_type,
        resample_how=resample_how,
        min_num_obs=min_num_obs,
        use_climatology_ref=use_climatology_ref,
        colocation_layer_limits=colocation_layer_limits,
        profile_layer_limits=profile_layer_limits,
    )

    assert colocated_data_list
    assert isinstance(colocated_data_list, ColocatedDataLists)
    assert len(colocated_data_list) == 2  # col objs for statistics and viz
    assert len(colocated_data_list[0]) == len(colocation_layer_limits)
    assert len(colocated_data_list[1]) == len(profile_layer_limits)
    assert all("just_for_viz" in obj.metadata for obj in colocated_data_list[1])
