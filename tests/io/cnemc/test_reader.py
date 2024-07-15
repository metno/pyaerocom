from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.io.cnemc.reader import ReadCNEMC

STATION_NAMES = ("1478A", "2706A", "3377A")
VARS_DEFAULT = {"concco", "concno2", "conco3", "concpm10", "concpm25", "concso2"}
VARS_PROVIDED = VARS_DEFAULT | {"vmro3", "vmro3max", "vmrno2"}


@pytest.fixture(scope="module")
def mep_path() -> Path:
    try:
        path = Path(const.OBSLOCS_UNGRIDDED[const.CNEMC_NAME])
    except KeyError:
        pytest.skip("CNEMC path is not registered")

    if not path.exists():
        pytest.skip(f"missing {path}, this os OK on CI")

    return path


@pytest.fixture(scope="module")
def reader(mep_path: Path) -> ReadCNEMC:
    return ReadCNEMC(data_dir=str(mep_path))


@pytest.fixture()
def station_files(mep_path: Path, station: str) -> list[Path]:
    files = sorted(mep_path.rglob(f"mep-rd-{station}-*.nc"))
    assert files, f"no files for {station}"
    return files


def test_DATASET_NAME(reader: ReadCNEMC):
    assert reader.DATASET_NAME == "CNEMC"


def test_DEFAULT_VARS(reader: ReadCNEMC):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


def test_files(reader: ReadCNEMC):
    assert reader.files, "no stations files found"
    assert len(reader.files) >= 3, "found less files than expected"


def test_FOUND_FILES(reader: ReadCNEMC):
    assert reader.FOUND_FILES, "no stations files found"
    assert len(reader.FOUND_FILES) >= 3, "found less files than expected"


@pytest.mark.parametrize("station", STATION_NAMES)
def test_stations(reader: ReadCNEMC, station: str):
    assert reader.stations()[station], f"no {station} station files"


def test_PROVIDES_VARIABLES(reader: ReadCNEMC):
    assert set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@pytest.mark.parametrize("station", STATION_NAMES)
def test_read_file(reader: ReadCNEMC, station_files: list[str]):
    data = reader.read_file(station_files[-1])
    assert set(data.contains_vars) == VARS_DEFAULT


def test_read_file_error(reader: ReadCNEMC):
    bad_station_file = "not-a-file.nc"
    with pytest.raises(ValueError) as e:
        reader.read_file(bad_station_file)
    assert str(e.value) == f"missing {bad_station_file}"


@pytest.mark.parametrize("station", STATION_NAMES)
def test_read(reader: ReadCNEMC, station_files: list[str]):
    data = reader.read(VARS_PROVIDED, station_files, first_file=0, last_file=5)
    assert set(data.contains_vars) == VARS_PROVIDED


def test_read_error(reader: ReadCNEMC):
    bad_variable_name = "not-a-variable"
    with pytest.raises(ValueError) as e:
        reader.read((bad_variable_name,))
    assert str(e.value) == f"Unsupported variables: {bad_variable_name}"


def test_reader_gives_correct_mep_path(reader: ReadCNEMC, mep_path: Path):
    assert Path(reader.data_dir) == mep_path
