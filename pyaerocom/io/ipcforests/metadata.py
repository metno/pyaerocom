from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd
from pandas import date_range

DEP_TYPE = {
    1: "Throughfall",
    2: "Bulk deposition",
    3: "Wet-only deposition",
    4: "Stemflow",
    5: "Fog",
    6: "Frozen fog (rime)",
    9: "Other",
    8: "Through also - do not use",
}

COUNTRY_CODES = {
    1: "FR",
    2: "BE",
    3: "NL",
    4: "DE",
    5: "IT",
    6: "UK",
    7: "IE",
    8: "DK",
    9: "GR",
    10: "PT",
    11: "ES",
    12: "LU",
    13: "SE",
    14: "AT",
    15: "FI",
    50: "CH",
    51: "HU",
    52: "RO",
    53: "PL",
    54: "SK",
    55: "NO",
    56: "LT",
    57: "HR",
    58: "CZ",
    59: "EE",
    60: "SI",
    61: "MD",
    62: "RU",
    63: "BG",
    64: "LV",
    65: "BY",
    66: "CY",
    67: "CS",
    68: "AD",
    95: "cn",
    80: "ME",
    96: "AZ",
    72: "TR",
}

COUNTRIES = {
    1: "France",
    2: "Belgium",
    3: "Netherlands",
    4: "Germany",
    5: "Italy",
    6: "United Kingdom",
    7: "Ireland",
    8: "Denmark",
    9: "Greece",
    10: "Portugal",
    11: "Spain",
    12: "Luxembourg",
    13: "Sweden",
    14: "Austria",
    15: "Finland",
    50: "Switzerland",
    51: "Hungary",
    52: "Romania",
    53: "Poland",
    54: "Slovak Republic",
    55: "Norway",
    56: "Lithuania",
    57: "Croatia",
    58: "Czech Republic",
    59: "Estonia",
    60: "Slovenia",
    61: "Republic of Moldova",
    62: "Russia",
    63: "Bulgaria",
    64: "Latvia",
    65: "Belarus",
    66: "Cyprus",
    67: "Serbia",
    68: "Andorra",
    95: "Canaries (Spain)",
    80: "Montenegro",
    96: "Azores (Portugal)",
    72: "Türkiye",
}


class Variables:
    def __init__(self) -> None:
        pass


class Station:
    def __init__(
        self,
        country_code: int,
        plot_code: int,
        sampler_code: int,
        lat: str,
        lon: str,
        alt: int,
        partner_code: int,
        ts_type: str,
    ) -> None:
        self.country_code = country_code
        self.plot_code = plot_code
        self.sampler_code = sampler_code
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.partner_code = partner_code
        self.ts_type = ts_type

        self.sampler_type = DEP_TYPE[self.sampler_code]

        self.data: dict[str, list[float]] = {}
        self.dtime: dict[str, list[datetime]] = {}

        self.country = COUNTRIES[country_code]

        self.station_name = self.get_station_name(country_code, plot_code, sampler_code)

        self.var_info: dict[str, dict[str, str | list[float]]] = {}

    @staticmethod
    def get_station_name(
        country_code: int,
        plot_code: int,
        sampler_code: int,
    ) -> str:
        return f"{COUNTRY_CODES[country_code]}-{plot_code}-{sampler_code}"

    def _add_species_to_var_info(self, species: str, unit: str) -> None:
        self.var_info[species] = dict(
            ts_type=self.ts_type,
            ts_type_src=self.ts_type,
            units=unit,
            sampler_type=self.sampler_type,
        )

    def add_measurement(self, species: str, time: datetime, measurement: float, unit: str) -> None:
        if species not in self.var_info:
            self._add_species_to_var_info(species, unit)
        if species not in self.dtime:
            self.dtime[species] = []
            self.data[species] = []

        self.dtime[species].append(time)
        self.data[species].append(measurement)

    def get_timeseries(self, species: str) -> pd.Series:
        return pd.Series(self.data[species], index=self.dtime[species])


class SurveyYear:
    def __init__(self, year: int, start: datetime, stop: datetime, periods: int) -> None:
        self.year = year
        self.start = start
        self.stop = stop
        self.periods = periods

        self.daterange = date_range(start, stop, periods)
        self.days = (self.stop - self.start).days / self.periods

        self.ts_type = self._get_tstype()

    def get_date(self, period: int) -> datetime:
        if period > self.periods or period <= 0:

            raise ValueError(f"The period {period} needs to be in the range 1-{self.periods}")
        return self.start + timedelta(days=self.days * (period - 1))
        # return self.daterange[period - 1]

    def _get_tstype(self) -> str:

        days = (self.stop - self.start).days / self.periods

        if self.days >= 26:
            return "monthly"
        elif self.days >= 6:
            return "weekly"
        else:
            return "daily"


