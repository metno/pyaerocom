from __future__ import annotations


from tests.fixtures.data_access import TEST_DATA
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from pyaerocom import GriddedData

import pytest

EMEP_DATA_PATH = TEST_DATA["MODELS"].path / "EMEP_cities"
UEMEP_DATA_PATH = TEST_DATA["MODELS"].path / "uEMEP_cities"

EMEP_FILE_PATHS = [
    EMEP_DATA_PATH / "Amsterdam",
    EMEP_DATA_PATH / "Berlin",
]

EMEP_FILE_PATHS_SPLIT = [
    EMEP_DATA_PATH / "Berlin_split_1",
    EMEP_DATA_PATH / "Berlin_split_2",
]

UEMEP_FILE_PATHS = [
    UEMEP_DATA_PATH / "Bordeaux",
    UEMEP_DATA_PATH / "Lyon",
]


@pytest.fixture
def cities_data() -> dict[str, list[GriddedData]]:
    data_dict = {}

    data_dict["uEMEP"] = [
        ReadMscwCtm("uemep", str(ddir)).read_var("concpm25", ts_type="hourly")
        for ddir in UEMEP_FILE_PATHS
    ]
    data_dict["EMEP"] = [
        ReadMscwCtm("emep", str(ddir)).read_var("concpm25", ts_type="monthly")
        for ddir in EMEP_FILE_PATHS
    ]

    data_dict["EMEP_split"] = [
        ReadMscwCtm("emep", str(ddir)).read_var("concpm25", ts_type="monthly")
        for ddir in EMEP_FILE_PATHS_SPLIT
    ]

    return data_dict
