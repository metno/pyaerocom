from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom.plugins.mep.reader import ReadMEP

MEP_PATH = Path("/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MEP/download")

STATION_NAMES = ("1478A", "2706A", "3377A")

VARS_DEFAULT = {"concco", "concno2", "conco3", "concpm10", "concpm25", "concso2"}
VARS_PROVIDED = VARS_DEFAULT | {"vmro3", "vmro3max", "vmrno2"}


needs_mep_path = pytest.mark.xfail(not MEP_PATH.is_dir(), reason=f"needs access to {MEP_PATH}")


@pytest.fixture(scope="module")
def reader() -> ReadMEP:
    return ReadMEP(data_dir=str(MEP_PATH))


@pytest.fixture()
def station_files(station: str) -> list[Path]:
    files = sorted(MEP_PATH.rglob(f"mep-rd-{station}-*.nc"))
    assert files, f"no files for {station}"
    return files


def test_reader_error():
    with pytest.raises(ValueError) as e:
        ReadMEP(data_dir=None)


@needs_mep_path
def test_DATASET_NAME(reader: ReadMEP):
    assert reader.DATASET_NAME == "MEP_HARP"


@needs_mep_path
def test_DEFAULT_VARS(reader: ReadMEP):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


@needs_mep_path
def test_files(reader: ReadMEP):
    assert reader.files, "no stations files found"
    assert len(reader.files) >= 167482, "found less files than expected"


@needs_mep_path
def test_FOUND_FILES(reader: ReadMEP):
    assert reader.FOUND_FILES, "no stations files found"
    assert len(reader.FOUND_FILES) >= 167482, "found less files than expected"


@pytest.mark.parametrize("station", STATION_NAMES)
@needs_mep_path
def test_stations(reader: ReadMEP, station: str):
    assert reader.stations()[station], f"no {station} station files"


@needs_mep_path
def test_PROVIDES_VARIABLES(reader: ReadMEP):
    return set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@pytest.mark.parametrize("station", STATION_NAMES)
@needs_mep_path
def test_read_file(reader: ReadMEP, station_files: list[str]):
    data = reader.read_file(station_files[-1])
    assert set(data.contains_vars) == VARS_DEFAULT


@needs_mep_path
def test_read_file_error(reader: ReadMEP):
    bad_station_file = "not-a-file.nc"
    with pytest.raises(ValueError) as e:
        reader.read_file(bad_station_file)
    assert str(e.value) == f"missing {bad_station_file}"


@pytest.mark.parametrize("station", STATION_NAMES)
@needs_mep_path
def test_read(reader: ReadMEP, station_files: list[str]):
    data = reader.read(VARS_PROVIDED, station_files, first_file=0, last_file=5)
    assert set(data.contains_vars) == VARS_PROVIDED


@needs_mep_path
def test_read_error(reader: ReadMEP):
    bad_variable_name = "not-a-variable"
    with pytest.raises(ValueError) as e:
        reader.read((bad_variable_name,))
    assert str(e.value) == f"Unsupported variables: {bad_variable_name}"
