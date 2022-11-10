import logging
import re
from datetime import datetime
from functools import cached_property
from glob import glob
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

# from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.plugins.harp.station import Station
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)

COLUMNS = "country, stationname, stationcode, latitude, longitude, altitude, timestamp, pollutant, unit, frequency, value".split(
    ","
)


METADATA_INDEX_START = 11


ALLOWED_FREQS = {
    "minutly",
    "hourly",
    "daily",
    "monthly",
    "yearly",
}

FILE_DIR = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/CHINA_MP_NRT/HARP_EXAMPLE_DATA/download/JJA-2022/HARP2/nobackup/users/tsikerde/China_grounddata/HARP/"


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
    START_TIME_NAME = "datetimebegin"

    #: filed name of the end time of the measurement (in lower case)
    END_TIME_NAME = "datetimeend"

    #: column name that holds the EEA variable code
    VAR_CODE_NAME = "airpollutantcode"

    #: there's no general instrument name in the data
    INSTRUMENT_NAME = "unknown"

    DATA_PRODUCT = ""

    VAR_MAPPING = {
        "concco": "CO_density",
        "concno2": "NO2_density",
        "conco3": "O3_density",
        "concpm10": "PM10_density",
        "concpm25": "PM2p5_density",
        "concso2": "SO2_density",
    }
    PATTERN = "MEP-surface-rd-*.nc"

    def __init__(self, data_id=None, data_dir=None):
        if data_dir is None:
            raise ValueError(
                f"For MiniCOD data_dir needs to be set to the folder where the data is found"
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
        station_pattern = "MEP-surface-rd-(.*A)-.*.nc"
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
        return ["conco3"]

    @property
    def DATASET_NAME(self):
        """Name of the dataset"""
        return self.data_id

    @property
    def PROVIDES_VARIABLES(self) -> List[str]:
        return list(self.VAR_MAPPING.keys())

    def _get_station_data(self, data: pd.DataFrame) -> StationData:
        sd = StationData()

        return sd

    def _get_stationname(self, filename: str) -> str | None:
        station_pattern = "MEP-surface-rd-(.*A)-.*.nc"
        try:
            stationname = re.search(station_pattern, filename).group(1)
            return stationname

        except:
            print(f"Skipping file {filename}")
            logger.debug(f"Skipping file {filename}")
            return None

    def _get_time(self, data: xr.Dataset) -> List[np.datetime64]:

        start = data["datetime_start"].data
        end = data["datetime_stop"].data

        return list(start)

    def read_file(self, filename: str, vars_to_retrieve: List[str]) -> xr.Dataset:
        """Reads data for a single year for one component"""
        return xr.open_dataset(filename)

    def read(
        self, vars_to_retrieve=None, files=None, first_file=None, last_file=None, metadatafile=None
    ):
        if vars_to_retrieve is None:
            vars_to_retrieve = self.PROVIDES_VARIABLES

        for var in vars_to_retrieve:
            if var not in self.PROVIDES_VARIABLES:
                raise ValueError(f"The variable {var} is not supported")

        stations: List[Station] = []

        for stationname in tqdm(self.STATIONS):
            f = self.STATIONS[stationname][0]

            data = self.read_file(f, vars_to_retrieve)
            lat = float(data["latitude"])
            lon = float(data["longitude"])
            alt = float(data["altitude"])
            station = Station(stationname, lat, lon, alt)

            for f in self.STATIONS[stationname]:

                for s in vars_to_retrieve:
                    try:
                        measurements = data[self.VAR_MAPPING[s]].data
                        unit = data[self.VAR_MAPPING[s]].units
                    except:
                        print(f"Could not find {s} in {f}. Skipping file")
                        logger.info(f"Could not find {s} in {f}. Skipping file")
                        continue

                    time = self._get_time(data)
                    for t, m in zip(time, measurements):
                        station.add_measurement(s, unit, m, t)

            stations.append(
                station.to_stationdata(self.DATA_ID, self.DATASET_NAME, self.STATIONS[stationname])
            )

        return UngriddedData.from_station_data(
            stations
        )  # , add_meta_keys=list(set(metadata_headers)))


if __name__ == "__main__":
    FILE_DIR = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/CHINA_MP_NRT/HARP_EXAMPLE_DATA/download/JJA-2022/HARP2/nobackup/users/tsikerde/China_grounddata/HARP/"
    reader = ReadHARP(data_dir=FILE_DIR)
    data = reader.read()

    breakpoint()
