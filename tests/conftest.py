import os
from importlib import metadata

import matplotlib
import pytest
from packaging.version import Version

from pyaerocom import const
from pyaerocom.access_testdata import AccessTestData

from .synthetic_data import FakeStationDataAccess

pytest_plugins = [
    "tests.fixtures.emep",
    "tests.fixtures.tm5",
    "tests.fixtures.ebas",
    "tests.fixtures.aeronet",
    "tests.fixtures.stations",
    "tests.fixtures.collocated_data",
]

matplotlib.use("Agg")

TEST_RTOL = 1e-4

FAKE_STATION_DATA = FakeStationDataAccess()

# class that provides / ensures access to testdataset
tda = AccessTestData()

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
def tempdir(tmpdir_factory):
    """Temporary directory for dumping data shared between tests"""
    tmpdir = tmpdir_factory.mktemp("data")
    return tmpdir


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
