import pytest

from pyaerocom.io import ReadAeronetSdaV3, ReadAeronetSunV3


@pytest.fixture(scope="session")
def aeronet_sun_subset_reader():
    reader = ReadAeronetSunV3("AeronetSunV3L2Subset.daily")
    return reader


@pytest.fixture(scope="session")
def aeronet_sda_subset_reader():
    reader = ReadAeronetSdaV3("AeronetSDAV3L2Subset.daily")
    return reader


@pytest.fixture(scope="session")
def aeronetsunv3lev2_subset(aeronet_sun_subset_reader):
    reader = aeronet_sun_subset_reader
    return reader.read(vars_to_retrieve=["od550aer", "ang4487aer"])


@pytest.fixture(scope="session")
def aeronetsdav3lev2_subset(aeronet_sda_subset_reader):
    reader = aeronet_sda_subset_reader
    return reader.read(vars_to_retrieve=["od550aer", "od550lt1aer"])
