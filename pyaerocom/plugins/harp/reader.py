from __future__ import annotations

import logging
import re
import time
from functools import cached_property
from glob import glob
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
    _FILEMASK = "*.nc"

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
    PATTERN = "mep-rd-*.nc"

    def __init__(self, data_id=None, data_dir=None):
        if data_dir is None:
            raise ValueError(
                f"For HARP data_dir needs to be set to the folder where the data is found"
            )
        super().__init__(data_id=data_id, data_dir=data_dir)

        self._found_files = None
        self.FOUND_FILES

    @cached_property
    def FOUND_FILES(self):
        found_files = []
        for file in glob(self.data_dir + "/**/" + self.PATTERN, recursive=True):
            found_files.append(file)

        self._found_files = found_files
        return found_files

    @cached_property
    def STATIONS(self):
        stations = {}
        station_pattern = "mep-rd-(.*A)-.*.nc"
        found_files = self.FOUND_FILES
        for file in found_files:
            filename = Path(file).name
            try:
                stationname = re.search(station_pattern, filename).group(1)
                if stationname not in stations:
                    stations[stationname] = []

                stations[stationname].append(file)
            except:
                print(f"Skipping file {filename}")
                logger.debug(f"Skipping file {filename}")

        return stations

    @property
    def DEFAULT_VARS(self):
        """List of default variables"""
        return list(self.VAR_MAPPING.keys())

    @property
    def DATASET_NAME(self):
        """Name of the dataset"""
        return self.data_id

    @property
    def PROVIDES_VARIABLES(self) -> list[str]:
        return list(self.VAR_MAPPING.keys()) + list(self.AUX_REQUIRES.keys())

    def _get_station_data(self, data: pd.DataFrame) -> StationData:
        sd = StationData()

        return sd

    def _get_stationname(self, filename: str) -> str | None:
        regex = re.compile("MEP-surface-rd-(.*A)-.*.nc")
        if (match := regex.search(filename)) is not None:
            return match.group(1)

        print(f"Skipping file {filename}")
        logger.debug(f"Skipping file {filename}")
        return None

    def _get_time(self, data: xr.Dataset) -> np.ndarray:

        start = np.array(data["datetime_start"])
        end = np.array(data["datetime_stop"])

        return start

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
            times = self._get_time(data)
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

        return UngriddedData.from_station_data(
            stations
        )  # , add_meta_keys=list(set(metadata_headers)))


"""
    def read(
        self, vars_to_retrieve=None, files=None, first_file=None, last_file=None, metadatafile=None
    ):
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS

        for var in vars_to_retrieve:
            if var not in self.PROVIDES_VARIABLES:
                raise ValueError(f"The variable {var} is not supported")

        stations: List[StationData] = []

        for stationname in self.STATIONS:
            f = self.STATIONS[stationname][0]

            data = self.read_file(f, vars_to_retrieve)
            lat = float(data["latitude"][0])
            lon = float(data["longitude"])
            alt = float(data["altitude"])
            station = Station(stationname, lat, lon, alt)
            breakpoint()
            print(f"Reading station {stationname}")
            for f in tqdm(self.STATIONS[stationname]):
                data = self.read_file(f, vars_to_retrieve)

                for s in vars_to_retrieve:
                    try:
                        if s in self.AUX_REQUIRES:
                            read_s = self.AUX_REQUIRES[s][0]
                        else:
                            read_s = s
                        measurements = data[self.VAR_MAPPING[read_s]].data
                        unit = data[self.VAR_MAPPING[read_s]].units
                    except:
                        print(f"Could not find {s} in {f}. Skipping file")
                        logger.info(f"Could not find {s} in {f}. Skipping file")
                        continue

                    time = self._get_time(data)
                    for t, m in zip(time, measurements):
                        if s in self.AUX_REQUIRES:
                            new_m = _conc_to_vmr_single_value(
                                m, self.AUX_REQUIRES[s], self.AUX_UNITS[s], unit
                            )
                            new_unit = self.AUX_UNITS[s]
                            station.add_measurement(s, new_unit, new_m, t)
                        else:
                            station.add_measurement(s, unit, m, t)

            stations.append(
                station.to_stationdata(self.DATA_ID, self.DATASET_NAME, self.STATIONS[stationname])
            )

        return UngriddedData.from_station_data(
            stations
        )  # , add_meta_keys=list(set(metadata_headers)))

"""
