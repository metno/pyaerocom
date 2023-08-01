from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property, lru_cache
from pathlib import Path

import xarray as xr

from pyaerocom import const
from pyaerocom.io.readgridded import ReadGriddedBase
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


class ReadTropomiL3(ReadGriddedData):
    """
    Class to read processed TROPOMI data (homebrewed L3 data) for use in SESAM.
    e.g., Tropospheric vertical column of nitrogen dioxide
    """

    _FILEMASK = "S5p_*.nc"
    __version__ = "0.01"

    DATA_ID = ""

    def __init__(self, data_id=None, data_dir=None):
        if data_dir is None:
            raise Exception("Need a data_dir")
        super.__init__(data)
