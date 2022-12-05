from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.harp.reader import ReadHARP

LUSTRE_PATH = Path("/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MEP/download")

STATION_NAMES = ("1478A", "2706A", "3377A")

VARS_DEFAULT = {"concco", "concno2", "conco3", "concpm10", "concpm25", "concso2"}
VARS_PROVIDED = VARS_DEFAULT | {"vmro3", "vmro3max", "vmrno2"}


pytestmark = pytest.mark.xfail(
    not const.has_access_lustre, reason=f"needs access to {LUSTRE_PATH}"
)


@pytest.fixture(scope="module")
def reader() -> ReadHARP:
    if not LUSTRE_PATH.is_dir():  # pragma: no cover
        pytest.fail(f"needs {LUSTRE_PATH}")
    return ReadHARP(data_dir=str(LUSTRE_PATH))


@pytest.fixture()
def station_files(reader: ReadHARP, station: str) -> list[Path]:
    files = reader.stations().get(station)
    assert files, f"no files for {station}"
    return files


def test_DATASET_NAME(reader: ReadHARP):
    assert reader.DATASET_NAME == "HARP"


def test_DEFAULT_VARS(reader: ReadHARP):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


def test_files(reader: ReadHARP):
    assert reader.files, "no stations files found"
    assert len(reader.files) >= 167482, "found less files than expected"


def test_FOUND_FILES(reader: ReadHARP):
    assert reader.FOUND_FILES, "no stations files found"
    assert len(reader.FOUND_FILES) >= 167482, "found less files than expected"


@pytest.mark.parametrize("station", STATION_NAMES)
def test_stations(reader: ReadHARP, station: str):
    assert reader.stations()[station], f"no {station} station files"


def test_PROVIDES_VARIABLES(reader: ReadHARP):
    return set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@pytest.mark.parametrize("station", STATION_NAMES)
def test_read_file(reader: ReadHARP, station_files: list[str]):
    data = reader.read_file(station_files[-1])
    assert set(data.contains_vars) == VARS_DEFAULT


def test_read_file_error(reader: ReadHARP):
    bad_station_file = "not-a-file.nc"
    with pytest.raises(ValueError) as e:
        reader.read_file(bad_station_file)
    assert str(e.value) == f"missing {bad_station_file}"


@pytest.mark.parametrize("station", STATION_NAMES)
def test_read(reader: ReadHARP, station_files: list[str]):
    data = reader.read(VARS_PROVIDED, station_files, first_file=0, last_file=5)
    assert set(data.contains_vars) == VARS_PROVIDED


def test_read_error(reader: ReadHARP):
    bad_variable_name = "not-a-variable"
    with pytest.raises(ValueError) as e:
        reader.read((bad_variable_name,))
    assert str(e.value) == f"Unsupported variables: {bad_variable_name}"
