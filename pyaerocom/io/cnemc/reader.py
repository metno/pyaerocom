from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property, lru_cache
from pathlib import Path

import xarray as xr

from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

from .aux_vars import vmrno2_from_ds, vmro3_from_ds, vmro3max_from_ds

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
    "hourly",
    "daily",
    "monthly",
    "yearly",
}


class ReadCNEMC(ReadUngriddedBase):
    """Class for reading CNEMC observations (formerly MEP and before that MarcoPolo)

    Note
    ----
    Currently only single variable reading into an :class:`UngriddedData`
    object is supported.
    """

    #: Mask for identifying datafiles
    _FILEMASK = "mep-rd-*.nc"

    #: Version log of this class (for caching)
    __version__ = "0.02"

    #: Name of the dataset (OBS_ID)
    DATA_ID = const.CNEMC_NAME

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
    AUX_FUNS = {
        "vmro3": vmro3_from_ds,
        "vmro3max": vmro3max_from_ds,
        "vmrno2": vmrno2_from_ds,
    }

    VAR_MAPPING = {
        "concco": "CO_density",
        "concno2": "NO2_density",
        "conco3": "O3_density",
        "concpm10": "PM10_density",
        "concpm25": "PM2p5_density",
        "concso2": "SO2_density",
    }

    STATION_REGEX = re.compile("mep-rd-(.*A)-.*.nc")

    DEFAULT_VARS = list(VAR_MAPPING)

    DATASET_NAME = DATA_ID

    PROVIDES_VARIABLES = list(VAR_MAPPING) + list(AUX_FUNS)

    def __init__(self, data_id: str | None = None, data_dir: str | None = None):
        if data_dir is None:
            data_dir = const.OBSLOCS_UNGRIDDED[const.CNEMC_NAME]

        super().__init__(data_id=data_id, data_dir=data_dir)
        self.files = sorted(map(str, self.FOUND_FILES))

    @cached_property
    def FOUND_FILES(self) -> tuple[Path, ...]:
        paths = sorted(Path(self.data_dir).rglob(self._FILEMASK))
        logger.debug(f"found {len(paths)} files")
        return tuple(paths)

    @lru_cache
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

        logger.debug(f"found {len(stations)} stations")
        return stations

    @classmethod
    def _station_name(cls, path: Path) -> str | None:
        match = cls.STATION_REGEX.search(path.name)
        return match.group(1) if match else None

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

        if unsupported := set(vars_to_retrieve) - set(self.PROVIDES_VARIABLES):
            raise ValueError(f"Unsupported variables: {', '.join(sorted(unsupported))}")

        if files is not None and not isinstance(files, tuple):
            files = tuple(files)

        if files is not None and first_file is not None:
            files = files[first_file:]

        if files is not None and last_file is not None:
            files = files[:last_file]

        stations: list[StationData] = []

        for station_name, paths in self.stations(files).items():
            logger.debug(f"Reading station {station_name}")
            ds = self._read_dataset(paths)[vars_to_retrieve]
            stations.append(self.to_stationdata(ds, station_name))

        return UngriddedData.from_station_data(stations)

    def _read_dataset(self, paths: list[Path]) -> xr.Dataset:
        ds = xr.open_mfdataset(
            sorted(paths),
            concat_dim="time",
            combine="nested",
            parallel=True,
            decode_cf=True,
            decode_timedelta=True,
        )
        ds = ds.rename({v: k for k, v in self.VAR_MAPPING.items()})
        ds = ds.assign(
            time=self._dataset_time(ds),
            **{name: func(ds) for name, func in self.AUX_FUNS.items()},
        )
        return ds.set_coords(("latitude", "longitude", "altitude"))

    @classmethod
    def _dataset_time(cls, ds: xr.Dataset) -> xr.DataArray:
        # can not add ds["datetime_start"] and ds["datetime_start"], as both are of type datetime[ns]
        time = ds[cls.START_TIME_NAME] + (ds[cls.END_TIME_NAME] - ds[cls.START_TIME_NAME]) / 2
        return xr.Variable(
            "time",
            time,
            dict(
                long_name="time at middle of the period",
                units=ds[cls.START_TIME_NAME].encoding["units"],
            ),
            ds[cls.START_TIME_NAME].encoding,
        )

    @classmethod
    def to_stationdata(cls, ds: xr.Dataset, station_name: str) -> StationData:
        station = StationData()
        station.data_id = cls.DATA_ID
        station.dataset_name = cls.DATASET_NAME
        station.station_id = station_name
        station.station_name = station_name
        station.latitude = float(ds["latitude"][0])
        station.longitude = float(ds["longitude"][0])
        station.altitude = float(ds["altitude"][0])

        station.station_coords = {
            "latitude": station.latitude,
            "longitude": station.longitude,
            "altitude": station.altitude,
        }

        station.ts_type = "hourly"
        station["dtime"] = ds["time"].values

        for var in ds.data_vars:
            station[var] = ds[var].to_series()
            station["var_info"][var] = {"units": ds[var].units}

        return station
