from __future__ import annotations

from contextlib import nullcontext as does_not_raise_exception
from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_allclose

from pyaerocom import VerticalProfile, const
from pyaerocom.io.read_earlinet import ReadEarlinet

from ..conftest import TEST_RTOL

ROOT: str = const.OBSLOCS_UNGRIDDED["Earlinet-test"]
TEST_FILES: list[str] = [
    f"{ROOT}/ev/ev1008192050.e532",
    f"{ROOT}/ev/ev1009162031.e532",
    f"{ROOT}/ev/ev1012131839.e532",
    f"{ROOT}/ev/ev1011221924.e532",
    f"{ROOT}/ev/ev1105122027.e532",
    f"{ROOT}/ms/ms1005242029.e355",
]


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "fnum,vars_to_retrieve,raises",
    [
        (0, "ec532aer", does_not_raise_exception()),
        (0, "invalidvar", pytest.raises(ValueError)),
        (0, "od550aer", pytest.raises(ValueError)),
        (0, ["ec532aer", "zdust"], does_not_raise_exception()),
        (0, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
        (1, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
        (2, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
        (3, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
        (4, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
        (5, ReadEarlinet.PROVIDES_VARIABLES, does_not_raise_exception()),
    ],
)
def test_ReadEarlinet_read_file(fnum, vars_to_retrieve, raises):
    read = ReadEarlinet()
    paths = TEST_FILES
    read.files = paths
    fname = paths[fnum]
    with raises:
        stat = read.read_file(fname, vars_to_retrieve)
        if fnum == 0:
            assert "data_level" in stat
            assert "wavelength_det" in stat
            assert "has_zdust" in stat
            assert "eval_method" in stat

            assert "ec532aer" in stat.var_info

            i = stat.var_info["ec532aer"]
            assert i["unit_ok"]
            assert i["err_read"]
            assert i["outliers_removed"]

            assert isinstance(stat.ec532aer, VerticalProfile)

            p = stat.ec532aer

            vals_data = [
                np.nanmean(p.data),
                np.nanstd(p.data),
                np.sum(np.isnan(p.data)),
                len(p.data),
            ]
            vals_dataerr = [np.nanmean(p.data_err), np.nanstd(p.data_err)]
            vals_altitude = [np.min(p.altitude), np.max(p.altitude)]

            assert_allclose(
                vals_data, [4.463068618148296, 1.8529271228530515, 216, 253], rtol=TEST_RTOL
            )
            assert_allclose(vals_dataerr, [4.49097234883772, 0.8332285038985179], rtol=TEST_RTOL)
            assert_allclose(vals_altitude, [331.29290771484375, 7862.52490234375], rtol=TEST_RTOL)


def test_ReadEarlinet_read():
    read = ReadEarlinet()
    read.files = TEST_FILES
    data = read.read(vars_to_retrieve="ec532aer")

    assert len(data.metadata) == 5
    assert data.shape == (786, 12)

    assert_allclose(np.nanmin(data._data[:, data._DATAINDEX]), -0.440742, rtol=TEST_RTOL)
    assert_allclose(np.nanmean(data._data[:, data._DATAINDEX]), 24.793547, rtol=TEST_RTOL)
    assert_allclose(np.nanmax(data._data[:, data._DATAINDEX]), 167.90787, rtol=TEST_RTOL)

    merged = data.to_station_data("Evora", freq="monthly")

    assert_allclose(float(np.nanmin(merged.ec532aer)), 0.220322, rtol=TEST_RTOL)
    assert_allclose(float(np.nanmean(merged.ec532aer)), 23.093238, rtol=TEST_RTOL)
    assert_allclose(float(np.nanmax(merged.ec532aer)), 111.478665, rtol=TEST_RTOL)


@pytest.mark.parametrize(
    "vars_to_retrieve,pattern,fnum,raises",
    [
        (None, None, 5, does_not_raise_exception()),
        (["ec355aer"], None, 1, does_not_raise_exception()),
        (["zdust"], None, 6, does_not_raise_exception()),
        (["bsc355aer"], None, 0, does_not_raise_exception()),
        (["bsc532aer"], None, 0, does_not_raise_exception()),
        (None, "*ev*", 5, does_not_raise_exception()),
        (None, "*xy*", 0, does_not_raise_exception()),
        (None, "*e.v*", 0, pytest.raises(NotImplementedError)),
    ],
)
def test_ReadEarlinet_get_file_list(vars_to_retrieve, pattern, fnum, raises):
    reader = ReadEarlinet("Earlinet-test")
    with raises:
        files = reader.get_file_list(vars_to_retrieve, pattern)
        assert len(files) == fnum


def test_ReadEarlinet__get_exclude_filelist():
    reader = ReadEarlinet("Earlinet-test")
    reader.EXCLUDE_CASES.append("onefile.txt")
    files = reader.get_file_list(reader.PROVIDES_VARIABLES)
    assert len(files) == 5
