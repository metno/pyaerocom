from __future__ import annotations

from pathlib import Path

import pytest
import numpy as np

from pyaerocom.io.read_eprofile import ReadEprofile
from pyaerocom import const, VerticalProfile, UngriddedData

from tests.conftest import lustre_unavail


ROOT: str = const.OBSLOCS_UNGRIDDED["Eprofile-test"]

TEST_FILES: list[str] = [
    f"{ROOT}/AP_0-20000-0-06235-A-2025-01-01.nc",
    f"{ROOT}/AP_0-20000-0-06240-A-2025-01-01.nc",
]


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@lustre_unavail
def test_ReadEprofile_get_file_list():
    reader = ReadEprofile()
    files = reader.get_file_list()
    assert isinstance(files, list)


@pytest.mark.parametrize(
    "num,vars_to_retrieve",
    [
        (0, "bsc1064aer"),
    ],
)
def test_ReadEprofile_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEprofile()
    read.files = paths = TEST_FILES
    stat = read.read_file(paths[num], vars_to_retrieve)

    assert "data_level" in stat
    assert "wavelength_emis" in stat
    assert "station_coords" in stat

    assert vars_to_retrieve in stat.var_info
    assert stat.var_info[vars_to_retrieve]["unit_ok"]
    assert not stat.var_info[vars_to_retrieve]["err_read"]
    assert stat.var_info[vars_to_retrieve]["outliers_removed"]

    bsc1064aer = stat.bsc1064aer
    assert isinstance(bsc1064aer, VerticalProfile)
    assert len(bsc1064aer.data) > 0
    assert isinstance(np.min(bsc1064aer.altitude), float)
    assert isinstance(np.max(bsc1064aer.altitude), float)


def test_ReadEprofile_read_file_error():
    read = ReadEprofile()
    read.files = paths = TEST_FILES
    with pytest.raises(ValueError) as e:
        read.read_file(paths[0], "invalidvar")
    assert str(e.value).endswith("is not supported")


def test_ReadEprofile_read():
    read = ReadEprofile()
    read.files = TEST_FILES
    data = read.read(vars_to_retrieve="bsc1064aer")
    assert isinstance(data, UngriddedData)
    assert len(data.metadata) == len(TEST_FILES)
    assert len(data.shape) == 2
