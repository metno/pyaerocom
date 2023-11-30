from pyaerocom.io.pyaro.pyaro_config import PyaroConfig

from pyaro import list_timeseries_engines, open_timeseries
from pyaro.timeseries import Reader, Data, Station
from pyaro.timeseries.Wrappers import VariableNameChangingReader

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData

import numpy as np

import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


class ReadPyaro(ReadUngriddedBase):
    __version__ = "0.0.2"

    SUPPORTED_DATASETS = list(list_timeseries_engines().keys())

    def __init__(self, config: PyaroConfig) -> None:
        self.config: PyaroConfig = config

        self._check_id()

        
        self.converter = PyaroToUngriddedData(self.config)
        self.reader = self.converter.reader
        self._data_id = self.config.data_id
        self._data_dir = self.config.filename_or_obj_or_url





        

    """
    Definition of abstract methods from ReadUngriddedBase
    """

    @property
    def DATA_ID(self):
        return self._data_id

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
        return "monthly"

    @property
    def _FILEMASK(self):
        return self.config.filename_or_obj_or_url

    @property

    
    @staticmethod
    def get_pyaro_readers():
        return list_timeseries_engines()

    def read(self, vars_to_retrieve=None, files=..., first_file=None, last_file=None):
        return self.converter.read(vars_to_retrieve=vars_to_retrieve)

    def read_file(self, filename, vars_to_retrieve=None):
        return self.converter.read(vars_to_retrieve)

    def _check_id(self):
        avail_readers = list_timeseries_engines()
        if not self.config.data_id in avail_readers:
            logger.warning(f"Could not find {self.config.data_id} in list of available Pyaro readers: {avail_readers}")
        





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

    def __init__(self, config: PyaroConfig) -> None:
        self.data: UngriddedData = UngriddedData()
        self.config = config
        self.reader: Reader = self._open_reader()

    def _open_reader(self) -> Reader:
        data_id = self.config.data_id

        if self.config.name_map is None:
            return open_timeseries(data_id, self.config.filename_or_obj_or_url, filters=self.config.filters)
        else:
            return VariableNameChangingReader(
                open_timeseries(data_id, self.config.filename_or_obj_or_url, filters=self.config.filters),
                self.config.name_map,
            )

    def _convert_to_ungriddeddata(self, pyaro_data: dict[str, Data]) -> UngriddedData:
        stations = self.get_stations()

        var_size = {var: len(pyaro_data[var]) for var in pyaro_data}
        vars = list(pyaro_data.keys())
        total_size = sum(list(var_size.values()))
        units = {var: {"units": pyaro_data[var]._units} for var in pyaro_data}


        # Object necessary for ungriddeddata
        var_idx = {var: i for i, var in enumerate(vars)}
        metadata = self._make_ungridded_metadata(stations=stations, var_idx=var_idx, units=units)
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
        self, stations: dict[str, Station], var_idx: dict[str, int], units: dict[str, str]
    ) -> dict[str, dict[str, str | list[str]]]:
        idx = 0
        metadata = {}
        for name, station in stations.items():
            metadata[idx] = dict(
                data_id=self.config.data_id,
                variables=list(self.get_variables()),
                var_info = units,
                # [
                # var_idx[var] for var in self.get_variables()
                # ],  # Temp: all stations are now assumed to have all variables
                instrument_name="",
                latitude=station["latitude"],
                longitude=station["longitude"],
                altitude=station["altitude"],
                station_name=name,
                country=station["country"],
                ts_type="monthly",  # TEMP
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
        new_data[self._DATAHEIGHTINDEX] = np.nan
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

    data_id = "csv_timeseries"

    config = PyaroConfig(
        data_id=data_id,
        filename_or_obj_or_url="/home/danielh/Documents/pyaerocom/pyaro/tests/testdata/csvReader_testdata.csv",
        filters=[],
        name_map={"SOx": "oxidised_sulphur"},
    )
    rp = ReadPyaro(config=config)

    print(rp.DEFAULT_VARS)
    data = rp.read()  # ["SOx", "NOx"])
    station = data.to_station_data(0)
    print(station)
