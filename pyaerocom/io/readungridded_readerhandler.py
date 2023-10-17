import sys
import logging
import os

import warnings
from pathlib import Path
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
from pyaerocom import const

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
        data_ids: Optional[list[str]] = None,
        data_dirs: Optional[dict[str, str]] = None,
        pyaro_config: Optional[dict[str, str]] = None,
    ) -> None:
        self.data_ids = data_ids
        self._data_dirs = data_dirs

        self.config = pyaro_config

        self._readers = {}

    def _set_reader_type(self):
        ...

    def dataset_provides_variables(self, data_id=None):
        """List of variables provided by a certain dataset"""
        if data_id is None:
            data_id = self.data_id
        if not data_id in self._readers:
            reader = self.get_lowlevel_reader(data_id)
        else:
            reader = self._readers[data_id]
        return reader.PROVIDES_VARIABLES

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
        for _cls in self.SUPPORTED_READERS_PYAEROCOM:
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

    @property
    def post_compute(self):
        """Information about datasets that can be computed in post"""
        return const.OBS_UNGRIDDED_POST

    @property
    def SUPPORTED_DATASETS(self):
        """
        Returns list of strings containing all supported dataset names
        """
        lst = []
        for reader in self.SUPPORTED_READERS_PYAEROCOM:
            lst.extend(reader.SUPPORTED_DATASETS)
        lst.extend(self.post_compute)
        return lst

    @property
    def supported_datasets(self):
        """
        Wrapper for :attr:`SUPPORTED_DATASETS`
        """
        return self.SUPPORTED_DATASETS

    @property
    def data_dirs(self):
        """
        dict: Data directory(ies) for dataset(s) to read (keys are data IDs)
        """
        return self._data_dirs

    @data_dirs.setter
    def data_dirs(self, val):
        if isinstance(val, Path):
            val = str(val)
        dsr = self.data_ids
        if len(dsr) < 2 and isinstance(val, str):
            val = {dsr[0]: val}
        elif not isinstance(val, dict):
            raise ValueError(f"Invalid input for data_dirs ({val}); needs to be a dictionary.")
        for data_dir in val.values():
            assert os.path.exists(data_dir), f"{data_dir} does not exist"
        self._data_dirs = val
