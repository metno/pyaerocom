"""
This module contains methods to create synthetic data objects for unit testing
"""
import numpy as np

from pyaerocom import StationData


def _make_station_data1():
    stat = StationData()

    d = dict(
        dataset_name="test",
        PI="jonas gliss",
        instrument_name="test instr",
        station_id=42,
        station_name="test station",
        ts_type="monthly",
        revision_date="20190513",
        data_level=2,
        country="norway",
        random_key1="bla",
        random_key2="blub",
        random_key3=["blub", "blablub"],
        random_key4=["blub", "blub"],
        filename="bla.csv",
        data_version=2,
    )

    stat.update(d)

    START = "2000"
    NUM_YEARS = 5
    NUM = NUM_YEARS * 12
    stat.dtime = np.datetime64(START) + np.arange(NUM).astype("timedelta64[M]")

    stat.ec550aer = np.random.random_sample(NUM) - 0.5
    stat.od550aer = np.ones(NUM)
    stat.latitude = list(np.ones(NUM) * 33)
    stat.longitude = np.ones(NUM) * 15
    stat.altitude = (np.ones(NUM) * 300).astype(int)

    stat.var_info["ec550aer"] = {"units": "m-1"}
    stat.var_info["od550aer"] = {"units": "1"}

    return stat


def _make_station_data2():
    """Create an example synthetic instance of StationData class"""
    stat = StationData()
    d = dict(
        latitude=33.01,
        longitude=15,
        altitude=300,
        dataset_name="test (alt)",
        PI="Jonas Gliss",
        instrument_name="test instr",
        station_id=42,
        station_name="test station",
        ts_type="daily",
        revision_date="20190513",
        data_level=3,
        country="norway",
        data_version=2,
    )

    stat.update(d)

    START = "2007"
    NUM_DAYS = 277

    stat.dtime = np.datetime64(START) + np.arange(NUM_DAYS).astype("timedelta64[D]")

    stat.ec550aer = np.random.random_sample(NUM_DAYS) - 0.5
    stat.od550aer = np.ones(NUM_DAYS)
    stat.conco3 = np.arange(NUM_DAYS)

    stat.var_info["ec550aer"] = {"units": "Mm-1"}
    stat.var_info["od550aer"] = {"units": "1"}
    stat.var_info["conco3"] = {"units": "ug m-3"}

    return stat


class FakeStationDataAccess:
    """Factory for loading and accessing of data objects"""

    _LOADERS = dict(station_data1=_make_station_data1, station_data2=_make_station_data2)

    def __getitem__(self, key):
        if key in self.__dict__:  # item is loaded
            return self.__dict__[key]
        data = self._LOADERS[key]()
        self.__dict__[key] = data
        return data
