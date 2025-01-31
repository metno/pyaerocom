from __future__ import annotations

import logging
from typing import TypeVar, Generic
import functools
from collections import defaultdict

import numpy as np
import numpy.typing as npt
from pyaro import list_timeseries_engines, open_timeseries
from pyaro.timeseries import Data, Reader, Station
from pyaro.timeseries.Wrappers import VariableNameChangingReader

from pyaerocom.io.pyaro.pyaro_config import PyaroConfig
from pyaerocom.io.pyaro.postprocess import PostProcessingReader
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.tstype import TsType
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)


class ReadPyaro(ReadUngriddedBase):
    __version__ = "1.1.0"

    SUPPORTED_DATASETS = list(list_timeseries_engines().keys())

    def __init__(self, config: PyaroConfig) -> None:
        self.config: PyaroConfig = config

        self._check_id()

        self.converter = PyaroToUngriddedData(self.config)
        self.reader = self.converter.reader
        self._data_dir = self.config.filename_or_obj_or_url
        self._data_name = self.config.name
        self._data_id = self.config.name

    """
    Definition of abstract methods from ReadUngriddedBase
    """

    @property
    def DATA_ID(self):
        return self._data_name

    @property
    def PROVIDES_VARIABLES(self):
        """
        return self.reader.get_variables()
        """
        return self.reader.variables()

    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    @property
    def TS_TYPE(self):
        """
        To be provided by the reader or engine
        """
        return "undefined"

    @property
    def _FILEMASK(self):
        return self.config.filename_or_obj_or_url

    @staticmethod
    def get_pyaro_readers():
        return list_timeseries_engines()

    def read(self, vars_to_retrieve=None, files=..., first_file=None, last_file=None):
        return self.converter.read(vars_to_retrieve=vars_to_retrieve)

    def read_file(self, filename, vars_to_retrieve=None):
        return self.converter.read(vars_to_retrieve)

    def _check_id(self):
        avail_readers = list_timeseries_engines()
        if self.config.reader_id not in avail_readers:
            logger.warning(
                f"Could not find {self.config.reader_id} in list of available Pyaro readers: {avail_readers}"
            )


def _calculate_ts_type(
    start: npt.NDArray[np.datetime64], end: npt.NDArray[np.datetime64]
) -> npt.NDArray[TsType]:
    seconds = (end - start).astype("timedelta64[s]").astype(np.int32)

    @np.vectorize(otypes=[TsType])
    @functools.lru_cache(maxsize=128)
    def memoized_ts_type(x: np.int32) -> TsType:
        if x == 0:
            return TsType("hourly")
        return TsType.from_total_seconds(x)

    return memoized_ts_type(seconds)