class Plot:
    def __init__(
        self,
        country_code: int,
        plot_code: int,
        sampler_code: int,
        lat: str,
        lon: str,
        alt: int,
        partner_code: int,
    ) -> None:
        self.country_code = country_code
        self.plot_code = plot_code
        self.sampler_code = sampler_code
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.partner_code = partner_code

        self.periods = {}
        self.survey_years: dict[int, SurveyYear] = {}

    def add_survey_year(self, year: int, start: str, stop: str, periods: int) -> None:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        stop_dt = datetime.strptime(stop, "%Y-%m-%d")
        self.survey_years[year] = SurveyYear(year, start_dt, stop_dt, periods)

    def get_date(self, year: int, period: int) -> datetime:
        return self.survey_years[year].get_date(period)


class Plots:
    def __init__(self, plot_file: str) -> None:
        self.plot_file: str = plot_file
        self.plots: dict[int, dict[int, dict[int, Plot]]] = {}

    def read_file(self, altitudes: dict[str, int]) -> dict[int, dict[int, dict[int, Plot]]]:
        plots: dict[int, dict[int, dict[int, Plot]]] = {}
        print(f"Starting to read plot metadata")
        with open(self.plot_file, "r") as f:
            f.readline()
            for line in f:
                words = line.split(";")
                if words[0] == "":
                    continue

                survey_year = int(words[0])
                country_code = int(words[1])
                partner_code = int(words[2])
                plot_code = int(words[3])
                sampler_code = int(words[4])

                lat = words[6]
                lon = words[7]
                alt_code = words[8]
                start = words[9]
                stop = words[10]
                periods = int(words[11])

                alt = altitudes[alt_code]

                if start == "" or stop == "":
                    continue

                if country_code not in plots:
                    plots[country_code] = {}
                if plot_code not in plots[country_code]:
                    plots[country_code][plot_code] = {}
                if sampler_code not in plots[country_code][plot_code]:
                    plots[country_code][plot_code][sampler_code] = Plot(
                        country_code, plot_code, sampler_code, lat, lon, alt, partner_code
                    )

                plots[country_code][plot_code][sampler_code].add_survey_year(
                    survey_year, start, stop, periods
                )
        print(f"Done read plot metadata")
        self.plots = plots
        return plots

    def get_ts_type(self, year: int, country_code: int, plot_code: int, sampler_code: int) -> str:
        return self.plots[country_code][plot_code][sampler_code].survey_years[year].ts_type

    def get_date(
        self, year: int, country_code: int, plot_code: int, sampler_code: int, period: int
    ) -> datetime:
        return self.plots[country_code][plot_code][sampler_code].get_date(year, period)

    def get_days(self, year: int, country_code: int, plot_code: int, sampler_code: int) -> float:
        start = self.plots[country_code][plot_code][sampler_code].survey_years[year].start
        stop = self.plots[country_code][plot_code][sampler_code].survey_years[year].stop
        days = self.plots[country_code][plot_code][sampler_code].survey_years[year].days

        if start == stop:
            raise ValueError(f"start {start} is the same as stop {stop}")

        return days

    def get_position(
        self, year: int, country_code: int, plot_code: int, sampler_code: int
    ) -> Tuple[float, float, int]:
        lat = self._coord_to_desimal(self.plots[country_code][plot_code][sampler_code].lat)
        lon = self._coord_to_desimal(self.plots[country_code][plot_code][sampler_code].lon)
        alt = self.plots[country_code][plot_code][sampler_code].alt

        return lat, lon, alt

    def _coord_to_desimal(self, coord: str) -> float:
        sign = 1
        if "-" in coord:
            sign = -1
            coord = coord[1:]

        if coord == "0":
            return 0

        coord = coord[:-2]
        if len(coord) >= 2:
            minute = int(coord[-2:])
            coord = coord[:-2]
        else:
            return sign * ((int(coord) / 60.0))

        degree = int(coord)

        return sign * (degree + (minute / 60.0))


class MetadataReader:
    def __init__(self, dir: str) -> None:
        self.dir = dir

        self.add_dir = dir + "/adds"

        self.altitudes = self._get_altitude_dir()

        self.plots = Plots(self.dir + "/dp_pld.csv")
        self.plots.read_file(self.altitudes)

        self.deposition_type = DEP_TYPE

    def _get_altitude_dir(self) -> dict[str, int]:
        altitudes = {}
        with open(self.add_dir + "/dictionaries/d_altitude.csv") as f:
            f.readline()
            for line in f:
                words = line.split(";")
                altitudes[words[0]] = int(words[4]) + (int(words[5]) - int(words[4])) // 2

        return altitudes


if __name__ == "__main__":
    metadata = MetadataReader(
        "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/ipc-forests/dep"
    )
    breakpoint()
    # print(metadata.altitudes)
