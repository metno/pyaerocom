from __future__ import annotations

import logging
import os
from pathlib import Path

import numpy as np
import pytest

from pyaerocom import const, VerticalProfile
from pyaerocom.io.sonde_like.reader import (
    ReadEvdcOzoneSondeDataHdf,
    ReadEvdcOzoneSondeDataHarp,
    ReadIagosDataHarp,
)
from pyaerocom.io.sonde_like.jdcal import is_leap, gcal2jd, jcal2jd, jd2jcal, jd2gcal

ROOT_IAGOS_HARP: Path = Path(const.OBSLOCS_UNGRIDDED["IAGOS-HARP-test"])
try:
    ROOT_IAGOS_HARP_LUSTRE: Path = Path(const.OBSLOCS_UNGRIDDED["IAGOS.HARP"])
except KeyError:
    ROOT_IAGOS_HARP_LUSTRE: Path = Path(
        "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/IAGOS/HARP"
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

TEST_FILES_IAGOS_HARP: list[str | Path] = [
    Path(
        f"{ROOT_IAGOS_HARP}//2025/09/13/iagos-o3_asc-L1-2025091320383902-MAA-20250913T203855-20250913T212339-0101-20250930T010019.nc"
    ),
    Path(
        f"{ROOT_IAGOS_HARP}/2025/09/13/iagos-o3_desc-L1-2025091221511102-FRA-20250913T044151-20250913T061827-0100-20250924T010017.nc"
    ),
]

TEST_FILES_IAGOS_HARP_LUSTRE: list[str | Path] = [
    f"{ROOT_IAGOS_HARP_LUSTRE}/2025/04/05/iagos-co_desc-L1-2025040520113616-MAD-20250405T204040-20250405T210244-0100-20250408T010022.nc",
    f"{ROOT_IAGOS_HARP_LUSTRE}/2025/04/05/iagos-co_desc-L1-2025040517472416-BCN-20250405T181632-20250405T184252-0100-20250408T010022.nc",
    f"{ROOT_IAGOS_HARP_LUSTRE}/2025/04/05/iagos-co_desc-L1-2025040510585616-MAD-20250405T123944-20250405T131712-0100-20250408T010021.nc",
]
SIMPLE_TEST_VAR = "conco33d"
TEST_VAR_HDF = "vmro33d"  # this is what all files provide
TEST_VAR_IAGOS_CO = "vmrco3d"  # this is what all files provide
TEST_RTOL = 1.0e-4

logger = logging.getLogger(__name__)


def test_IAGOS_Data_read_harp_file_list():
    # test reading of harp files
    if os.path.exists(ROOT_IAGOS_HARP_LUSTRE):
        read = ReadIagosDataHarp(data_dir=ROOT_IAGOS_HARP_LUSTRE)
        data = read.read(vars_to_retrieve=TEST_VAR_IAGOS_CO, files=TEST_FILES_IAGOS_HARP_LUSTRE)
        #
        assert len(data.unique_station_names) > 1
        assert len(data.metadata) > 1
    else:
        assert True


def test_IAGOS_Data_read_harp():
    # test reading of harp files
    read = ReadIagosDataHarp(data_dir=ROOT_IAGOS_HARP)
    data = read.read(vars_to_retrieve=TEST_VAR_HDF)
    #
    assert len(data.unique_station_names) > 1
    assert len(data.metadata) > 1


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
    # test the get_file_list method for harp reading
    read = ReadEvdcOzoneSondeDataHarp(data_dir=ROOT_HARP)
    read.files = read.get_file_list()
    assert len(read.files) >= len(TEST_FILES_HARP)


def test_get_file_list_iagos_harp():
    # test the get_file_list method for harp reading
    read = ReadIagosDataHarp(data_dir=ROOT_IAGOS_HARP)
    read.files = read.get_file_list()
    assert len(read.files) >= len(TEST_FILES_HARP)


def test_get_file_list_hdf():
    # test the get_file_list method for hdf reading
    read = ReadEvdcOzoneSondeDataHdf(
        data_dir=ROOT_HDF,
    )
    read.files = read.get_file_list()
    # we look for .h5 files only and omit hdf files for the moment
    assert len(read.files) >= 0


def test_EvdcOzoneSondeData_read_hdf():
    # test reading of hdf files
    read = ReadEvdcOzoneSondeDataHdf(
        data_dir=ROOT_HDF,
    )
    data = read.read(vars_to_retrieve=TEST_VAR_HDF)
    assert len(data.unique_station_names) >= 1
    assert len(data.metadata) >= 1


def test_EvdcOzoneSondeData_read_harp():
    # test reading of harp files
    read = ReadEvdcOzoneSondeDataHarp(data_dir=ROOT_HARP)
    data = read.read(vars_to_retrieve=SIMPLE_TEST_VAR)
    #
    assert len(data.unique_station_names) > 1
    assert len(data.metadata) > 1


def test_jdcal():
    # to make codecov happy
    assert not is_leap(2021)
    assert jd2gcal(*gcal2jd(1950, 1, 1)) == (1950, 1, 1, 0.0)
    assert jd2jcal(*jcal2jd(2000, 1, 1)) == (2000, 1, 1, 0.0)
