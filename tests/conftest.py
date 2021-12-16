import os
from importlib import metadata

import matplotlib
import numpy as np
import pytest
from packaging.version import Version

from pyaerocom import const
from pyaerocom.access_testdata import AccessTestData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.io import ReadAasEtal, ReadAeronetSdaV3, ReadAeronetSunV3

from ._conftest_helpers import (
    _create_fake_coldata_3d,
    _create_fake_coldata_3d_hourly,
    _create_fake_coldata_4d,
    _create_fake_coldata_5d,
    _create_fake_trends_coldata_3d,
    create_fake_stationdata_list,
)
from .synthetic_data import FakeStationDataAccess

pytest_plugins = [
    "tests.fixtures.emep",
    "tests.fixtures.tm5",
    "tests.fixtures.ebas",
]

matplotlib.use("Agg")

TEST_RTOL = 1e-4

FAKE_STATION_DATA = FakeStationDataAccess()

# class that provides / ensures access to testdataset
tda = AccessTestData()

TESTDATADIR = tda.testdatadir

# Additional paths that have to exist (for sanity checking)
CHECK_PATHS = {
    "tm5": "modeldata/TM5-met2010_CTRL-TEST/renamed",
    "tm5aod": "modeldata/TM5-met2010_CTRL-TEST/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
    "emep": "modeldata/EMEP_2017",
    "coldata_tm5_aeronet": "coldata/od550aer_REF-AeronetSunV3L2Subset.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc",
}

TEST_VARS_AERONET = ["od550aer", "ang4487aer"]


# checks if testdata-minimal is available and if not, tries to download it
# automatically into ~/MyPyaerocom/testdata-minimal

assert tda.init(), "cound not find minimal test data"


# skipif marker that is True if no access to metno PPI is provided
# (some tests are skipped in this case)
lustre_unavail = pytest.mark.skipif(
    not const.has_access_lustre,
    reason="Skipping tests that require access to AEROCOM database on METNo servers",
)

lustre_avail = pytest.mark.skipif(
    const.has_access_lustre, reason="Skipping tests that will crash if lustre can be accessed."
)

# custom skipif marker that is used below for test functions that
# require geonum to be installed
geonum_unavail = pytest.mark.skipif(
    not const.GEONUM_AVAILABLE, reason="Skipping tests that require geonum."
)

try:
    import reverse_geocode

    rg_avail = True
except ModuleNotFoundError:
    rg_avail = False

rg_unavail = pytest.mark.skipif(
    not rg_avail, reason="Skipping tests that require access to reverse_geocode"
)

etopo1_unavail = pytest.mark.skipif(
    not const.ETOPO1_AVAILABLE, reason="Skipping tests that require access to ETOPO1 data"
)


try:
    import geojsoncontour

    geojson_avail = True
except ModuleNotFoundError:
    geojson_avail = False

geojson_unavail = pytest.mark.skipif(
    not geojson_avail, reason="Skipping tests that require access geojsoncontour"
)

broken_test = pytest.mark.skip(reason="Method raises Exception")

### Fixtures representing data


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
    r = aeronet_sun_subset_reader
    return r.read(vars_to_retrieve=TEST_VARS_AERONET)


@pytest.fixture(scope="session")
def aeronetsdav3lev2_subset(aeronet_sda_subset_reader):
    r = aeronet_sda_subset_reader
    return r.read(vars_to_retrieve=["od550aer", "od550lt1aer"])


@pytest.fixture(scope="session")
def tempdir(tmpdir_factory):
    """Temporary directory for dumping data shared between tests"""
    tmpdir = tmpdir_factory.mktemp("data")
    return tmpdir


@pytest.fixture(scope="session")
def statlist():
    data = {}
    stats = create_fake_stationdata_list()
    data["all"] = stats
    data["od550aer"] = [stat.copy() for stat in stats if stat.has_var("od550aer")]
    pm10sites = [stat.copy() for stat in stats if stat.has_var("concpm10")]
    data["concpm10_X"] = pm10sites
    data["concpm10_X2"] = [stat.copy() for stat in pm10sites[:3]]
    data["concpm10"] = [stat.copy() for stat in pm10sites[:2]]
    return data


@pytest.fixture(scope="session")
def coldata():
    EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS["coldata_tm5_aeronet"])
    return {
        "tm5_aeronet": ColocatedData(str(EXAMPLE_FILE)),
        "fake_nodims": ColocatedData(np.ones((2, 1, 1))),
        "fake_3d": _create_fake_coldata_3d(),
        "fake_4d": _create_fake_coldata_4d(),
        "fake_5d": _create_fake_coldata_5d(),
        "fake_3d_hr": _create_fake_coldata_3d_hourly(),
        "fake_3d_trends": _create_fake_trends_coldata_3d(),
    }


TMPDIR = os.path.join(os.path.expanduser("~"), "tmp", "pyatest")
os.makedirs(TMPDIR, exist_ok=True)

# iris >= 3.2 corrected an error in iris.cube.Cube.intersection
# see https://github.com/metno/pyaerocom/issues/588
iris_version = metadata.version("scitools-iris")
need_iris_32 = pytest.mark.xfail(
    Version(iris_version) < Version("3.2"),
    reason=f"results are different with iris {iris_version} < 3.2",
    strict=True,
)
