from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property, lru_cache
from pathlib import Path

import xarray as xr

from pyaerocom import const
from pyaerocom.plugins.mep.reader import ReadMEP


class ReadICOS(ReadMEP):
    """Class for reading ICOS (CO2) observations. HARP format so based on MEP reader

    Args:
        ReadMEP (class): Base class for this reader, based on ReadUngriddedBase

    """

    #: Mask for identifying datafiles
    _FILEMASK = "icos-co2-*.nc"

    #: Version log of this class (for caching)
    __version__ = "0.01"

    #: Name of the dataset (OBS_ID)
    DATA_ID = const.ICOS_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: There is no global ts_type but it is specified in the data files...
    TS_TYPE = "variable"

    #: sampling frequencies found in data files
    TS_TYPES_FILE = {"hour": "hourly", "day": "daily"}

    #: field name of the start time of the measurement (in lower case)
    START_TIME_NAME = "datetime_start"

    #: filed name of the end time of the measurement (in lower case)
    END_TIME_NAME = "datetime_stop"

    #: there's no general instrument name in the data
    INSTRUMENT_NAME = "unknown"

    DATA_PRODUCT = ""

    #: functions used to convert variables that are computed
    AUX_FUNS = {}

    VAR_MAPPING = {"vmrco2": "CO2_volume_mixing_ratio"}

    # STATION_REGEX = re.compile("icos-co2-nrt-(.*)-.*-.*-.*.nc")
    STATION_REGEX = re.compile("icos-co2-(.*A)-.*.nc")

    DEFAULT_VARS = list(VAR_MAPPING)

    DATASET_NAME = DATA_ID

    PROVIDES_VARIABLES = list(VAR_MAPPING) + list(AUX_FUNS)

    def __init__(self, data_id=None, data_dir=None):
        breakpoint()
        if data_dir is None:
            data_dir = const.OBSLOCS_UNGRIDDED[const.ICOS_NAME]

        super().__init__(data_id=data_id, data_dir=data_dir)
        self.files = sorted(map(str, self.FOUND_FILES))
