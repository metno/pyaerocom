from __future__ import annotations

import logging
import re
from collections.abc import Iterable
from pathlib import Path

import xarray as xr

from pyaerocom import const
from pyaerocom.io.cnemc.reader import ReadCNEMC
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)


class ReadICOS(ReadCNEMC):
    """Class for reading ICOS (CO2) observations. HARP format so based on CNEMC reader

    Args:
        ReadCNEMC (class): Base class for this reader, based on ReadUngriddedBase

    """

    #: Mask for identifying datafiles
    _FILEMASK = "icos-*.nc"

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

    VAR_MAPPING = {
        "vmrco2": "CO2_volume_mixing_ratio",
        "vmrch4": "CH4_volume_mixing_ratio",
        "vmrco": "CO_volume_mixing_ratio",
    }

    FILEMASK_MAPPING = {
        "vmrco2": "icos-co2-*.nc",
        "vmrch4": "icos-ch4-*.nc",
        "vmrco": "icos-co-*.nc",
    }

    STATION_REGEX = re.compile("icos-.*-(.*)-.*-.*.nc")  # co2, ch4, co agnostic

    DEFAULT_VARS = list(VAR_MAPPING)

    DATASET_NAME = DATA_ID

    PROVIDES_VARIABLES = list(VAR_MAPPING) + list(AUX_FUNS)

    def __init__(self, data_id: str | None = None, data_dir: str | None = None):
        if data_dir is None:
            data_dir = const.OBSLOCS_UNGRIDDED[const.ICOS_NAME]

        super().__init__(data_id=data_id, data_dir=data_dir)

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
        var_to_retrieve: str | None = None,
        files: Iterable[str | Path] | None = None,
        first_file: int | None = None,
        last_file: int | None = None,
    ) -> UngriddedData:
        if var_to_retrieve is None:
            var_to_retrieve = self.DEFAULT_VARS[0]

        if isinstance(var_to_retrieve, list):
            var_to_retrieve = var_to_retrieve[0]

        if len([var_to_retrieve]) > 1:
            raise NotImplementedError("Unnskyld, ReadICOS can only read one variable at a time...")

        if unsupported := set([var_to_retrieve]) - set(self.PROVIDES_VARIABLES):
            raise ValueError(f"Unsupported variables: {', '.join(sorted(unsupported))}")

        if files is not None and not isinstance(files, tuple):
            files = tuple(files)

        if files is not None and first_file is not None:
            files = files[first_file:]

        if files is not None and last_file is not None:
            files = files[:last_file]

        if files is None:
            # # Files will depend on the var
            stations: list[StationData] = []
            this_var_files = sorted(
                Path(self.data_dir).rglob(self.FILEMASK_MAPPING[var_to_retrieve])
            )

            for station_name, paths in self.stations(files).items():
                paths_to_read = list(set(paths) & set(this_var_files))
                if not paths_to_read:
                    continue

                logger.debug(f"Reading station {station_name}")
                ds = self._read_dataset(paths_to_read)
                ds = ds.rename({self.VAR_MAPPING[var_to_retrieve]: var_to_retrieve})
                ds = ds.assign(
                    time=self._dataset_time(ds),
                    **{name: func(ds) for name, func in self.AUX_FUNS.items()},
                )
                ds.set_coords(("latitude", "longitude", "altitude"))
                stations.append(self.to_stationdata(ds, station_name))
            return UngriddedData.from_station_data(stations)
        else:
            stations: list[StationData] = []
            this_var_files = sorted(
                Path(self.data_dir).rglob(self.FILEMASK_MAPPING[var_to_retrieve])
            )

            for station_name, paths in self.stations(files).items():
                paths_to_read = list(set(paths) & set(this_var_files))
                if not paths_to_read:
                    continue

                logger.debug(f"Reading station {station_name}")
                ds = self._read_dataset(paths)
                ds = ds.rename({self.VAR_MAPPING[var_to_retrieve]: var_to_retrieve})
                ds = ds.assign(
                    time=self._dataset_time(ds),
                    **{name: func(ds) for name, func in self.AUX_FUNS.items()},
                )
                ds.set_coords(("latitude", "longitude", "altitude"))
                stations.append(self.to_stationdata(ds, station_name))

            return UngriddedData.from_station_data(stations)

    def _read_dataset(self, paths: list[Path]) -> xr.Dataset:
        return xr.open_mfdataset(
            sorted(paths),
            concat_dim="time",
            combine="nested",
            parallel=True,
            decode_cf=True,
            decode_timedelta=True,
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
            if var not in cls.PROVIDES_VARIABLES:
                continue
            station[var] = ds[var].to_series()
            station["var_info"][var] = {"units": ds[var].units}

        return station