class PyaroToUngriddedData:
    def __init__(self, config: PyaroConfig) -> None:
        self.data: UngriddedData = UngriddedData()
        self.config = config
        self.reader: Reader = self._open_reader()

    def _open_reader(self) -> Reader:
        reader_id = self.config.reader_id
        if self.config.model_extra is not None:
            kwargs = self.config.model_extra
        else:
            kwargs = {}

        reader = open_timeseries(
            reader_id,
            self.config.filename_or_obj_or_url,
            filters=self.config.filters,
            **kwargs,
        )
        if self.config.name_map is not None:
            reader = VariableNameChangingReader(
                reader,
                self.config.name_map,
            )
        if self.config.post_processing is not None:
            reader = PostProcessingReader(
                reader,
                self.config.post_processing,
            )
        return reader

    def _convert_to_ungriddeddata(self, pyaro_data: dict[str, Data]) -> UngriddedData:
        total_size = sum(len(var) for var in pyaro_data.values())

        COLNO = 12
        outarray = np.nan * np.ones((total_size, COLNO), dtype=float, order="F")

        T = TypeVar("T")

        class UniqueMapper(Generic[T]):
            """Assign a unique ID to each item it has
            not seen before
            """

            def __init__(self):
                self.inner: dict[T, float] = dict()
                self._idx: float = 0.0

            def index_and_insert_if_not(self, item: T) -> float:
                index = self.inner.get(item)
                if index is not None:
                    return index
                index = self._idx
                self._idx += 1.0

                self.inner[item] = index
                return index

            def __getitem__(self, key: T) -> float:
                return self.inner[key]

        # unique in (station_name, variable_name, units, tstype)
        station_mapper: UniqueMapper[tuple[str, str, str, str]] = UniqueMapper()
        var_mapper: UniqueMapper[str] = UniqueMapper()

        stations_with_metadata = self.get_stations()

        current_offset = 0
        for var, var_data in pyaro_data.items():
            next_offset = current_offset + len(var_data)
            idx = slice(current_offset, next_offset)
            current_offset = next_offset

            var_key = var_mapper.index_and_insert_if_not(var)

            tstype = _calculate_ts_type(var_data.start_times, var_data.end_times)
            stations = var_data.stations
            units = var_data.units
            # Find unique pairs of (station, var, TsType)
            station_key = [
                station_mapper.index_and_insert_if_not((s, var, units, str(t)))
                for (s, t) in zip(stations, tstype)
            ]

            outarray[idx, UngriddedData._METADATAKEYINDEX] = station_key
            # midtime = var_data.start_times + (var_data.end_times - var_data.start_times)/2
            # outarray[idx, UngriddedData._TIMEINDEX] = midtime.astype("datetime64[s]")
            outarray[idx, UngriddedData._TIMEINDEX] = var_data.start_times.astype("datetime64[s]")
            outarray[idx, UngriddedData._LATINDEX] = var_data.latitudes
            outarray[idx, UngriddedData._LONINDEX] = var_data.longitudes
            outarray[idx, UngriddedData._ALTITUDEINDEX] = var_data.altitudes
            outarray[idx, UngriddedData._VARINDEX] = var_key
            outarray[idx, UngriddedData._DATAINDEX] = var_data.values
            # outarray[idx, UngriddedData._DATAHEIGHTINDEX] = ?? Unused ??
            outarray[idx, UngriddedData._DATAERRINDEX] = var_data.standard_deviations
            outarray[idx, UngriddedData._DATAFLAGINDEX] = var_data.flags  # Only counts if non-NaN?
            # outarray[idx, UngriddedData._STOPTIMEINDEX] = var_data.end_times # Seems unused?
            # outarray[idx, UngriddedData._TRASHINDEX]  # No need to set, only non-NaN values are considered trash

        metadata = dict()
        for (station_name, var, units, tstype), station_key in station_mapper.inner.items():
            extra_metadata = stations_with_metadata[station_name].metadata
            d = {
                "data_id": self.config.name,
                "station_name": station_name,
                "var_info": {
                    var: {"units": units},
                },
                **stations_with_metadata[station_name],
                **extra_metadata,
            }
            if "ts_type" not in d:
                d["ts_type"] = tstype
            metadata[station_key] = d

        meta_idx = defaultdict(dict)
        for (_station_name, var, _units, tstype), station_key in station_mapper.inner.items():
            var_key = var_mapper[var]
            mask = (outarray[:, UngriddedData._METADATAKEYINDEX] == station_key) & (
                outarray[:, UngriddedData._VARINDEX] == var_key
            )
            indices = np.flatnonzero(mask)
            meta_idx[station_key][var] = indices

        var_idx = var_mapper.inner

        return UngriddedData._from_raw_parts(outarray, metadata, meta_idx, var_idx)

    def get_variables(self) -> list[str]:
        return self.reader.variables()

    def get_stations(self) -> dict[str, Station]:
        return self.reader.stations()

    def read(self, vars_to_retrieve=None) -> UngriddedData:
        allowed_vars = self.get_variables()
        if vars_to_retrieve is None:
            vars_to_retrieve = allowed_vars
        else:
            if isinstance(vars_to_retrieve, str):
                vars_to_retrieve = [vars_to_retrieve]

        data = {}
        for var in vars_to_retrieve:
            if var not in allowed_vars:
                logger.warning(
                    f"Variable {var} not in list over allowed variabes for {self.config.reader_id}: {allowed_vars}"
                )
                continue

            data[var] = self.reader.data(varname=var)

        return self._convert_to_ungriddeddata(data)
