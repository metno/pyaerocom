from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from pyaerocom import const, VerticalProfile
from pyaerocom.io.evdc_ozone_sonde.reader import ReadEvdcOzoneSondeData

ROOT: str = const.OBSLOCS_UNGRIDDED["EVDC-HARP-test"]

TEST_FILES: list[str | Path] = [
    Path(
        f"{ROOT}/2019/08/07/evdc-sonde_o3-mch-000-consolidated-payerne-20190807T110000-20190807T123713-003-20200907T191640.nc"
    ),
    Path(
        f"{ROOT}/2019/08/21/evdc-sonde_o3-dwd-000-hohenpeissenberg-20190821T044901-20190821T062921-003-20191023T135711.nc"
    ),
]

SIMPLE_TEST_VAR = "conco33D"
TEST_RTOL = 1.0e-4


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "num,vars_to_retrieve",
    [
        (1, SIMPLE_TEST_VAR),
    ],
)
def test_Evdc_harp_read_file(num: int, vars_to_retrieve: list[str]):
    read = ReadEvdcOzoneSondeData()
    read.files = paths = TEST_FILES
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
    #
    # assert np.nanmean(stat[SIMPLE_TEST_VAR].data_err) == pytest.approx(0.003919774151078758, rel=TEST_RTOL)
    # assert np.nanstd(stat[SIMPLE_TEST_VAR].data_err) == pytest.approx(0.0020847733483625517, rel=TEST_RTOL)
    #
    assert np.min(stat[SIMPLE_TEST_VAR].altitude) <= 1000
    assert np.max(stat[SIMPLE_TEST_VAR].altitude) >= 5000


# def test_ReadEarlinet_read():
#     read = ReadEarlinet()
#     read.files = TEST_FILES
#     data = read.read(vars_to_retrieve="ec355aer")
#
#     assert len(data.metadata) == 1
#     assert data.shape == (164, 12)
#
#     assert np.nanmin(data._data[:, data._DATAINDEX]) == pytest.approx(
#         -0.002188435098876817, rel=TEST_RTOL
#     )
#     assert np.nanmean(data._data[:, data._DATAINDEX]) == pytest.approx(
#         0.02495260001522142, rel=TEST_RTOL
#     )
#     assert np.nanmax(data._data[:, data._DATAINDEX]) == pytest.approx(
#         0.16084047083963124, rel=TEST_RTOL
#     )
#
#     merged = data.to_station_data(0)
#     # same values as above because only one meta_idx
#     assert np.nanmin(merged.ec355aer) == pytest.approx(-0.002188435098876817, rel=TEST_RTOL)
#     assert np.nanmean(merged.ec355aer) == pytest.approx(0.02495260001522142, rel=TEST_RTOL)
#     assert np.nanmax(merged.ec355aer) == pytest.approx(0.16084047083963124, rel=TEST_RTOL)
#
#
# @pytest.mark.parametrize(
#     "vars_to_retrieve,pattern,num",
#     [
#         (None, None, 1),
#         (["ec355aer"], None, 1),
#         (["bsc355aer"], None, 0),
#         (["bsc532aer"], None, 1),
#     ],
# )
# def test_ReadEarlinet_get_file_list(
#         vars_to_retrieve: list[str] | None, pattern: str | None, num: int
# ):
#     reader = ReadEarlinet("Earlinet-test")
#     files = reader.get_file_list(vars_to_retrieve, pattern)
#     assert len(files) == num
#
#
# def test_ReadEarlinet_get_file_list_error():
#     reader = ReadEarlinet("Earlinet-test")
#     with pytest.raises(NotImplementedError) as e:
#         reader.get_file_list(pattern="*e.v*")
#     assert str(e.value) == "filetype delimiter . not supported"
#
#
# def test_ReadEarlinet__get_exclude_filelist():
#     reader = ReadEarlinet("Earlinet-test")
#     reader.EXCLUDE_CASES.append("onefile.txt")
#     files = reader.get_file_list(reader.PROVIDES_VARIABLES)
#     assert len(files) == 1
