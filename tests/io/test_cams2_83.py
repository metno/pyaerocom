from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest
import xarray as xr

from pyaerocom.io.cams2_83.models import ModelName, PollutantName
from pyaerocom.io.cams2_83.reader import find_model_path


@pytest.mark.parametrize(
    "model,name",
    [
        ("EMEP", "emep"),
        ("MATCH", "match"),
        ("EURAD", "euradim"),
    ],
)
def test_ModelName(model: str, name: str):
    assert ModelName[model] == name


@pytest.mark.parametrize(
    "poll,name",
    [
        ("O3", "ozone"),
        ("NO2", "nitrogen_dioxide"),
        ("PM10", "particulate_matter_10um"),
        ("PM25", "particulate_matter_2.5um"),
    ],
)
def test_PollutantName(poll: str, name: str):
    assert PollutantName[poll] == name


@pytest.fixture
def model_path(model: str | ModelName, date: str | date | datetime) -> Path:
    return find_model_path(model, date)


@pytest.mark.skip(reason="No access to lustre")
@pytest.mark.parametrize("date", ["20210602", date(2021, 6, 2), datetime(2021, 6, 2)])
@pytest.mark.parametrize("model", ["EMEP", ModelName.EMEP])
def test_find_model_path(model_path: Path):
    assert model_path.exists()


@pytest.mark.skip(reason="No access to lustre")
@pytest.fixture
def model_dataset(model_path: Path) -> xr.Dataset:
    return xr.open_dataset(model_path)

@pytest.mark.skip(reason="No access to lustre")
@pytest.mark.parametrize("date", ["20210602"])
@pytest.mark.parametrize("model", ["EMEP", "MATCH"])
def test_model_file_contents(model_dataset: xr.Dataset):
    for poll in PollutantName:
        poll.value in model_dataset.data_vars
