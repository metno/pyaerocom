from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.io.cams2_83.obs import DEFAULT_METADATA_NAME, read_csv
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH, ReadCAMS2_83
from pyaerocom.io.cams2_83.read_obs import obs_paths as find_obs_paths
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

TEST_DATE = datetime(2021, 12, 1)
TEST_DATES = [TEST_DATE + timedelta(days=d) for d in range(3)]


@pytest.fixture
def obs_paths(dates: list[str | date | datetime]) -> list[Path]:
    if not DATA_FOLDER_PATH.is_dir():
        pytest.skip(f"no access to {DATA_FOLDER_PATH}")
    paths = find_obs_paths(*dates)
    return list(paths)


@pytest.fixture
def tmp_obs_file(tmp_path) -> Path:
    tmp_dir = tmp_path / "tmp_d1"
    tmp_dir.mkdir(parents=True)
    tmp_file = tmp_dir / "obs.csv"
    tmp_file.write_text(
        """
            STATION;LAT;LON;ALT(m);PARAMETER;YEAR;MONTH;DAY;HOUR;AVERAGING_PERIOD(h);CONCENTRATION(kg/m3)
            AT0ENK1;48.392; 13.671;0525;o3;2025;02;12;01;1; 4.27600e-08
            AT0ILL1;47.770; 16.766;0117;o3;2025;02;12;01;1; 6.56700e-08
    """
    )
    return tmp_file


@pytest.mark.parametrize("dates", [TEST_DATES])
def test_obs_paths(obs_paths: list[Path]):
    for path in obs_paths:
        assert path.exists()


def test_init():
    data = ReadCAMS2_83()
    assert isinstance(data, ReadUngriddedBase)


@pytest.mark.parametrize("dates", [TEST_DATES])
def test_read_ungridded(obs_paths: list[Path]):
    data = ReadUngridded().read(const.CAMS2_83_NRT_NAME, "concco", files=obs_paths)
    assert isinstance(data, UngriddedData)


def test_obs_no_metadata_file(tmp_obs_file, caplog):
    df = read_csv(tmp_obs_file, polls=["O3"])
    assert (
        f"Metadata file {tmp_obs_file.parent.parent / DEFAULT_METADATA_NAME} does not exist"
        in caplog.text
    )
    assert df.columns.values.tolist() == [
        "station",
        "lat",
        "lon",
        "alt",
        "time",
        "poll",
        "conc",
    ]


def test_obs_invalid_metadata_file(tmp_obs_file, caplog):
    tmp_metadata_file = tmp_obs_file.parent.parent / DEFAULT_METADATA_NAME
    tmp_metadata_file.write_text(
        """
        something not parsable as expected
        bla;bla;bla
        bla;bla;bla
        """
    )

    df = read_csv(tmp_obs_file, polls=["O3"])
    assert df.columns.values.tolist() == [
        "station",
        "lat",
        "lon",
        "alt",
        "time",
        "poll",
        "conc",
    ]
    assert "Invalid metadata file" in caplog.text


def test_obs_empty_metadata_file(tmp_obs_file, caplog):
    tmp_metadata_file = tmp_obs_file.parent.parent / DEFAULT_METADATA_NAME
    tmp_metadata_file.write_text("station, station_type")

    df = read_csv(tmp_obs_file, polls=["O3"])
    assert df.columns.values.tolist() == [
        "station",
        "lat",
        "lon",
        "alt",
        "time",
        "poll",
        "conc",
    ]
    assert "Empty metadata" in caplog.text


def test_obs_ok_metadata_file(tmp_obs_file):
    tmp_metadata_file = tmp_obs_file.parent.parent / DEFAULT_METADATA_NAME
    tmp_metadata_file.write_text(
        """
        something, something, something
        bla, bla, bla
        bla, bla, bla
        """
    )

    df = read_csv(tmp_obs_file, polls=["O3"])
    assert df.columns.values.tolist() == [
        "station",
        "lat",
        "lon",
        "alt",
        "time",
        "poll",
        "conc",
        "station_type",
    ]


def test_obs_read_to_ungridded(tmp_obs_file, caplog):
    tmp_metadata_file = tmp_obs_file.parent.parent / DEFAULT_METADATA_NAME
    tmp_metadata_file.write_text(
        """
        something, something, something
        AT0ENK1, bla, rur
        AT0ENK1, bla, sub
        """
    )
    reader = ReadCAMS2_83()
    data = reader.read(vars_to_retrieve=["conco3"], files=[tmp_obs_file])
    assert isinstance(data, UngriddedData)
    assert "Time needed to convert obs to ungridded" in caplog.text
    assert all("station_type" in dict.keys() for dict in data.metadata.values())
