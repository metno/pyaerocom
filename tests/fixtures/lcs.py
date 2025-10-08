from .data_access import DataForTests
from pyaerocom.io import PyaroConfig, ReadPyaro
import pytest

OBS_PATH = DataForTests("obsdata/LCS/2019").path


@pytest.fixture
def lcs_data():
    reader_id = "lcsreader"
    config = PyaroConfig(
        name="test-lcs",
        reader_id=reader_id,
        filename_or_obj_or_url=str(OBS_PATH),
        filters={},
        network="SC",
        min_quality=2,
        name_map={
            "PM25": "concpm25",
        },
    )

    reader = ReadPyaro(config)

    return reader.read(vars_to_retrieve=["concpm25"])
