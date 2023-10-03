from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from pyaerocom import VerticalProfile, const
from pyaerocom.io.read_earlinet import ReadEarlinet
from tests.conftest import TEST_RTOL

ROOT: str = const.OBSLOCS_UNGRIDDED["Earlinet-test"]

TEST_FILES: list[str] = [
    f"{ROOT}/EARLINET_AerRemSen_cyc_Lev02_e0355_202104262030_202104262130_v01_qc03.nc",
    f"{ROOT}/EARLINET_AerRemSen_waw_Lev02_b0532_202109221030_202109221130_v01_qc03.nc",
]


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "num,vars_to_retrieve",
    [
        (0, "ec355aer"),
    ],
)
def test_ReadEarlinet_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEarlinet()
    read.files = paths = TEST_FILES
    stat = read.read_file(paths[num], vars_to_retrieve)

    assert "data_level" in stat
    assert "wavelength_emis" in stat
    assert "has_zdust" in stat
    assert "location" in stat

    if num != 0:
        return

    assert "ec355aer" in stat.var_info
    assert stat.var_info["ec355aer"]["unit_ok"]
    assert stat.var_info["ec355aer"]["err_read"]
    assert stat.var_info["ec355aer"]["outliers_removed"]

    ec355aer = stat.ec355aer
    assert isinstance(ec355aer, VerticalProfile)
    assert len(ec355aer.data) == 164
    assert np.sum(np.isnan(ec355aer.data)) == 0

    assert np.nanmean(ec355aer.data) == pytest.approx(0.02495260001522142, rel=TEST_RTOL)
    assert np.nanstd(ec355aer.data) == pytest.approx(0.03295176956505217, rel=TEST_RTOL)

    assert np.nanmean(ec355aer.data_err) == pytest.approx(0.003919774151078758, rel=TEST_RTOL)
    assert np.nanstd(ec355aer.data_err) == pytest.approx(0.0020847733483625517, rel=TEST_RTOL)

    assert np.min(ec355aer.altitude) == pytest.approx(935.4610692253234, rel=TEST_RTOL)
    assert np.max(ec355aer.altitude) == pytest.approx(10678.245216562595, rel=TEST_RTOL)


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
    data = read.read(vars_to_retrieve="ec355aer")

    assert len(data.metadata) == 1
    assert data.shape == (164, 12)

    assert np.nanmin(data._data[:, data._DATAINDEX]) == pytest.approx(
        -0.002188435098876817, rel=TEST_RTOL
    )
    assert np.nanmean(data._data[:, data._DATAINDEX]) == pytest.approx(
        0.02495260001522142, rel=TEST_RTOL
    )
    assert np.nanmax(data._data[:, data._DATAINDEX]) == pytest.approx(
        0.16084047083963124, rel=TEST_RTOL
    )

    merged = data.to_station_data(0)
    # same values as above because only one meta_idx
    assert np.nanmin(merged.ec355aer) == pytest.approx(-0.002188435098876817, rel=TEST_RTOL)
    assert np.nanmean(merged.ec355aer) == pytest.approx(0.02495260001522142, rel=TEST_RTOL)
    assert np.nanmax(merged.ec355aer) == pytest.approx(0.16084047083963124, rel=TEST_RTOL)


@pytest.mark.parametrize(
    "vars_to_retrieve,pattern,num",
    [
        (None, None, 1),
        (["ec355aer"], None, 1),
        (["bsc355aer"], None, 0),
        (["bsc532aer"], None, 1),
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
    assert len(files) == 1
