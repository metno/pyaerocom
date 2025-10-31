from __future__ import annotations

import pytest

from pyaerocom.griddeddata import GriddedData
from tests.fixtures.data_access import TEST_DATA
from .data_access import DataForTests

CMIP_CI_DATA_PATH = str(TEST_DATA["MODELS"].path / "CMIP6")


# # CHECK_PATHS = SimpleNamespace(
# #     cmip_ci="modeldata/CMIP6",
# # )
#
# CMIP_CI_DATA_PATH = DataForTests(CHECK_PATHS.emep_ci).path


@pytest.fixture(scope="session")
def data_cmip_ci() -> GriddedData:
    path = DataForTests(CMIP_CI_DATA_PATH).path
    assert path.exists()
    data = GriddedData(path)
    return data


def path_cmip_ci() -> str:
    return CMIP_CI_DATA_PATH
