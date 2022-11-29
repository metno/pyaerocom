from __future__ import annotations

import numpy as np
import pandas as pd

from pyaerocom import StationData


class Station:
    def __init__(self, stationname, lat, lon, alt) -> None:
        self.stationname = stationname
        self.lat = lat
        self.lon = lon
        self.alt = alt

        self.measurements: dict[str, Measurement] = {}

    def add_measurement(self, species: str, unit: str, data: float, time: np.datetime64) -> None:
        if species not in self.measurements:
            self.measurements[species] = Measurement(species, unit)

        self.measurements[species].add_measurement(data, time, unit)

    def add_series(self, species: str, unit: str, ts: pd.Series) -> None:
        if species not in self.measurements:
            self.measurements[species] = Measurement(species, unit)

        self.measurements[species].add_series(ts)

    def to_stationdata(self, data_id: str, dataset: str, filename: str | list[str]) -> StationData:
        data_out = StationData()
        data_out.data_id = data_id
        data_out.dataset_name = dataset
        data_out.station_id = self.stationname
        data_out.station_name = self.stationname
        data_out.filename = filename

        data_out.station_coords = {
            "latitude": self.lat,
            "longitude": self.lon,
            "altitude": self.alt,
        }
        data_out.latitude = self.lat
        data_out.longitude = self.lon
        data_out.altitude = self.alt

        data_out.ts_type = "hourly"
        # ToDo: check "variables" entry, it should not be needed anymore in UngriddedData
        data_out["variables"] = list(self.measurements.keys())
        for s in self.measurements:
            data_out["var_info"][s] = {}
            data_out["var_info"][s]["units"] = self.measurements[s].unit

            data_out["dtime"] = self._get_unique_times()

            data_out[s] = self.measurements[s].to_pandas()
        return data_out

    def _get_unique_times(self) -> list[np.datetime64]:
        times = []
        for s in self.measurements:
            times += self.measurements[s].time

        return sorted(list(set(times)))


class Measurement:
    def __init__(self, speciesname: str, unit: str) -> None:
        self.speciesname = speciesname
        self.unit = unit

        self.data: list[float] = []
        self.time: list[np.datetime64] = []

        self.timeseries: pd.Series

    def add_measurement(self, data: float, time: np.datetime64, unit: str) -> None:
        if unit != self.unit:
            raise ValueError(f"Unit {unit} is not the same {self.unit}")
        self.data.append(data)
        self.time.append(time)

    def to_pandas(self) -> pd.Series:
        if self.timeseries is not None:
            return self.timeseries
        return pd.Series(self.data, self.time)

    def add_series(self, ts: pd.Series):
        self.timeseries = ts
