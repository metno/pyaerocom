from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from textwrap import dedent

import pytest

from pyaerocom import const
from pyaerocom.io.cams2_83.obs import DEFAULT_METADATA_NAME
from pyaerocom.io.cams2_83.read_obs import DATA_FOLDER_PATH, ReadCAMS2_83
from pyaerocom.io.cams2_83.read_obs import obs_paths as find_obs_paths
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

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
    assert isinstance(data, UngriddedData)
