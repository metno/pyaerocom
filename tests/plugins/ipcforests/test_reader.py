from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.ipcforests.reader import ReadIPCForest
from tests.conftest import lustre_unavail

try:
    IPC_PATH = Path(const.OBSLOCS_UNGRIDDED[const.IPCFORESTS_NAME])
except KeyError:
    pytest.mark.skip(reason=f"IPCForests path not initialised due to non existence in CI")

# stationnames are not consistent between variables!
# wetoxn
STATION_NAMES = ("DE-604-2", "NO-7-2", "UK-718-2")
# fakedrypm10
# STATION_NAMES = ("Birkenes II", "La Coulonche", "Jarczew")

VARS_DEFAULT = {"wetoxn"}
VARS_PROVIDED = VARS_DEFAULT


@lustre_unavail
@pytest.fixture(scope="module")
def reader() -> ReadIPCForest:
    return ReadIPCForest(data_dir=str(IPC_PATH))


@lustre_unavail
@pytest.fixture()
def station_files(station: str) -> list[Path]:
    p = IPC_PATH.glob("dp_dem.csv")
    files = [x for x in p if x.is_file()]
    # assert files, f"no files for {station}"
    assert files
    return files


@lustre_unavail
def test_DATASET_NAME(reader: ReadIPCForest):
    assert reader.DATA_ID == const.IPCFORESTS_NAME


@lustre_unavail
def test_DEFAULT_VARS(reader: ReadIPCForest):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


# @lustre_unavail
# def test_FOUND_FILES(reader: ReadIPCForest):
#     assert reader.FOUND_FILES, "no stations files found"
#     assert len(reader.FOUND_FILES) >= 3, "found less files than expected"


# @lustre_unavail
# @pytest.mark.parametrize("station", STATION_NAMES)
# def test_stations(reader: ReadIPCForest, station: str):
#     assert reader.stations()[station], f"no {station} station files"


@lustre_unavail
def test_PROVIDES_VARIABLES(reader: ReadIPCForest):
    return set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@lustre_unavail
# @pytest.mark.parametrize("station", STATION_NAMES)
def test_read_file(
    reader: ReadIPCForest,
):
    data = reader.read(vars_to_retrieve=VARS_DEFAULT)
    assert set(data.contains_vars) == VARS_DEFAULT


# @lustre_unavail
# @pytest.mark.parametrize("station", STATION_NAMES)
# def test_read(reader: ReadIPCForest, station_files: list[str]):
#     data = reader.read(VARS_PROVIDED, station_files, first_file=0, last_file=5)
#     assert set(data.contains_vars) == VARS_PROVIDED


@lustre_unavail
def test_reader_gives_correct_IPC_PATH(reader: ReadIPCForest):
    assert str(IPC_PATH) == reader.data_dir
