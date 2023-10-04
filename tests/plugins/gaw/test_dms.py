import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from pyaerocom.plugins.gaw.reader import ReadGAW
from tests.conftest import TEST_RTOL, lustre_unavail


def _make_data():
    r = ReadGAW()
    return r.read("vmrdms")


@pytest.fixture(scope="module")
@lustre_unavail
def data_vmrdms_ams_cvo():
    return _make_data()


@lustre_unavail
@pytest.mark.xfail(reason="wrong data.shape")
def test_ungriddeddata_ams_cvo(data_vmrdms_ams_cvo):
    data = data_vmrdms_ams_cvo
    # assert data.data_revision['DMS_AMS_CVO'] == 'n/a'
    assert data.shape == (819 + 7977, 12)
    assert len(data.metadata) == 2

    unique_coords = []
    unique_coords.extend(np.unique(data.latitude))
    unique_coords.extend(np.unique(data.longitude))
    unique_coords.extend(np.unique(data.altitude))
    assert len(unique_coords) == 6
    assert_allclose(unique_coords, [-37.8, 16.848, -24.871, 77.53, 10.0, 65.0], rtol=TEST_RTOL)

    vals = data._data[:, data.index["data"]]
    assert_allclose(
        [vals.nanmean(), vals.nanstd(), vals.nanmax(), vals.nanmin],
        [174.8499921813917, 233.0328306938496, 2807.6, 0.0],
        rtol=TEST_RTOL,
    )


@lustre_unavail
@pytest.mark.xfail(reason='stat["vmrdms"] are 1e12 off')
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
        [185.6800736155262, 237.1293922258991, 2807.6, 5.1],
        rtol=TEST_RTOL,
    )


@lustre_unavail
def test_vmrdms_ams_subset(data_vmrdms_ams_cvo):
    stat = data_vmrdms_ams_cvo.to_station_data(meta_idx=0, start=2000, stop=2008, freq="monthly")

    assert_array_equal(
        [str(stat.dtime.min()), str(stat.dtime.max())],
        ["2000-01-15T00:00:00.000000000", "2007-12-15T00:00:00.000000000"],
    )
    assert stat.ts_type == "monthly"
    assert stat.ts_type_src == "daily"
