from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.io.icos.reader import ReadICOS

if not const.has_access_lustre:
    pytestmark = pytest.skip(
        reason="Skipping tests that require access to AEROCOM database on METNo servers",
        allow_module_level=True,
    )

VARS_DEFAULT = {"vmrco2", "vmrch4", "vmrco"}
VARS_PROVIDED = VARS_DEFAULT  # | {} add more if ever needed

station_names = pytest.mark.parametrize("station", ("Birkenes", "Gartow", "Hohenpeissenberg"))


@pytest.fixture(scope="module")
def icos_path() -> Path:
    try:
        return Path(const.OBSLOCS_UNGRIDDED[const.ICOS_NAME])
    except KeyError:
        pytest.skip(reason="ICOS path not initialised due to non existence in CI")


@pytest.fixture(scope="module")
def reader(icos_path: Path) -> ReadICOS:
    return ReadICOS(data_dir=str(icos_path))


@pytest.fixture()
def station_files(icos_path: Path, station: str) -> list[Path]:
    files = sorted(icos_path.rglob(f"icos-co2-{station}*.nc"))
    assert files, f"no files for {station}"
    return files


def test_DATASET_NAME(reader: ReadICOS):
    assert reader.DATASET_NAME == "ICOS"


def test_DEFAULT_VARS(reader: ReadICOS):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


def test_files(reader: ReadICOS):
    assert reader.files, "no stations files found"
    assert len(reader.files) >= 1, "found less files than expected"


def test_FOUND_FILES(reader: ReadICOS):
    assert reader.FOUND_FILES, "no stations files found"
    assert len(reader.FOUND_FILES) >= 1, "found less files than expected"


@station_names
def test_stations(reader: ReadICOS, station: str):
    assert reader.stations()[station], f"no {station} station files"


def test_PROVIDES_VARIABLES(reader: ReadICOS):
    assert set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@station_names
def test_read_file(reader: ReadICOS, station_files: list[str]):
    data = reader.read_file(station_files[-1])
    assert set(data.contains_vars) <= VARS_DEFAULT


def test_read_file_error(reader: ReadICOS):
    bad_station_file = "not-a-file.nc"
    with pytest.raises(ValueError) as e:
        reader.read_file(bad_station_file)
    assert str(e.value) == f"missing {bad_station_file}"


@station_names
def test_read(reader: ReadICOS, station_files: list[str]):
    for var in VARS_PROVIDED:
        data = reader.read(var, station_files, first_file=0, last_file=1)
        assert set(data.contains_vars) <= VARS_PROVIDED


def test_read_error(reader: ReadICOS):
    bad_variable_name = "not-a-variable"
    with pytest.raises(ValueError) as e:
        reader.read(bad_variable_name)
    assert str(e.value) == f"Unsupported variables: {bad_variable_name}"


def test_reader_gives_correct_icos_path(reader: ReadICOS, icos_path: Path):
    assert reader.data_dir == str(icos_path)
