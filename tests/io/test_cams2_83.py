import pytest

from pyaerocom.io.cams2_83.models import ModelName, PollutantName
from pyaerocom.io.cams2_83.reader import find_model_path


@pytest.mark.parametrize(
    "model,name",
    [("EMEP", "emep"), ("MATCH", "match"), ("EURAD", "euradim")],
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


def test_find_model_path():
    assert False
