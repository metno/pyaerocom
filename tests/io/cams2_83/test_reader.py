from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
import xarray as xr

from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.io.cams2_83.reader import AEROCOM_NAMES, DATA_FOLDER_PATH
from pyaerocom.io.cams2_83.reader import model_paths as find_model_paths
from pyaerocom.io.cams2_83.reader import read_dataset

TEST_DATE = datetime(2021, 12, 1)
TEST_DATES = [TEST_DATE + timedelta(days=d) for d in range(3)]


@pytest.fixture
def model_paths(
    model: str | ModelName, run: str | RunType, dates: list[str | date | datetime]
) -> list[Path]:
    if not DATA_FOLDER_PATH.is_dir():
        pytest.skip(f"no access to {DATA_FOLDER_PATH}")
    paths = find_model_paths(model, *dates, run=run)
    return list(paths)


@pytest.mark.parametrize("model", ["EMEP"])
@pytest.mark.parametrize("run", RunType)
@pytest.mark.parametrize(
    "dates,num,unique",
    [
        ([TEST_DATE, TEST_DATE.date(), TEST_DATE.strftime("%Y%m%d")], 3, 1),
        (TEST_DATES, len(TEST_DATES), len(TEST_DATES)),
    ],
)
def test_model_paths(model_paths: list[Path], num: int, unique: int):
    assert bool(model_paths)
    assert all(path.exists() for path in model_paths)
    assert len(model_paths) == num
    assert len(set(model_paths)) == unique


@pytest.fixture
def model_dataset(model_paths: list[Path], day: int) -> xr.Dataset:
    return read_dataset(model_paths, day=day)


@pytest.mark.parametrize("dates,steps", [(TEST_DATES, len(TEST_DATES) * 24)])
@pytest.mark.parametrize("model", ["EMEP"])
@pytest.mark.parametrize("run,day", [("AN", 0), ("FC", 0), ("FC", 3)])
def test_model_file_contents(model_dataset: xr.Dataset, steps: int):
    for var_name in AEROCOM_NAMES.values():
        assert var_name in model_dataset
    assert len(model_dataset.time) == steps
