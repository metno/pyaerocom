from __future__ import annotations

import os.path

import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from pyaerocom import const
from pyaerocom.io.gaw.reader import ReadGAW
from tests.conftest import TEST_RTOL


def skip_flag():
    # for some reason const.OBSLOCS_UNGRIDDED[const.DMS_AMS_CVO_NAME] is not defined on CI
    if const.DMS_AMS_CVO_NAME not in const.OBSLOCS_UNGRIDDED:
        return True
    elif os.path.exists(const.OBSLOCS_UNGRIDDED[const.DMS_AMS_CVO_NAME]):
        return False
    else:
        return True


skip = pytest.mark.skipif(
    skip_flag(),
    reason="GAW path not found (are we on CI?)",
    allow_module_level=True,
)


@pytest.fixture(scope="module")
def gaw_path() -> str:
    return const.OBSLOCS_UNGRIDDED[const.DMS_AMS_CVO_NAME]


@pytest.fixture(scope="module")
def _make_data(gaw_path: str) -> ReadGAW:
    r = ReadGAW(data_dir=gaw_path)
    return r.read("vmrdms")


@pytest.fixture(scope="module")
def data_vmrdms_ams_cvo(_make_data, gaw_path):
    return _make_data


@skip
def test_ungriddeddata_ams_cvo(data_vmrdms_ams_cvo):
    data = data_vmrdms_ams_cvo
    assert data.shape == (15616, 12)
    assert len(data.metadata) == 6

    unique_coords = []
    unique_coords.extend(np.unique(data.latitude))
    unique_coords.extend(np.unique(data.longitude))
    unique_coords.extend(np.unique(data.altitude))
    assert len(unique_coords) == 6
    assert_allclose(unique_coords, [-37.8, 16.848, -24.871, 77.53, 10.0, 65.0], rtol=TEST_RTOL)

    vals = data._data[:, data.index["data"]]
    assert_allclose(
        [np.nanmean(vals), np.nanstd(vals), np.nanmax(vals), np.nanmin(vals)],
        [1.794279e14, 2.352963e14, 2.807600e15, -7.900000e12],
        rtol=TEST_RTOL,
    )


@skip
def test_vmrdms_ams(data_vmrdms_ams_cvo):
    stat = data_vmrdms_ams_cvo.to_station_data(meta_idx=0)

    keys = list(stat)
    assert "vmrdms" in keys
    assert "var_info" in keys

    assert stat.dtime.min() == np.datetime64("1987-03-01T00:00:00.000000000")
    assert stat.dtime.max() == np.datetime64("2008-12-31T00:00:00.000000000")

    assert stat["instrument_name"] == "unknown"
    assert stat["ts_type"] == "daily"
    assert stat["filename"] == "ams137s00.lsce.as.fl.dimethylsulfide.nl.da.dat"

    vmrdms = stat["vmrdms"]
    assert_allclose(
        [vmrdms.mean(), vmrdms.std(), vmrdms.max(), vmrdms.min()],
        [1.856801e14, 2.371294e14, 2.807600e15, 5.100000e12],
        rtol=TEST_RTOL,
    )


@skip
def test_vmrdms_ams_subset(data_vmrdms_ams_cvo):
    stat = data_vmrdms_ams_cvo.to_station_data(meta_idx=0, start=2000, stop=2008, freq="monthly")

    assert_array_equal(
        [str(stat.dtime.min()), str(stat.dtime.max())],
        ["2000-01-15T00:00:00.000000000", "2007-12-15T00:00:00.000000000"],
    )
    assert stat.ts_type == "monthly"
    assert stat.ts_type_src == "daily"
