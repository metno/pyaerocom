from __future__ import annotations

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
    "num,vars_to_retrieve",
    [
        (0, "ec532aer"),
        (0, ["ec532aer", "zdust"]),
        (0, ReadEarlinet.PROVIDES_VARIABLES),
        (1, ReadEarlinet.PROVIDES_VARIABLES),
        (2, ReadEarlinet.PROVIDES_VARIABLES),
        (3, ReadEarlinet.PROVIDES_VARIABLES),
        (4, ReadEarlinet.PROVIDES_VARIABLES),
        (5, ReadEarlinet.PROVIDES_VARIABLES),
    ],
)
def test_ReadEarlinet_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEarlinet()
    read.files = paths = TEST_FILES
    stat = read.read_file(paths[num], vars_to_retrieve)

    assert "data_level" in stat
    assert "wavelength_det" in stat
    assert "has_zdust" in stat
    assert "eval_method" in stat

    if num != 0:
        return

    assert "ec532aer" in stat.var_info
    assert stat.var_info["ec532aer"]["unit_ok"]
    assert stat.var_info["ec532aer"]["err_read"]
    assert stat.var_info["ec532aer"]["outliers_removed"]

    ec532aer = stat.ec532aer
    assert isinstance(ec532aer, VerticalProfile)
    assert len(ec532aer.data) == 253
    assert np.sum(np.isnan(ec532aer.data)) == 216

    assert_allclose(np.nanmean(ec532aer.data), 4.463068618148296, rtol=TEST_RTOL)
    assert_allclose(np.nanstd(ec532aer.data), 1.8529271228530515, rtol=TEST_RTOL)

    assert_allclose(np.nanmean(ec532aer.data_err), 4.49097234883772, rtol=TEST_RTOL)
    assert_allclose(np.nanstd(ec532aer.data_err), 0.8332285038985179, rtol=TEST_RTOL)

    assert_allclose(np.min(ec532aer.altitude), 331.29290771484375, rtol=TEST_RTOL)
    assert_allclose(np.max(ec532aer.altitude), 7862.52490234375, rtol=TEST_RTOL)


@pytest.mark.parametrize(
    "vars_to_retrieve,error",
    [
        ("invalidvar", "invalidvar is not supported"),
        ("od550aer", "od550aer is not supported"),
    ],
)
def test_ReadEarlinet_read_file_error(vars_to_retrieve: str, error: str):
    read = ReadEarlinet()
    read.files = paths = TEST_FILES
    with pytest.raises(ValueError) as e:
        read.read_file(paths[0], vars_to_retrieve)
    assert str(e.value) == error


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

    assert_allclose(np.nanmin(merged.ec532aer), 0.220322, rtol=TEST_RTOL)
    assert_allclose(np.nanmean(merged.ec532aer), 23.093238, rtol=TEST_RTOL)
    assert_allclose(np.nanmax(merged.ec532aer), 111.478665, rtol=TEST_RTOL)


@pytest.mark.parametrize(
    "vars_to_retrieve,pattern,num",
    [
        (None, None, 5),
        (["ec355aer"], None, 1),
        (["zdust"], None, 6),
        (["bsc355aer"], None, 0),
        (["bsc532aer"], None, 0),
        (None, "*ev*", 5),
        (None, "*xy*", 0),
    ],
)
def test_ReadEarlinet_get_file_list(
    vars_to_retrieve: list[str] | None, pattern: str | None, num: int
):
    reader = ReadEarlinet("Earlinet-test")
    files = reader.get_file_list(vars_to_retrieve, pattern)
    assert len(files) == num


def test_ReadEarlinet_get_file_list_error():
    reader = ReadEarlinet("Earlinet-test")
    with pytest.raises(NotImplementedError) as e:
        reader.get_file_list(pattern="*e.v*")
    assert str(e.value) == "filetype delimiter . not supported"


def test_ReadEarlinet__get_exclude_filelist():
    reader = ReadEarlinet("Earlinet-test")
    reader.EXCLUDE_CASES.append("onefile.txt")
    files = reader.get_file_list(reader.PROVIDES_VARIABLES)
    assert len(files) == 5
