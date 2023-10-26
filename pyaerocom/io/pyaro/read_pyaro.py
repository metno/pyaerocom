from pyaro_config import PyaroConfig

from pyaro.timeseries import Reader, Data, Station
from pyaro.csvreader import CSVTimeseriesReader

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

import numpy as np

import logging

logger = logging.getLogger(__name__)


class ReadPyaro(ReadUngriddedBase):
    __version__ = "0.0.1"

    def __init__(self, config: PyaroConfig, reader: Reader) -> None:
        self.config: PyaroConfig = config
        # self.engine: Reader = config.engine
        self.reader = reader
        self.converter = PyaroToUngriddedData(self.reader, self.config)

    """
    Definition of abstract methods from ReadUngriddedBase
    """

    def DATA_ID(self):
        return self.config.data_id

    def PROVIDES_VARIABLES(self):
        """
        return self.reader.get_variables()
        """
        return []

    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    def TS_TYPE(self):
        """
        To be provided by the reader or engine
        """
        return "undefined"

    def _FILEMASK(self):
        return self.config.filename_or_obj_or_url

    def SUPPORTED_DATASETS(self):
        return [self.data_id]

    def read(self, vars_to_retrieve=None, files=..., first_file=None, last_file=None):
        return self.converter.read(vars_to_retrieve=vars_to_retrieve)

    def read_file(self, filename, vars_to_retrieve=None):
        return self.read(vars_to_retrieve)


class PyaroToUngriddedData:
    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4  # altitude of measurement device
    _VARINDEX = 5
    _DATAINDEX = 6
    _DATAHEIGHTINDEX = 7
    _DATAERRINDEX = 8  # col where errors can be stored
    _DATAFLAGINDEX = 9  # can be used to store flags
    _STOPTIMEINDEX = 10  # can be used to store stop time of acq.
    _TRASHINDEX = 11  # index where invalid data can be moved to (e.g. when outliers are removed)

    def __init__(self, reader: Reader, config: PyaroConfig) -> None:
        self.data: UngriddedData = UngriddedData()
        self.reader: Reader = reader
        self.config = config

    def _convert_to_ungriddeddata(self, pyaro_data: dict[str, Data]) -> UngriddedData:
        stations = self.get_stations()

        var_size = {var: len(pyaro_data[var]) for var in pyaro_data}
        vars = list(pyaro_data.keys())
        total_size = sum(list(var_size.values()))

        # Object necessary for ungriddeddata
        var_idx = {var: i for i, var in enumerate(vars)}
        metadata = self._make_ungridded_metadata(stations=stations, var_idx=var_idx)
        meta_idx = {s: {v: [] for v in vars} for s in metadata}
        data_array = np.zeros([total_size, 12])

        # Helper objects
        station_idx = {metadata[idx]["station_name"]: idx for idx in metadata}

        idx = 0
        for var, var_data in pyaro_data.items():
            # var_data = pyaro_data[var]
            size = var_size[var]
            for i in range(
                1, size
            ):  # The 1 start is a temp fix for the empty first row of the current Data implementation from pyaro
                data_line = var_data[i]
                current_station = data_line["stations"]

                # Fills data array
                ungriddeddata_line = self._pyaro_dataline_to_ungriddeddata_dataline(
                    data_line, idx, var_idx[var]
                )

                data_array[idx, :] = ungriddeddata_line

                #  Fills meta_idx
                meta_idx[station_idx[current_station]][var].append(idx)

                idx += 1

        new_meta_idx = {}
        for station_id in meta_idx:
            new_meta_idx[station_id] = {}
            for var_id in meta_idx[station_id]:
                new_meta_idx[station_id][var_id] = np.array(meta_idx[station_id][var_id])

        self.data._data = data_array
        self.data.meta_idx = new_meta_idx
        self.data.metadata = metadata
        self.data.var_idx = var_idx

        return self.data

    def _make_ungridded_metadata(
        self, stations: dict[str, Station], var_idx: dict[str, int]
    ) -> dict[str, dict[str, str | list[str]]]:
        idx = 0
        metadata = {}
        for name, station in stations.items():
            metadata[idx] = dict(
                data_id=self.config.data_id,
                variables=list(self.get_variables()),
                # [
                # var_idx[var] for var in self.get_variables()
                # ],  # Temp: all stations are now assumed to have all variables
                instrument_name="",
                latitude=station["latitude"],
                longitude=station["longitude"],
                altitude=station["altitude"],
                station_name=name,
                country=station["country"],
                data_revision="n/d",  # Temp: Need to be changed. Must add way of getting this from Reader
            )
            idx += 1

        return metadata

    def _pyaro_dataline_to_ungriddeddata_dataline(
        self, data: np.void, idx: int, var_idx: int
    ) -> np.ndarray:
        new_data = np.zeros(12)
        new_data[self._METADATAKEYINDEX] = idx
        new_data[self._TIMEINDEX] = data["start_times"]
        new_data[self._LATINDEX] = data["latitudes"]
        new_data[self._LONINDEX] = data["longitudes"]
        new_data[self._ALTITUDEINDEX] = data["altitudes"]
        new_data[self._VARINDEX] = var_idx
        new_data[self._DATAINDEX] = data["values"]
        new_data[self._DATAHEIGHTINDEX] = 0
        new_data[self._DATAERRINDEX] = data["standard_deviations"]
        new_data[self._DATAFLAGINDEX] = data["flags"]
        new_data[self._STOPTIMEINDEX] = data["stop_times"]
        new_data[self._TRASHINDEX] = np.nan

        return new_data

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
                print(var, allowed_vars)
                logger.warning(
                    f"Variable {var} not in list over allowed variabes for {self.config.data_id}: {allowed_vars}"
                )
                continue

            data[var] = self.reader.data(varname=var)

        return self._convert_to_ungriddeddata(data)


if __name__ == "__main__":
    data_id = "csv_reader"
    reader = CSVTimeseriesReader(
        filename="/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/pyaro/src/pyaro/csvreader/testdata/csvReader_testdata.csv",
    )

    config = PyaroConfig(
        data_id=data_id,
        filename_or_obj_or_url="/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/pyaro/src/pyaro/csvreader/testdata/csvReader_testdata.csv",
        filters=[],
    )
    rp = ReadPyaro(config, reader)

    data = rp.read(["SOx", "NOx"])
    station = data.to_station_data(0)
