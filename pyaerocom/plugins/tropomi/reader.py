from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property, lru_cache
from pathlib import Path

import xarray as xr

from pyaerocom import const
from pyaerocom.io.readgridded import ReadGridded
from pyaerocom.stationdata import StationData
from pyaerocom.griddeddata import GriddedData

logger = logging.getLogger(__name__)

COLUMNS = (
    "country",
    "stationname",
    "stationcode",
    "latitude",
    "longitude",
    "altitude",
    "timestamp",
    "pollutant",
    "unit",
    "frequency",
    "value",
)

TMP_DATA_DIR = "/lustre/storeB/project/fou/kl/sesam/archive/CSO-gridded/xEMEP__r01x01__qa08/NO2/2022/10/"


class ReadTropomiL3(ReadGridded):
    """
    Class to read processed TROPOMI data (homebrewed L3 data) for use in SESAM.
    e.g., Tropospheric vertical column of nitrogen dioxide
    """

    _FILEMASK = "CSO_output_*_gridded.nc"
    __version__ = "0.01"

    DATA_ID = const.TROPOMI_NAME

    def __init__(self, data_id=None, data_dir=None):
        if data_dir is None:
            data_dir = TMP_DATA_DIR
        breakpoint()
        # raise Exception("Need a data_dir")
        super().__init__(data_dir=data_dir, file_convention="cso")
        breakpoint()
