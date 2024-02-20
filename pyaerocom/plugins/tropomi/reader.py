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

# LB: Might not even need
class ReadTropomi_XEMEP_R01x01(ReadGridded):
    """
    Class to read processed TROPOMI data (homebrewed L3 data) for use in SESAM.
    e.g., Tropospheric vertical column of nitrogen dioxide
    """

    _FILEMASK = ""
    __version__ = "0.01"

    DATA_ID = "TROPOMI_XEMEP_R01x01"
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.TROPOMI_XEMEP_R01x01_NAME]

    TS_TYPE = "daily"

    def __init__(self, data_id: str = DATA_ID, data_dir: Path[str] = None):
        if data_dir is None:
            data_dir = const.OBSLOCS_UNGRIDDED[const.TROPOMI_XEMEP_R01x01_NAME]
        # raise Exception("Need a data_dir")
        super().__init__(data_id=data_id, data_dir=data_dir, file_convention="aerocom3")


    # # LB: testing if can hack together for both obs and model reader
    # def has_var(self, var_name):
    #     """Check if variable is supported

    #     Parameters
    #     ----------
    #     var_name : str
    #         variable to be checked

    #     Returns
    #     -------
    #     bool
    #     """
    #     breakpoint()
    #     avail = self.vars_provided
    #     if var_name in avail or const.VARS[var_name].var_name_aerocom in avail:
    #         return True
    #     return False