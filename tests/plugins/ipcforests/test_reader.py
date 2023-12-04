from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.ipcforests.metadata import MetadataReader as ReadIPCForestMeta
from pyaerocom.plugins.ipcforests.reader import ReadIPCForest
from tests.fixtures.data_access import TEST_DATA, DataForTests

# station names are not consistent between variables!
# Station names are kind of limited since we took only the last 5000 lines from the data file for the test data set
STATION_NAMES = ("BG-1-1", "LV-15-2", "BG-4-3")

VARS_DEFAULT = {"wetoxn"}
VARS_PROVIDED = VARS_DEFAULT

IPC_PATH = DataForTests(TEST_DATA["IPCFORESTS.Subset"].relpath).path


@pytest.fixture(scope="module")
def reader():
    return ReadIPCForest("IPCFORESTS.Subset")


@pytest.fixture(scope="module")
def meta_reader() -> ReadIPCForestMeta:
    return ReadIPCForestMeta(str(IPC_PATH))


@pytest.fixture()
def station_files(station: str) -> list[Path]:
    p = IPC_PATH.glob("dp_dem.csv")
    files = [x for x in p if x.is_file()]
    # assert files, f"no files for {station}"
    assert files
    return files


def test_DATASET_NAME(reader: ReadIPCForest):
    assert reader.DATA_ID == const.IPCFORESTS_NAME


def test_DEFAULT_VARS(reader: ReadIPCForest):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


def test_METADATA(meta_reader: ReadIPCForestMeta):
    assert len(meta_reader.deposition_type) >= 3, "found less deposition types than expected"


def test_PROVIDES_VARIABLES(reader: ReadIPCForest):
    return set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


def test_read_file(
    reader: ReadIPCForest,
):
    data = reader.read(vars_to_retrieve=VARS_DEFAULT)
    assert set(data.contains_vars) == VARS_DEFAULT


def test_read_station(
    reader: ReadIPCForest,
):
    data = reader.read(
        vars_to_retrieve=VARS_DEFAULT,
    )
    for station in STATION_NAMES:
        assert station in data.unique_station_names


def test_reader_gives_correct_IPC_PATH(reader: ReadIPCForest):
    assert str(IPC_PATH) == reader.data_dir
