from __future__ import annotations

import logging
import re
import time
from collections import defaultdict
from functools import cached_property
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

# from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

from .aux_vars import _conc_to_vmr, _conc_to_vmr_marcopolo_stats, _conc_to_vmr_single_value
from .station import Station

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
METADATA_INDEX_START = 11
ALLOWED_FREQS = {
    "minutly",
    "hourly",
    "daily",
    "monthly",
    "yearly",
}


class ReadHARP(ReadUngriddedBase):
    """Class for reading MiniCOD data

    Extended class derived from  low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality.

    Note
    ----
    Currently only single variable reading into an :class:`UngriddedData`
    object is supported.
    """

    #: Mask for identifying datafiles
    _FILEMASK = "mep-rd-*.nc"

    #: Version log of this class (for caching)
    __version__ = "0.01"

    #: Name of the dataset (OBS_ID)
    DATA_ID = "HARP"  # change this since we added more vars?

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: There is no global ts_type but it is specified in the data files...
    TS_TYPE = "variable"

    #: sampling frequencies found in data files
    TS_TYPES_FILE = {
        "hour": "hourly",
        "day": "daily",
    }

    #: field name of the start time of the measurement (in lower case)
    START_TIME_NAME = "datetime_start"

    #: filed name of the end time of the measurement (in lower case)
    END_TIME_NAME = "datetime_stop"

    #: column name that holds the EEA variable code
    VAR_CODE_NAME = "airpollutantcode"

    #: there's no general instrument name in the data
    INSTRUMENT_NAME = "unknown"

    DATA_PRODUCT = ""

    #: Variables that are computed (cannot be read directly)
    AUX_REQUIRES = {"vmro3": ["conco3"], "vmro3max": ["conco3"], "vmrno2": ["concno2"]}

    #: functions used to convert variables that are computed
    AUX_FUNS = {
        "vmro3": _conc_to_vmr_single_value,
        "vmro3max": _conc_to_vmr_single_value,
        "vmrno2": _conc_to_vmr_single_value,
    }

    #: units of computed variables
    AUX_UNITS = {"vmro3": "ppb", "vmro3max": "ppb", "vmrno2": "ppb"}

    VAR_MAPPING = {
        "concco": "CO_density",
        "concno2": "NO2_density",
        "conco3": "O3_density",
        "concpm10": "PM10_density",
        "concpm25": "PM2p5_density",
        "concso2": "SO2_density",
    }

    STATION_REGEX = re.compile("mep-rd-(.*A)-.*.nc")

    def __init__(self, data_id=None, data_dir=None):
        if data_dir is None:
            raise ValueError(
                f"For HARP data_dir needs to be set to the folder where the data is found"
            )
        super().__init__(data_id=data_id, data_dir=data_dir)

    @cached_property
    def FOUND_FILES(self) -> list[Path]:
        paths = sorted(Path(self.data_dir).rglob(self._FILEMASK))
        logger.debug(f"found {len(paths)} files")
        return paths

    @cached_property
    def STATIONS(self) -> dict[str, list[str]]:
        stations = defaultdict(list)
        for path in self.FOUND_FILES:
            if (name := self._station_name(path)) is None:
                logger.debug(f"Skipping {path.name}")
                continue

            stations[name].append(str(path))

        return stations

    @classmethod
    def _station_name(cls, path: Path) -> str | None:
        match = cls.STATION_REGEX.search(path.name)
        return match.group(1) if match else None

    @property
    def DEFAULT_VARS(self) -> list[str]:
        """List of default variables"""
        return list(self.VAR_MAPPING)

    @property
    def DATASET_NAME(self) -> str:
        """Name of the dataset"""
        assert self.data_id is not None, f"missing {self}.data_id"
        return str(self.data_id)

    @property
    def PROVIDES_VARIABLES(self) -> list[str]:
        return list(self.VAR_MAPPING) + list(self.AUX_REQUIRES)

    @classmethod
    def _station_time(cls, data: xr.Dataset) -> np.ndarray:
        return data[cls.START_TIME_NAME].values

    def read_file(self, filename: str, vars_to_retrieve: list[str]) -> xr.Dataset:
        """Reads data for a single year for one component"""
        return xr.open_dataset(filename)

    def read(
        self, vars_to_retrieve=None, files=None, first_file=None, last_file=None, metadatafile=None
    ):
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS

        for var in vars_to_retrieve:
            if var not in self.PROVIDES_VARIABLES:
                raise ValueError(f"The variable {var} is not supported")

        stations: list[StationData] = []

        for stationname in tqdm(self.STATIONS):
            print(f"Reading station {stationname}")
            start_time = time.time()
            data = xr.open_mfdataset(
                self.STATIONS[stationname],
                concat_dim="time",
                combine="nested",
                parallel=True,
                autoclose=True,
            )
            print(f"After reading df {time.time()-start_time}")
            lat = float(data["latitude"][0])
            lon = float(data["longitude"][0])
            alt = float(data["altitude"][0])
            station = Station(stationname, lat, lon, alt)
            print(f"After making Station {time.time()-start_time}")
            times = self._station_time(data)
            print(f"After getting times {time.time()-start_time}")
            for s in vars_to_retrieve:
                if s in self.AUX_REQUIRES:
                    read_s = self.AUX_REQUIRES[s][0]
                else:
                    read_s = s
                measurements = np.array(data[self.VAR_MAPPING[read_s]])
                unit = data[self.VAR_MAPPING[read_s]].units

                if s in self.AUX_REQUIRES:
                    measurements = _conc_to_vmr(
                        measurements, self.AUX_REQUIRES[s], self.AUX_UNITS[s], unit
                    )
                    unit = self.AUX_UNITS[s]

                ts = pd.Series(measurements, times)
                station.add_series(s, unit, ts)
            print(f"After creating series {time.time()-start_time}")
            stations.append(
                station.to_stationdata(self.DATA_ID, self.DATASET_NAME, self.STATIONS[stationname])
            )

        return UngriddedData.from_station_data(stations)
