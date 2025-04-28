"""
checks if testdata-minimal is available and if not, tries to download it
automatically into ~/MyPyaerocom/testdata-minimal
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import NamedTuple


from pyaerocom import const, io
from pyaerocom.io.ghost.reader import ReadGhost
from pyaerocom.io.icpforests.reader import ReadICPForest
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

logger = logging.getLogger(__name__)

from pyaerocom import download_minimal_dataset
from pyaerocom.sample_data_access.minimal_dataset import minimal_dataset


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
    "ICPFORESTS.Subset": DataForTests("obsdata/ipc-forests/dep", ReadICPForest),
    "EEA_AQeRep.v2.Subset": DataForTests("obsdata/EEA_AQeRep.v2/renamed", io.ReadEEAAQEREP_V2),
    "Earlinet-test": DataForTests("obsdata/Earlinet", io.ReadEarlinet),
    "Eprofile-test": DataForTests("obsdata/EPROFILE", io.ReadEprofile),
}


def init() -> bool:
    download_minimal_dataset()

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
