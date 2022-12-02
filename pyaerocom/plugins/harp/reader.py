from __future__ import annotations

import logging
import re
from collections import defaultdict
from functools import cached_property, lru_cache
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import xarray as xr
from tqdm import tqdm

# from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

from .aux_vars import conc_to_vmr
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
    TS_TYPES_FILE = {"hour": "hourly", "day": "daily"}

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
    AUX_FUNS = {"vmro3": conc_to_vmr, "vmro3max": conc_to_vmr, "vmrno2": conc_to_vmr}

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

        self.files = sorted(map(str, self.FOUND_FILES))

    @cached_property
    def FOUND_FILES(self) -> tuple[Path, ...]:
        paths = sorted(Path(self.data_dir).rglob(self._FILEMASK))
        logger.debug(f"found {len(paths)} files")
        return tuple(paths)

    @lru_cache()
    def stations(self, files: tuple[str | Path, ...] | None = None) -> dict[str, list[Path]]:
        if not files:
            files = self.FOUND_FILES
        stations = defaultdict(list)
        for path in files:
            if not isinstance(path, Path):
                path = Path(path)
            if (name := self._station_name(path)) is None:
                logger.debug(f"Skipping {path.name}")
                continue

            stations[name].append(path)

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

    def read_file(
        self, filename: str | Path, vars_to_retrieve: Iterable[str] | None = None
    ) -> UngriddedData:
        """Reads data for a single year for one component"""
        if not isinstance(filename, Path):
            filename = Path(filename)
        if not filename.is_file():
            raise ValueError(f"missing {filename}")
        return self.read(vars_to_retrieve, (filename,))

    def read(
        self,
        vars_to_retrieve: Iterable[str] | None = None,
        files: Iterable[str | Path] | None = None,
        first_file: int | None = None,
        last_file: int | None = None,
        metadatafile=None,
    ) -> UngriddedData:
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS

        if not set(vars_to_retrieve) <= set(self.PROVIDES_VARIABLES):
            unsupported = set(vars_to_retrieve) - set(self.PROVIDES_VARIABLES)
            raise ValueError(f"Unsupported variables: {', '.join(sorted(unsupported))}")

        if files is not None and not isinstance(files, tuple):
            files = tuple(files)

        if files is not None and first_file is not None:
            files = files[first_file:]

        if files is not None and last_file is not None:
            files = files[:last_file]

        stations: list[StationData] = []

        for name, paths in tqdm(self.stations(files).items()):
            logger.debug(f"Reading station {name}")
            data = xr.open_mfdataset(paths, concat_dim="time", combine="nested", parallel=True)

            lat = float(data["latitude"][0])
            lon = float(data["longitude"][0])
            alt = float(data["altitude"][0])
            station = Station(name, lat, lon, alt)

            times = self._station_time(data)
            for var in vars_to_retrieve:
                if var in self.VAR_MAPPING:
                    aux = self.VAR_MAPPING[var]
                    measurements = data[aux].values
                    unit = data[aux].units
                elif var in self.AUX_REQUIRES:
                    if len(self.AUX_REQUIRES[var]) != 1:
                        raise NotImplementedError(f"Unsupported {self.AUX_REQUIRES[var]}-->{var}")
                    aux = self.AUX_REQUIRES[var][0]
                    aux = self.VAR_MAPPING[aux]
                    measurements = self.AUX_FUNS[var](
                        data[aux].values,
                        self.AUX_REQUIRES[var],
                        self.AUX_UNITS[var],
                        data[aux].units,
                    )
                    unit = self.AUX_UNITS[var]
                else:  # should never get here
                    raise NotImplementedError(f"Unsupported {var}")

                ts = pd.Series(measurements, times)
                station.add_series(var, unit, ts)

            stations.append(station.to_stationdata(self.DATA_ID, self.DATASET_NAME))

        return UngriddedData.from_station_data(stations)
