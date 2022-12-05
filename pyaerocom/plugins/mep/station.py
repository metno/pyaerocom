from __future__ import annotations

from itertools import chain
from typing import Iterable, Iterator, NamedTuple

import numpy as np
import pandas as pd

from pyaerocom.stationdata import StationData


class Station:
    def __init__(self, station_name: str, lat: float, lon: float, alt: float) -> None:
        self.station_name = station_name
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.measurements: list[Measurement] = []

    def add_series(self, species: str, unit: str, ts: pd.Series) -> None:
        assert species not in set(self.species), f"{species} already included"
        assert not ts.empty, f"{species} is empty"
        self.measurements.append(Measurement(species, unit, ts))

    @property
    def species(self) -> Iterator[str]:
        return (obs.species for obs in self.measurements)

    def to_stationdata(self, data_id: str, dataset: str) -> StationData:
        data_out = StationData()
        data_out.data_id = data_id
        data_out.dataset_name = dataset
        data_out.station_id = self.station_name
        data_out.station_name = self.station_name

        data_out.station_coords = {
            "latitude": self.lat,
            "longitude": self.lon,
            "altitude": self.alt,
        }
        data_out.latitude = self.lat
        data_out.longitude = self.lon
        data_out.altitude = self.alt

        data_out.ts_type = "hourly"
        # what happens when different measurements have different time steps?
        data_out["dtime"] = self.unique_times
        assert data_out["dtime"], "no time"

        for obs in self.measurements:
            data_out[obs.species] = obs.timeseries
            data_out["var_info"][obs.species] = {"units": obs.unit}

        return data_out

    @property
    def unique_times(self) -> list[np.datetime64]:
        times = chain.from_iterable(obs.time for obs in self.measurements)
        return sorted(set(times))


class Measurement(NamedTuple):
    species: str
    unit: str
    timeseries: pd.Series

    @property
    def time(self) -> Iterable[np.datetime64]:
        return self.timeseries.index
