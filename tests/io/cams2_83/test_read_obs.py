from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from pyaerocom import const
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
