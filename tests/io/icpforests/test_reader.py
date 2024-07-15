from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.io.icpforests.metadata import MetadataReader as ReadICPForestMeta
from pyaerocom.io.icpforests.reader import ReadICPForest
from tests.fixtures.data_access import TEST_DATA, DataForTests

# station names are not consistent between variables!
# Station names are kind of limited since we took only the last 5000 lines from the data file for the test data set
STATION_NAMES = ("BG-1-1", "LV-15-2", "BG-4-3")

VARS_DEFAULT = {"wetoxn"}
VARS_PROVIDED = VARS_DEFAULT

ICP_PATH = DataForTests(TEST_DATA["ICPFORESTS.Subset"].relpath).path


@pytest.fixture(scope="module")
def reader():
    return ReadICPForest("ICPFORESTS.Subset")


@pytest.fixture(scope="module")
def meta_reader() -> ReadICPForestMeta:
    return ReadICPForestMeta(str(ICP_PATH))


@pytest.fixture()
def station_files(station: str) -> list[Path]:
    p = ICP_PATH.glob("dp_dem.csv")
    files = [x for x in p if x.is_file()]
    # assert files, f"no files for {station}"
    assert files
    return files


def test_DATASET_NAME(reader: ReadICPForest):
    assert reader.DATA_ID == const.ICPFORESTS_NAME


def test_DEFAULT_VARS(reader: ReadICPForest):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


def test_METADATA(meta_reader: ReadICPForestMeta):
    assert len(meta_reader.deposition_type) >= 3, "found less deposition types than expected"


def test_PROVIDES_VARIABLES(reader: ReadICPForest):
    assert set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


def test_read_file(
    reader: ReadICPForest,
):
    data = reader.read(vars_to_retrieve=VARS_DEFAULT)
    assert set(data.contains_vars) == VARS_DEFAULT


def test_read_station(
    reader: ReadICPForest,
):
    data = reader.read(
        vars_to_retrieve=VARS_DEFAULT,
    )
    for station in STATION_NAMES:
        assert station in data.unique_station_names


def test_reader_gives_correct_ICP_PATH(reader: ReadICPForest):
    assert str(ICP_PATH) == reader.data_dir
