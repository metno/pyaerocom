"""
checks if testdata-minimal is available and if not, tries to download it
automatically into ~/MyPyaerocom/testdata-minimal
"""

from __future__ import annotations

import logging
import tarfile
from pathlib import Path
from typing import NamedTuple, Type

import requests

from pyaerocom import const, io
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

logger = logging.getLogger(__name__)


#: Name of testdata directory
TESTDATA_NAME = "testdata-minimal"

#: That's were the testdata can be downloaded from
TESTDATA_URL = f"https://pyaerocom-ng.met.no/pyaerocom-suppl/{TESTDATA_NAME}.tar.gz.ebas_202201"

#: Directory where testdata will be downloaded into
TESTDATA_ROOT = Path(const.OUTPUTDIR) / TESTDATA_NAME


class TestData(NamedTuple):
    relpath: str
    reader: Type[ReadUngriddedBase] | None = None

    @property
    def path(self) -> Path:
        return TESTDATA_ROOT / self.relpath


TEST_DATA: dict[str, TestData] = {
    "MODELS": TestData("modeldata"),
    "OBSERVATIONS": TestData("obsdata"),
    "CONFIG": TestData("config"),
    "AeronetSunV3L2Subset.daily": TestData(
        "obsdata/AeronetSunV3Lev2.daily/renamed", io.ReadAeronetSunV3
    ),
    "AeronetSunV3L2Subset.AP": TestData(
        "obsdata/AeronetSunV3Lev2.0.AP/renamed", io.ReadAeronetSunV3
    ),
    "AeronetSDAV3L2Subset.daily": TestData(
        "obsdata/AeronetSDAV3Lev2.daily/renamed", io.ReadAeronetSdaV3
    ),
    "AeronetInvV3L2Subset.daily": TestData(
        "obsdata/AeronetInvV3Lev2.daily/renamed", io.ReadAeronetInvV3
    ),
    "EBASSubset": TestData("obsdata/EBASMultiColumn", io.ReadEbas),
    "AirNowSubset": TestData("obsdata/AirNowSubset", io.ReadAirNow),
    "G.EEA.daily.Subset": TestData("obsdata/GHOST/data/EEA_AQ_eReporting/daily", io.ReadGhost),
    "G.EEA.hourly.Subset": TestData("obsdata/GHOST/data/EEA_AQ_eReporting/hourly", io.ReadGhost),
    "G.EBAS.daily.Subset": TestData("obsdata/GHOST/data/EBAS/daily", io.ReadGhost),
    "G.EBAS.hourly.Subset": TestData("obsdata/GHOST/data/EBAS/hourly", io.ReadGhost),
    "EEA_AQeRep.v2.Subset": TestData("obsdata/EEA_AQeRep.v2/renamed", io.ReadEEAAQEREP_V2),
    "Earlinet-test": TestData("obsdata/Earlinet", io.ReadEarlinet),
}


def download() -> bool:
    """
    Download testdata

    Returns
    -------
    bool
        True if download was successful, else False

    """
    path = TESTDATA_ROOT.parent / Path(TESTDATA_URL).name
    logger.info(f"Downloading pyaerocom testdata into {path.parent}")
    path.parent.mkdir(exist_ok=True, parents=True)

    try:
        r = requests.get(TESTDATA_URL)
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.warning(f"Failed to download testdata: {e}", exc_info=True)
        return False
    else:
        path.write_bytes(r.content)

    try:
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(path.parent)
    except tarfile.TarError as e:
        logger.warning(f"Failed to unpack testdata: {e}", exc_info=True)
        return False
    finally:
        path.unlink()

    return True


def check_access() -> bool:
    """
    Method that checks if testdata can be accessed

    See also :func:`check_access_and_download_if_needed`.

    Returns
    -------
    bool
        True if testdata is available and all relevant path locations
        could be validated, else False.

    """
    return all(data.path.is_dir() for data in TEST_DATA.values())


def check_access_and_download_if_needed() -> bool:
    """
    Method that checks if testdata can be accessed and if not downloads it

    Returns
    -------
    bool
        True if testdata is available and all relevant path locations
        could be validated, else False.

    """
    if check_access():
        return True

    if download():
        return check_access()

    return False


def init() -> bool:
    if not check_access_and_download_if_needed():
        return False

    for name, data in TEST_DATA.items():
        if data.reader is None:
            logger.info(f"Adding data search directory {data.path}.")
            const.add_data_search_dir(str(data.path))
            continue

        if const.OBSLOCS_UNGRIDDED.get(name) == str(data.path):
            logger.info(f"dataset {name} is already registered")
            continue

        logger.info(
            f"Adding ungridded dataset {name} located at {data.path}. Reader: {data.reader}"
        )
        try:
            const.add_ungridded_obs(name, str(data.path), reader=data.reader, check_read=False)
        except Exception as e:
            logger.warning(
                f"Failed to instantiate testdata since ungridded "
                f"dataset {name} at {data.path} could not be registered: {e}"
            )
            return False

    return True


assert init(), "cound not find minimal test data"
