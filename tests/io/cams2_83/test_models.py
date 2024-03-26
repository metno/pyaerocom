from pathlib import Path

import pytest

from pyaerocom.io.cams2_83.models import ModelData, ModelName, RunType


@pytest.mark.parametrize("model", ModelName)
def test_ModelName(model: ModelName):
    assert model == str(model) == model.value


@pytest.mark.parametrize("run", RunType)
def test_RunType(run: RunType):
    assert run == str(run) == run.value


@pytest.fixture
def model_data(tmp_path: Path, model_name: ModelName, run_type: RunType) -> ModelData:
    """ModelData on a temporary path"""
    return ModelData(model_name, run_type, root=tmp_path)


@pytest.mark.parametrize("model_name", ModelName)
@pytest.mark.parametrize("run_type", RunType)
def test_ModelData_frompath(model_data: ModelData):
    path = model_data.path
    assert ModelData.frompath(str(path)) == ModelData.frompath(path) == model_data
