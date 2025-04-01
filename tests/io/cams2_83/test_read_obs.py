from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent

import pytest

from pyaerocom import const
from pyaerocom.io.cams2_83.obs import DEFAULT_METADATA_NAME, read_csv
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH, ReadCAMS2_83
from pyaerocom.io.cams2_83.read_obs import obs_paths as find_obs_paths
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungridded_data_container import UngriddedDataContainer

TEST_DATE = datetime(2021, 12, 1)
TEST_DATES = [TEST_DATE + timedelta(days=d) for d in range(3)]


@pytest.fixture
def obs_paths() -> list[Path]:
    if not DATA_FOLDER_PATH.is_dir():
        pytest.skip(f"no access to {DATA_FOLDER_PATH}")
    paths = find_obs_paths(*TEST_DATES)
    return list(paths)


@pytest.fixture
def obs_file(tmp_path: Path) -> Path:
    obs = """
        STATION;LAT;LON;ALT(m);PARAMETER;YEAR;MONTH;DAY;HOUR;AVERAGING_PERIOD(h);CONCENTRATION(kg/m3)
        AT0ENK1;48.392; 13.671;0525;o3;2025;02;12;01;1; 4.27600e-08
        AT0ILL1;47.770; 16.766;0117;o3;2025;02;12;01;1; 6.56700e-08
        """

    path = tmp_path / "tmp_d1" / "obs.csv"
    path.parent.mkdir(parents=True)
    path.write_text(dedent(obs))
    return path


@pytest.fixture
def metadata_file(tmp_path: Path) -> Path:
    return tmp_path / DEFAULT_METADATA_NAME


def test_init():
    data = ReadCAMS2_83()
    assert isinstance(data, ReadUngriddedBase)


def test_obs_paths(obs_paths: list[Path]):
    for path in obs_paths:
        assert path.exists()


def test_read_ungridded(obs_paths: list[Path]):
    data = ReadUngridded().read(const.CAMS2_83_NRT_NAME, "concco", files=obs_paths)
    assert isinstance(data, UngriddedDataContainer)


def test_obs_no_metadata_file(
    obs_file: Path, metadata_file: Path, caplog: pytest.LogCaptureFixture
):
    df = read_csv(obs_file, polls=["O3"])
    assert f"Metadata file {metadata_file} does not exist" in caplog.text
    assert list(df) == ["station", "lat", "lon", "alt", "time", "poll", "conc"]


def test_obs_invalid_metadata_file(
    obs_file: Path, metadata_file: Path, caplog: pytest.LogCaptureFixture
):
    metadata = """
        something not parsable as expected
        bla;bla;bla
        bla;bla;bla
        """
    metadata_file.write_text(dedent(metadata))

    df = read_csv(obs_file, polls=["O3"])
    assert list(df) == ["station", "lat", "lon", "alt", "time", "poll", "conc"]
    assert "Invalid metadata file" in caplog.text


def test_obs_empty_metadata_file(
    obs_file: Path, metadata_file: Path, caplog: pytest.LogCaptureFixture
):
    metadata = "station, station_type"
    metadata_file.write_text(metadata)

    df = read_csv(obs_file, polls=["O3"])
    assert list(df) == ["station", "lat", "lon", "alt", "time", "poll", "conc"]
    assert "Empty metadata" in caplog.text


def test_obs_ok_metadata_file(obs_file: Path, metadata_file: Path):
    metadata = """
        something, something, something
        bla, bla, bla
        bla, bla, bla
        """
    metadata_file.write_text(dedent(metadata))

    df = read_csv(obs_file, polls=["O3"])
    assert list(df) == [
        "station",
        "lat",
        "lon",
        "alt",
        "time",
        "poll",
        "conc",
        "station_type",
    ]
    assert df["station_type"].isna().all()


def test_obs_read_to_ungridded(
    obs_file: Path, metadata_file: Path, caplog: pytest.LogCaptureFixture
):
    metadata = """
        something, something, something
        AT0ENK1, bla, rur
        AT0ILL1, bla, sub
        """
    metadata_file.write_text(dedent(metadata))

    reader = ReadCAMS2_83()
    data = reader.read(vars_to_retrieve=["conco3"], files=[obs_file])
    assert isinstance(data, UngriddedDataContainer)
    assert "Time needed to convert obs to ungridded" in caplog.text
    assert all("station_type" in dict for dict in data.metadata.values())
    assert {dict["station_type"] for dict in data.metadata.values()} == {"rur", "sub"}
