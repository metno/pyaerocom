import pytest

from pyaerocom.io import ReadAeronetSdaV3, ReadAeronetSunV3
from pyaerocom.ungriddeddata import UngriddedData


@pytest.fixture(scope="session")
def aeronet_sun_subset_reader() -> ReadAeronetSunV3:
    return ReadAeronetSunV3("AeronetSunV3L2Subset.daily")


@pytest.fixture(scope="session")
def aeronet_sda_subset_reader() -> ReadAeronetSdaV3:
    return ReadAeronetSdaV3("AeronetSDAV3L2Subset.daily")


@pytest.fixture(scope="session")
def aeronetsunv3lev2_subset(aeronet_sun_subset_reader: ReadAeronetSunV3) -> UngriddedData:
    return aeronet_sun_subset_reader.read(vars_to_retrieve=["od550aer", "ang4487aer"])


@pytest.fixture(scope="session")
def aeronetsdav3lev2_subset(aeronet_sda_subset_reader: ReadAeronetSdaV3) -> UngriddedData:
    return aeronet_sda_subset_reader.read(vars_to_retrieve=["od550aer", "od550lt1aer"])
