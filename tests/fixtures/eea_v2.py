import pytest

from pyaerocom.io import ReadEEAAQEREP_V2


@pytest.fixture(scope="session")
def eea_v2_subset_reader() -> ReadEEAAQEREP_V2:
    return ReadEEAAQEREP_V2("EEA_AQeRep.v2.Subset")
