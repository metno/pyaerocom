import sys
import logging
from typing import Optional

if sys.version_info >= (3, 10):  # pragma: no cover
    from importlib import metadata
else:  # pragma: no cover
    import importlib_metadata as metadata

from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.io.read_aeronet_invv2 import ReadAeronetInvV2
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_airnow import ReadAirNow
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom.io.read_ebas import ReadEbas
from pyaerocom.io.read_eea_aqerep import ReadEEAAQEREP
from pyaerocom.io.read_eea_aqerep_v2 import ReadEEAAQEREP_V2
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.exceptions import DataRetrievalError, NetworkNotImplemented, NetworkNotSupported

logger = logging.getLogger(__name__)


class ReaderHandler:
    SUPPORTED_READERS_PYAEROCOM = [
        ReadAeronetInvV3,
        ReadAeronetInvV2,
        ReadAeronetSdaV2,
        ReadAeronetSdaV3,
        ReadAeronetSunV2,
        ReadAeronetSunV3,
        ReadEarlinet,
        ReadEbas,
        ReadAasEtal,
        ReadAirNow,
        ReadEEAAQEREP,
        ReadEEAAQEREP_V2,
    ]
    SUPPORTED_READERS_PYAEROCOM.extend(
        ep.load() for ep in metadata.entry_points(group="pyaerocom.ungridded")
    )

    def __init__(
        self,
        data_id: Optional[str] = None,
    ) -> None:
        pass

    def get_lowlevel_reader(self, data_id=None):
        """Helper method that returns initiated reader class for input ID

        Parameters
        -----------
        data_id : str
            Name of dataset

        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base
            class :class:`ReadUngriddedBase`).
        """
        if data_id is None:
            if len(self.data_ids) != 1:
                raise ValueError("Please specify dataset")
        if not data_id in self.supported_datasets:
            raise NetworkNotSupported(
                f"Could not fetch reader class: Input "
                f"network {data_id} is not supported by "
                f"ReadUngridded"
            )
        elif not data_id in self.data_ids:
            self.data_ids.append(data_id)

        if not data_id in self._readers:
            _cls = self._find_read_class(data_id)
            reader = self._init_lowlevel_reader(_cls, data_id)
            self._readers[data_id] = reader
        return self._readers[data_id]

    def _find_read_class(self, data_id):
        """Find reading class for dataset name

        Loops over all reading classes available in :attr:`SUPPORTED_READERS`
        and finds the first one that matches the input dataset name, by
        checking the attribute :attr:`SUPPORTED_DATASETS` in each respective
        reading class.

        Parameters
        -----------
        data_id : str
            Name of dataset

        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base
            class :class:`ReadUngriddedBase`)

        Raises
        ------
        NetworkNotImplemented
            if network is supported but no reading routine is implemented yet

        """
        for _cls in self.SUPPORTED_READERS:
            if data_id in _cls.SUPPORTED_DATASETS:
                return _cls
        raise NetworkNotImplemented(f"Could not find reading class for dataset {data_id}")

    def _init_lowlevel_reader(self, reader, data_id):
        """
        Initiate lowlevel reader for input data ID

        Parameters
        ----------
        reader
            reader class (not instantiated)
        data_id : str
            ID of dataset to be isntantiated with input reader

        Returns
        -------
        ReadUngriddedBase
            instantiated reader class for input ID.

        """
        if data_id in self.data_dirs:
            ddir = self.data_dirs[data_id]
            logger.info(f"Reading {data_id} from specified data loaction: {ddir}")
        else:
            ddir = None
        return reader(data_id=data_id, data_dir=ddir)
