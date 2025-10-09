from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pytest

from pyaerocom import const, VerticalProfile
from pyaerocom.io.evdc_ozone_sonde.reader import (
    ReadEvdcOzoneSondeDataHdf,
    ReadEvdcOzoneSondeDataHarp,
)

ROOT_HARP: Path = Path(const.OBSLOCS_UNGRIDDED["EVDC-HARP-test"])
ROOT_HDF: Path = Path(const.OBSLOCS_UNGRIDDED["EVDC-HDF-test"])

TEST_FILES_HARP: list[str | Path] = [
    Path(
        f"{ROOT_HARP}/2019/08/07/evdc-sonde_o3-mch-000-consolidated-payerne-20190807T110000-20190807T123713-003-20200907T191640.nc"
    ),
    Path(
        f"{ROOT_HARP}/2019/08/21/evdc-sonde_o3-dwd-000-hohenpeissenberg-20190821T044901-20190821T062921-003-20191023T135711.nc"
    ),
]

TEST_FILES_HDF: list[str | Path] = [
    Path(
        f"{ROOT_HDF}/balloon_sonde.o3_dwd000_hohenpeissenberg_20190311t060600z_20190311t074200z_003.h5"
    ),
    Path(
        f"{ROOT_HDF}/balloon_sonde.o3_awi001_ny.alesund_20061230t105000z_20061230t122220z_001.hdf"
    ),
]

SIMPLE_TEST_VAR = "conco33d"
TEST_VAR_HDF = "vmro33d"  # this is what all files provide
TEST_RTOL = 1.0e-4

logger = logging.getLogger(__name__)


def test_all_files_exist():
    for file in TEST_FILES_HARP:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "num,vars_to_retrieve",
    [
        (1, SIMPLE_TEST_VAR),
    ],
)
def test_Evdc_harp_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEvdcOzoneSondeDataHarp()
    read.files = paths = TEST_FILES_HARP
    stat = read.read_file(paths[num], vars_to_retrieve)

    if num != 0:
        return

    assert SIMPLE_TEST_VAR in stat.var_info
    assert stat.var_info[SIMPLE_TEST_VAR]["unit_ok"]
    assert "err_read" in stat.var_info[SIMPLE_TEST_VAR]
    assert "outliers_removed" in stat.var_info[SIMPLE_TEST_VAR]

    assert isinstance(stat[SIMPLE_TEST_VAR], VerticalProfile)
    assert len(stat[SIMPLE_TEST_VAR].data) > 1000
    assert np.sum(np.isnan(stat[SIMPLE_TEST_VAR].data)) == 0
    #
    assert np.nanmean(stat[SIMPLE_TEST_VAR].data) == pytest.approx(
        2.3126154036210864, rel=TEST_RTOL
    )
    assert np.min(stat[SIMPLE_TEST_VAR].altitude) <= 1000
    assert np.max(stat[SIMPLE_TEST_VAR].altitude) >= 5000


@pytest.mark.parametrize(
    "num,vars_to_retrieve",
    [
        (0, SIMPLE_TEST_VAR),
    ],
)
def test_Evdc_hdf_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEvdcOzoneSondeDataHdf()
    read.files = paths = TEST_FILES_HDF
    stat = read.read_file(paths[num], vars_to_retrieve)

    if num != 0:
        return

    assert SIMPLE_TEST_VAR in stat.var_info
    assert stat.var_info[SIMPLE_TEST_VAR]["unit_ok"]
    assert "err_read" in stat.var_info[SIMPLE_TEST_VAR]
    assert "outliers_removed" in stat.var_info[SIMPLE_TEST_VAR]

    assert isinstance(stat[SIMPLE_TEST_VAR], VerticalProfile)
    assert len(stat[SIMPLE_TEST_VAR].data) > 500
    assert np.nanmean(stat[SIMPLE_TEST_VAR].data) == pytest.approx(
        2.431399685597938, rel=TEST_RTOL
    )
    assert np.min(stat[SIMPLE_TEST_VAR].altitude) <= 1000
    assert np.max(stat[SIMPLE_TEST_VAR].altitude) >= 5000


def test_get_file_list_harp():
    # test the getfiles method
    read = ReadEvdcOzoneSondeDataHarp(data_dir=ROOT_HARP)
    read.files = read.get_file_list()
    assert len(read.files) >= len(TEST_FILES_HARP)


def test_get_file_list_hdf():
    # test the getfiles method
    read = ReadEvdcOzoneSondeDataHdf(
        data_dir=ROOT_HDF,
    )
    read.files = read.get_file_list()
    # assert len(read.files) >= len(TEST_FILES_HDF)
    # we look foo h5 files only and omit hdf files for the moment
    assert len(read.files) >= 0


def test_EvdcOzoneSondeData_read_hdf():
    read = ReadEvdcOzoneSondeDataHdf(
        data_dir=ROOT_HDF,
    )
    data = read.read(vars_to_retrieve=TEST_VAR_HDF)
    #
    assert len(data.metadata) >= 1


def test_EvdcOzoneSondeData_read_harp():
    read = ReadEvdcOzoneSondeDataHarp(data_dir=ROOT_HARP)
    #     read.files = TEST_FILES_HARP
    data = read.read(vars_to_retrieve=SIMPLE_TEST_VAR)
    #
    assert len(data.metadata) > 1
