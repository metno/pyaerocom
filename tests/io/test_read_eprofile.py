from __future__ import annotations

from pathlib import Path

import pytest
import numpy as np

from pyaerocom.io.read_eprofile import ReadEprofile
from pyaerocom import VerticalProfile
from tests.conftest import TEST_RTOL


TEST_FILES: list[str] = [
    "/lustre/storeB/project/fou/kl/v-profiles/2025/01/01/AP_0-20000-0-06235-A-2025-01-01.nc",
    "/lustre/storeB/project/fou/kl/v-profiles/2025/01/01/AP_0-20000-0-06240-A-2025-01-01.nc",
]


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "vars_to_retrieve",
    [
        (["ec1064aer"], 2),
    ],
)
def test_ReadEprofile_get_file_list(vars_to_retrieve: list[str] | None):
    reader = ReadEprofile()
    files = reader.get_file_list()
    assert len(files) > 0


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
    assert len(bsc1064aer.data) == 288
    assert np.sum(np.isnan(bsc1064aer.data)) == 0
    assert np.nanmean(bsc1064aer.data) == pytest.approx(0.0011734896433714444, rel=TEST_RTOL)
    assert np.nanstd(bsc1064aer.data) == pytest.approx(0.005380064098560619, rel=TEST_RTOL)
    assert np.min(bsc1064aer.altitude) == pytest.approx(10.989999771118164, rel=TEST_RTOL)
    assert np.max(bsc1064aer.altitude) == pytest.approx(15340.989999771118, rel=TEST_RTOL)


def test_ReadEprofile_read():
    read = ReadEprofile()
    read.files = TEST_FILES
    data = read.read(vars_to_retrieve="bsc1064aer")

    assert len(data.metadata) == 1
