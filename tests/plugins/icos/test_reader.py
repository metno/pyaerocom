from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.icos.reader import ReadICOS
from tests.conftest import lustre_unavail

try:
    ICOS_PATH = Path(const.OBSLOCS_UNGRIDDED[const.ICOS_NAME])
except KeyError:
    pytest.mark.skip(reason=f"ICOS path not initialised due to non existence in CI")


VARS_DEFAULT = {"vmrco2"}


@lustre_unavail
@pytest.fixture(scope="module")
def reader() -> ReadICOS:
    return ReadICOS(data_dir=str(ICOS_PATH))


@lustre_unavail
@pytest.fixture()
def station_files(station: str) -> list[Path]:
    files = sorted(ICOS_PATH.rglob(f"icos-co2-nrt-{station}-.*-.*-.*.nc"))
    assert files, f"no files for {station}"
    return files


@lustre_unavail
def test_DATASET_NAME(reader: ReadICOS):
    assert reader.DATASET_NAME == "ICOS"


@lustre_unavail
def test_DEFAULT_VARS(reader: ReadICOS):
    assert set(reader.DEFAULT_VARS) >= VARS_DEFAULT


@lustre_unavail
def test_files(reader: ReadICOS):
    assert reader.files, "no stations files found"
    # assert len(reader.files) >= 3, "found less files than expected"


@lustre_unavail
def test_FOUND_FILES(reader: ReadICOS):
    assert reader.FOUND_FILES, "no stations files found"
    # assert len(reader.FOUND_FILES) >= 3, "found less files than expected"


@lustre_unavail
@pytest.mark.parametrize("station", STATION_NAMES)
def test_stations(reader: ReadICOS, station: str):
    assert reader.stations()[station], f"no {station} station files"


@lustre_unavail
def test_PROVIDES_VARIABLES(reader: ReadICOS):
    return set(reader.PROVIDES_VARIABLES) >= VARS_PROVIDED


@lustre_unavail
@pytest.mark.parametrize("station", STATION_NAMES)
def test_read_file(reader: ReadICOS, station_files: list[str]):
    data = reader.read_file(station_files[-1])
    assert set(data.contains_vars) == VARS_DEFAULT


@lustre_unavail
def test_read_file_error(reader: ReadICOS):
    bad_station_file = "not-a-file.nc"
    with pytest.raises(ValueError) as e:
        reader.read_file(bad_station_file)
    assert str(e.value) == f"missing {bad_station_file}"


@lustre_unavail
@pytest.mark.parametrize("station", STATION_NAMES)
def test_read(reader: ReadICOS, station_files: list[str]):
    # data = reader.read(VARS_PROVIDED, station_files, first_file=0, last_file=5)
    # assert set(data.contains_vars) == VARS_PROVIDED
    pass


@lustre_unavail
def test_read_error(reader: ReadICOS):
    bad_variable_name = "not-a-variable"
    with pytest.raises(ValueError) as e:
        reader.read((bad_variable_name,))
    assert str(e.value) == f"Unsupported variables: {bad_variable_name}"


@lustre_unavail
def test_reader_gives_correct_mep_path(reader: ReadICOS):
    assert str(ICOS_PATH) == reader.data_dir
