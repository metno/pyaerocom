from __future__ import annotations

from types import SimpleNamespace

import pytest

from pyaerocom.griddeddata import GriddedData
from .data_access import DataForTests

CHECK_PATHS = SimpleNamespace(
    emep_ci="modeldata/EMEP.CI",
)

EMEP_CI_DATA_PATH = DataForTests(CHECK_PATHS.emep_ci).path


@pytest.fixture(scope="session")
def data_emep_ci() -> GriddedData:
    path = DataForTests(CHECK_PATHS.emep_ci).path
    assert path.exists()
    data = GriddedData(path)
    return data
