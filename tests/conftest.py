from importlib import metadata

import pytest
from packaging.version import Version

from pyaerocom import const

pytest_plugins = [
    "pyaerocom.fixtures.mscw_ctm",
    "pyaerocom.fixtures.tm5",
    "pyaerocom.fixtures.ebas",
    "pyaerocom.fixtures.aeronet",
    "pyaerocom.fixtures.stations",
    "pyaerocom.fixtures.collocated_data",
    "pyaerocom.fixtures.aeroval.config",
    "pyaerocom.fixtures.pyaro",
]

TEST_RTOL = 1e-4


# skipif marker that is True if no access to metno PPI is provided
# (some tests are skipped in this case)
lustre_unavail = pytest.mark.skipif(
    not const.has_access_lustre,
    reason="Skipping tests that require access to AEROCOM database on METNo servers",
)

lustre_avail = pytest.mark.skipif(
    const.has_access_lustre, reason="Skipping tests that will crash if lustre can be accessed."
)

etopo1_unavail = pytest.mark.skipif(
    not const.ETOPO1_AVAILABLE, reason="Skipping tests that require access to ETOPO1 data"
)


def __package_installed(name: str) -> bool:
    try:
        metadata.version(name)
    except ModuleNotFoundError:
        return False
    return True


geojson_unavail = pytest.mark.xfail(
    not __package_installed("geojsoncontour"),
    reason="geojsoncontour might not be avaiable on a conda environment",
    raises=ModuleNotFoundError,
)

# iris >= 3.2 corrected an error in iris.cube.Cube.intersection
# see https://github.com/metno/pyaerocom/issues/588
iris_version = metadata.version("scitools-iris")
need_iris_32 = pytest.mark.xfail(
    Version(iris_version) < Version("3.2"),
    reason=f"results are different with iris {iris_version} < 3.2",
    strict=True,
)
