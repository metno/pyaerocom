from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest
import xarray as xr

from pyaerocom.io.cams2_83.models import RunType
from pyaerocom.io.cams2_83.reader import AEROCOM_NAMES, DATA_FOLDER_PATH, all_model_paths
from pyaerocom.io.cams2_83.reader import model_path as one_model_path
from pyaerocom.io.cams2_83.reader import read_dataset


@pytest.fixture
def model_path(model: str, date: str, run: str) -> Path:
    if not DATA_FOLDER_PATH.is_dir():
        pytest.skip(f"no access to {DATA_FOLDER_PATH}")
    return one_model_path(model, date, run=run)


@pytest.mark.parametrize("date,model", [("20211202", "EMEP")])
@pytest.mark.parametrize("run", RunType)
def test_find_model_path(model_path: Path):
    assert model_path.exists()


@pytest.mark.skipif(not DATA_FOLDER_PATH.is_dir(), reason=f"no access to {DATA_FOLDER_PATH}")
def test_all_model_paths():
    date = datetime(2021, 12, 2)
    dates = (date, date.date(), f"{date:%Y%m%d}")
    assert len(list(all_model_paths("EMEP", *dates))) == len(dates) == 3
    assert len(set(all_model_paths("EMEP", *dates))) == 1


@pytest.fixture
def model_dataset(model: str, run: str, dates: list[str], day: int) -> xr.Dataset:
    paths = all_model_paths(model, *dates, run=run)
    return read_dataset(list(paths), day=day)


@pytest.mark.parametrize("dates,steps", [("20211201 20211202 20211203".split(), 24 * 3)])
@pytest.mark.parametrize("model", ["EMEP"])
@pytest.mark.parametrize("run,day", [("AN", 0), ("FC", 0), ("FC", 3)])
def test_model_file_contents(model_dataset: xr.Dataset, steps: int):
    for var_name in AEROCOM_NAMES.values():
        assert var_name in model_dataset
    assert len(model_dataset.time) == steps
