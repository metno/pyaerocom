from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pyaerocom import StationData


def station_data1() -> StationData:
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
    stat.data_err["ec550aer"] = np.random.random_sample(NUM) - 0.5
    stat.latitude = list(np.ones(NUM) * 33)
    stat.longitude = np.ones(NUM) * 15
    stat.altitude = (np.ones(NUM) * 300).astype(int)

    stat.var_info["ec550aer"] = {"units": "m-1"}
    stat.var_info["od550aer"] = {"units": "1"}

    return stat


def station_data2() -> StationData:
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

    _LOADERS = dict(station_data1=station_data1, station_data2=station_data2)

    def __getitem__(self, key):
        if key in self.__dict__:  # item is loaded
            return self.__dict__[key]
        data = self._LOADERS[key]()
        self.__dict__[key] = data
        return data


FAKE_STATION_DATA = FakeStationDataAccess()


def create_fake_station_data(addvars, varinfo, varvals, start, stop, freq, meta) -> StationData:
    if isinstance(addvars, str):
        addvars = [addvars]
    stat = StationData()
    stat.update(**meta)
    dtime = pd.date_range(start, stop, freq=freq).values
    stat["dtime"] = dtime
    for var in addvars:
        if var in varinfo:
            stat.var_info[var] = varinfo[var]
        if isinstance(varvals, dict):
            val = varvals[var]
        else:
            val = varvals
        stat[var] = np.ones(len(dtime)) * val
    return stat


def create_fake_stationdata_list() -> list[StationData]:
    stat1 = create_fake_station_data(
        "concpm10",
        {"concpm10": {"units": "ug m-3"}},
        10,
        "2010-01-01",
        "2010-12-31",
        "d",
        {
            "awesomeness": 10,
            "data_revision": 20120101,
            "ts_type": "daily",
            "latitude": 42.001,
            "longitude": 20,
            "altitude": 0.1,
            "station_name": "FakeSite",
        },
    )

    stat2 = create_fake_station_data(  # overlaps with first one
        "concpm10",
        {"concpm10": {"units": "ug m-3"}},
        20,
        "2010-06-01",
        "2011-12-31",
        "d",
        {
            "awesomeness": 12,
            "data_revision": 20110101,
            "ts_type": "daily",
            "latitude": 42.001,
            "longitude": 20,
            "altitude": 0.1,
            "station_name": "FakeSite",
        },
    )

    stat3 = create_fake_station_data(  # monthly, but missing ts_type and wrong unit
        "concpm10",
        {"concpm10": {"units": "mole mole-1"}},
        20,
        "2014-01-01",
        "2015-12-31",
        "3MS",
        {
            "awesomeness": 2,
            "data_revision": 20140101,
            "latitude": 42.001,
            "longitude": 20,
            "altitude": 0.1,
            "station_name": "FakeSite",
        },
    )

    stat4 = create_fake_station_data(  # invalid ts_type
        "concpm10",
        {"concpm10": {"units": "ug m-3"}},
        20,
        "1850",
        "2020",
        "1000d",
        {
            "awesomeness": 15,
            "data_revision": 20130101,
            "ts_type": "1000daily",
            "latitude": 42.001,
            "longitude": 20,
            "altitude": 0.1,
            "station_name": "FakeSite",
        },
    )

    stat5 = create_fake_station_data(  # new variable and monthly
        "od550aer",
        {"od550aer": {"units": "1"}},
        1,
        "2005",
        "2012",
        "MS",
        {
            "awesomeness": 42,
            "data_revision": 20200101,
            "ts_type": "monthly",
            "latitude": 22.001,
            "longitude": 10,
            "altitude": 99,
            "station_name": "FakeSite",
        },
    )

    stat6 = create_fake_station_data(
        "od550aer",
        {"od550aer": {"units": "1"}},
        0.1,
        "2008",
        "2009",
        "60d",
        {
            "awesomeness": 46,
            "data_revision": 20200101,
            "ts_type": "60daily",
            "latitude": 22.001,
            "longitude": 10,
            "altitude": 100,
            "station_name": "FakeSite2",
        },
    )

    stat_werr = create_fake_station_data(
        "od550aer",
        {"od550aer": {"units": "1"}},
        0.2,
        "2010",
        "2016",
        "10d",
        {
            "awesomeness": 30,
            "data_revision": 20200101,
            "ts_type": "10daily",
            "latitude": 22.001,
            "longitude": 10,
            "altitude": 100,
            "station_name": "FakeSite2",
        },
    )
    stat_werr.data_err["od550aer"] = np.ones(len(stat_werr.dtime)) * 9999

    return [stat1, stat2, stat3, stat4, stat5, stat6, stat_werr]


@pytest.fixture(scope="session")
def statlist():
    """fake stations data"""
    data = {}
    stats = create_fake_stationdata_list()
    data["all"] = stats
    data["od550aer"] = [stat.copy() for stat in stats if stat.has_var("od550aer")]
    pm10sites = [stat.copy() for stat in stats if stat.has_var("concpm10")]
    data["concpm10_X"] = pm10sites
    data["concpm10_X2"] = [stat.copy() for stat in pm10sites[:3]]
    data["concpm10"] = [stat.copy() for stat in pm10sites[:2]]
    return data
