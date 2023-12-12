"""
checks if testdata-minimal is available and if not, tries to download it
automatically into ~/MyPyaerocom/testdata-minimal
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import NamedTuple

import pooch

from pyaerocom import const, io
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.plugins.ghost.reader import ReadGhost
from pyaerocom.plugins.ipcforests.reader import ReadIPCForest

logger = logging.getLogger(__name__)

#: tarfile to download
TESTATA_FILE = "testdata-minimal.tar.gz.20231116"

minimal_dataset = pooch.create(
    path=const.OUTPUTDIR,  # ~/MyPyaerocom/
    base_url="https://pyaerocom-ng.met.no/pyaerocom-suppl",
    registry={
        "testdata-minimal.tar.gz.20220602": "md5:5d4c6455089bc93fff1fc5e2612cf439",
        "testdata-minimal.tar.gz.20220707": "md5:86fc5cb31e8123b96ef01d44fbe93c52",
        "testdata-minimal.tar.gz.20230919": "md5:7b4c55d5258da7a2b41a3a085b947fba",
        "testdata-minimal.tar.gz.20231013": "md5:f3e311c28e341a5c54d5bbba6f9849d2",
        "testdata-minimal.tar.gz.20231017": "md5:705d91e01ca7647b4c93dfe67def661f",
        "testdata-minimal.tar.gz.20231019": "md5:f8912ee83d6749fb2a9b1eda1d664ca2",
        "testdata-minimal.tar.gz.20231116": "md5:5da747f6596817295ba7affe3402b722",
    },
)


def download(file_name: str = TESTATA_FILE):
    """download tar file to ~/MyPyaerocom/ unpack cointents into ~/MyPyaerocom/testdata-minimal/"""
    logger.debug(f"fetch {file_name} to {minimal_dataset.path}")
    minimal_dataset.fetch(file_name, processor=pooch.Untar(["testdata-minimal"], extract_dir="./"))


class DataForTests(NamedTuple):
    relpath: str
    reader: type[ReadUngriddedBase] | None = None

    @property
    def path(self) -> Path:
        return minimal_dataset.path / "testdata-minimal" / self.relpath

    def register_ungridded(self, name: str):
        if self.reader is None:
            logger.info(f"Adding data search directory {self.path}")
            const.add_data_search_dir(str(self.path))
            return

        if const.OBSLOCS_UNGRIDDED.get(name) == str(self.path):
            logger.info(f"Ungridded dataset {name} is already registered")
            return

        logger.info(f"Register ungridded dataset {name}:  path={self.path} reader={self.reader}")
        const.add_ungridded_obs(name, str(self.path), reader=self.reader, check_read=False)


TEST_DATA: dict[str, DataForTests] = {
    "MODELS": DataForTests("modeldata"),
    "OBSERVATIONS": DataForTests("obsdata"),
    "CONFIG": DataForTests("config"),
    "AeronetSunV3L2Subset.daily": DataForTests(
        "obsdata/AeronetSunV3Lev2.daily/renamed", io.ReadAeronetSunV3
    ),
    "AeronetSunV3L2Subset.AP": DataForTests(
        "obsdata/AeronetSunV3Lev2.0.AP/renamed", io.ReadAeronetSunV3
    ),
    "AeronetSDAV3L2Subset.daily": DataForTests(
        "obsdata/AeronetSDAV3Lev2.daily/renamed", io.ReadAeronetSdaV3
    ),
    "AeronetInvV3L2Subset.daily": DataForTests(
        "obsdata/AeronetInvV3Lev2.daily/renamed", io.ReadAeronetInvV3
    ),
    "EBASSubset": DataForTests("obsdata/EBASMultiColumn", io.ReadEbas),
    "AirNowSubset": DataForTests("obsdata/AirNowSubset", io.ReadAirNow),
    "G.EEA.daily.Subset": DataForTests("obsdata/GHOST/data/EEA_AQ_eReporting/daily", ReadGhost),
    "G.EEA.hourly.Subset": DataForTests("obsdata/GHOST/data/EEA_AQ_eReporting/hourly", ReadGhost),
    "G.EBAS.daily.Subset": DataForTests("obsdata/GHOST/data/EBAS/daily", ReadGhost),
    "G.EBAS.hourly.Subset": DataForTests("obsdata/GHOST/data/EBAS/hourly", ReadGhost),
    "IPCFORESTS.Subset": DataForTests("obsdata/ipc-forests/dep", ReadIPCForest),
    "EEA_AQeRep.v2.Subset": DataForTests("obsdata/EEA_AQeRep.v2/renamed", io.ReadEEAAQEREP_V2),
    "Earlinet-test": DataForTests("obsdata/Earlinet", io.ReadEarlinet),
}


def init() -> bool:
    download()

    for name, data in TEST_DATA.items():
        assert data.path.is_dir(), f"missing dataset {name=}"
        try:
            data.register_ungridded(name)
        except Exception as e:
            logger.warning(
                f"Failed to instantiate testdata since ungridded "
                f"dataset {name} at {data.path} could not be registered: {e}"
            )
            return False

    return True


assert init(), "cound not find minimal test data"
