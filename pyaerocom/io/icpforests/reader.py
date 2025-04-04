from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path

import numpy as np
from tqdm import tqdm

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.io.icpforests.metadata import MetadataReader, Station, SurveyYear
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)


class ReadICPForest(ReadUngriddedBase):
    #: version log of this class (for caching)
    __version__ = "0.5_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.ICPFORESTS_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.ICPFORESTS_NAME]

    TS_TYPE = "undefined"

    _FILEMASK = "dp_dem.csv"

    #: Temporal resolution codes that (so far) can be understood by pyaerocom
    TS_TYPE_CODES = {
        "1mn": "minutely",
        "1h": "hourly",
        "1d": "daily",
        "1w": "weekly",
        "1mo": "monthly",
        "mn": "minutely",
        "h": "hourly",
        "d": "daily",
        "w": "weekly",
        "mo": "monthly",
    }

    VAR_POSITION = {
        "wetoxs": 20,
        "wetoxn": 19,
        "wetrdn": 17,
        "dryoxs": 20,
        "dryoxn": 19,
        "dryrdn": 17,
        "depoxs": 20,
        "depoxn": 19,
        "deprdn": 17,
        "depna": 16,
        "depoxsf": 20,
        "depoxnf": 19,
        "deprdnf": 17,
        "depnaf": 16,
        "wetso4": 20,
        "wetno3": 19,
        "wetnh4": 17,
        "wetno2": 41,
        "wetna": 16,
        "wetcl": 18,
    }

    UNITS = {
        "wetoxs": "mg S m-2 d-1",
        "wetoxn": "mg N m-2 d-1",
        "wetrdn": "mg N m-2 d-1",
        "dryoxs": "mg S m-2 d-1",
        "dryoxn": "mg N m-2 d-1",
        "dryrdn": "mg N m-2 d-1",
        "depoxs": "mg S m-2 d-1",
        "depoxn": "mg N m-2 d-1",
        "deprdn": "mg N m-2 d-1",
        "depoxsf": "mg S m-2 d-1",
        "depoxnf": "mg N m-2 d-1",
        "deprdnf": "mg N m-2 d-1",
        "wetso4": "mg S m-2 d-1",
        "wetno3": "mg N m-2 d-1",
        "wetnh4": "mg N m-2 d-1",
        "wetno2": "mg N m-2 d-1",
        "wetna": "mg m-2 d-1",
        "depna": "mg m-2 d-1",
        "depnaf": "mg m-2 d-1",
        # unverified
        "wetcl": "mg m-2 d-1",
    }

    SEASALT_CORRECTION = {
        "wetoxs": 0.3338,
        "wetso4": 0.3338,
        "depoxs": 0.3338,
        "depoxsf": 0.3338,
    }
    SEASALT_FACTORS = {
        "wetna": 0.120,
        "wetcl": 0.103,
    }

    DEP_TYPES_TO_USE = ["Throughfall", "Bulk", "Wet-only"]

    QUALITY_LIMIT = 0.5

    MIN_YEAR = 1984
    MAX_YEAR = 2019

    def __init__(self, data_id=None, data_dir=None):
        super().__init__(data_id, data_dir)

        self.metadata = None

        self._file_dir = None
        self.files = None

        if data_dir is not None:
            self.metadata = MetadataReader(data_dir)

    @property
    def file_dir(self):
        """Directory containing EBAS NASA Ames files"""
        if self._file_dir is not None:
            return self._file_dir
        return os.path.join(self.data_dir)

    @file_dir.setter
    def file_dir(self, val):
        if not isinstance(val, str) or not os.path.exists(val):
            raise FileNotFoundError("Input directory does not exist")

        self._file_dir = val

    def read(self, vars_to_retrieve=None, files=[], first_file=None, last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file
            in the list is used

        Returns
        -------
        UngriddedData
            instance of ungridded data object containing data from all files.
        """
        self.files = Path(self.data_dir).joinpath(self._FILEMASK)
        data = self.read_file(
            str(self.files),
            vars_to_retrieve,
        )

        return data

    @property
    def PROVIDES_VARIABLES(self):
        """List of variables that are provided by this dataset

        Note
        ----
        May be implemented as global constant in header
        """
        return list(self.VAR_POSITION.keys())

    @property
    def DEFAULT_VARS(self):
        """List containing default variables to read"""
        return list(self.VAR_POSITION.keys())

    def read_file(self, filename, vars_to_retrieve=None, last_line=None):
        """Read single file

        Parameters
        ----------
        filename : str
            string specifying filename
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        last_line : int
            last line number to read
            Used to speed up testing

        Returns
        -------
        :obj:`dict` or :obj:`StationData`, or other...
            imported data in a suitable format that can be handled by
            :func:`read` which is supposed to append the loaded results from
            this method (which reads one datafile) to an instance of
            :class:`UngriddedData` for all files.
        """
        stations: dict[str, dict[str, Station]] = {}
        if self.metadata is None:
            if self.data_dir is None:
                raise ValueError("Data Dir is not read yet")

            self.metadata = MetadataReader(self.data_dir)

        if vars_to_retrieve is None:
            vars_to_retrieve = self.PROVIDES_VARIABLES

        with open(filename) as f:
            f.readline()

            for line_nr, line in tqdm(enumerate(f)):
                words = line.split(";")
                year = int(words[0])
                country_code = int(words[1])
                partner_code = int(words[2])
                plot_code = int(words[3])
                sampler_code = int(words[9])
                q_flag = int(words[44]) if words[44] != "" else 0

                # 8 is the code for "do not use"
                if (
                    self.metadata.deposition_type[sampler_code] not in self.DEP_TYPES_TO_USE
                    or sampler_code == 8
                ):
                    continue

                period = int(words[6])
                start = words[4]
                stop = words[5]

                quantity = words[47]
                if quantity == "":  # or quantity == "0":
                    continue
                else:
                    quantity = float(quantity)

                try:
                    self.metadata.plots.plots[country_code]
                    self.metadata.plots.plots[country_code][plot_code]
                    self.metadata.plots.plots[country_code][plot_code][sampler_code]
                except KeyError:
                    logger.warning(
                        f"Some metadata is missing for {country_code=}, {plot_code=}, {sampler_code=}. Skipping"
                    )
                    continue

                try:
                    self.metadata.plots.plots[country_code][plot_code][sampler_code].survey_years[
                        year
                    ]
                except KeyError:
                    logger.warning(
                        f"Year {year} can't be found for {country_code=}, {plot_code=}, {sampler_code=}. Only years found are {self.metadata.plots.plots[country_code][plot_code][sampler_code].survey_years.keys()}"
                    )
                    continue
                days, dtime, ts_type = self._get_days_date_ts_type(
                    year, country_code, plot_code, sampler_code, period, start, stop
                )

                if days is None or dtime is None or ts_type is None:
                    continue
                station_name = Station.get_station_name(country_code, plot_code, sampler_code)

                if station_name not in stations:
                    stations[station_name] = {}
                if ts_type not in stations[station_name]:
                    lat, lon, alt = self.metadata.plots.get_position(
                        year, country_code, plot_code, sampler_code
                    )
                    stations[station_name][ts_type] = Station(
                        country_code, plot_code, sampler_code, lat, lon, alt, partner_code, ts_type
                    )

                for species in vars_to_retrieve:
                    conc = self._get_species_conc(words[self.VAR_POSITION[species]], species)

                    # Sea-salt correction
                    # The factor self.SEASALT_CORRECTION[species] is the factor use to go from mg/L to mg S/L (for sulpher)
                    if species in self.SEASALT_CORRECTION:
                        na_factor = (
                            self._get_species_conc(words[self.VAR_POSITION["wetna"]], "wetna")
                            * self.SEASALT_FACTORS["wetna"]
                            * self.SEASALT_CORRECTION[species]
                        )
                        cl_factor = (
                            self._get_species_conc(words[self.VAR_POSITION["wetcl"]], "wetcl")
                            * self.SEASALT_FACTORS["wetcl"]
                            * self.SEASALT_CORRECTION[species]
                        )
                        seasalt_correction = min(na_factor, cl_factor)

                        if seasalt_correction > conc and conc > 0:
                            logger.warning(
                                f"Seasalt correction {seasalt_correction} is larger than concentration {conc} for {species}"
                            )
                        if conc > 0:
                            conc -= seasalt_correction

                    # Unit correction
                    conc *= quantity / days

                    stations[station_name][ts_type].add_measurement(
                        species, dtime, conc, self.UNITS[species], q_flag
                    )

        station_datas = []
        for station_name in stations:
            for ts_type in stations[station_name]:
                station = stations[station_name][ts_type]
                station_data = StationData()
                station_data.var_info = BrowseDict(**station.var_info)
                for species in station.data.keys():
                    station_data[species] = self._clean_data_with_flags(
                        station.data[species],
                        station.dtime[species],
                        station.flags[species],
                        species,
                    )
                    station_data.dtime = station.dtime[species]

                station_data.country = station.country

                # Needs to convert coordinates to correct type!
                station_data.station_coords = {
                    "latitude": station.lat,
                    "longitude": station.lon,
                    "altitude": station.alt,
                }

                station_data.latitude = station.lat
                station_data.longitude = station.lon
                station_data.altitude = station.alt

                station_data.filename = filename
                station_data.ts_type = station.ts_type
                station_data.ts_type_src = station.ts_type
                station_data.station_name = station.station_name
                station_data._append_meta_item("sampler_type", station.sampler_type)

                station_data.data_id = self.data_id

                station_datas.append(station_data)
        return UngriddedData.from_station_data(station_datas, add_meta_keys="sampler_type")

    def _get_species_conc(self, conc_str: str, species: str) -> float:
        conc = float(conc_str) if conc_str != "" else np.nan
        if conc == -1:
            logger.warning(f"Value for {species} found to be {conc}")
            conc = np.nan
        return conc

    def _get_days_date_ts_type(
        self,
        year: int,
        country_code: int,
        plot_code: int,
        sampler_code: int,
        period: int,
        start: str | datetime,
        stop: str | datetime,
    ) -> tuple[float | None, datetime | None, str | None]:
        if start != "" and stop != "":
            if isinstance(start, str):
                start = datetime.strptime(start, "%Y-%m-%d")
            if isinstance(stop, str):
                stop = datetime.strptime(stop, "%Y-%m-%d")

            if (stop - start).days <= 0:
                return None, None, None

            return (stop - start).days, start, self._get_tstype(start, stop)

        if self.metadata is None:
            raise ValueError("Metadata is not read yet")

        try:
            days = self.metadata.plots.get_days(year, country_code, plot_code, sampler_code)
        except ValueError as e:
            logger.warning(repr(e))
            return None, None, None

        if days == 0:
            return None, None, None

        try:
            dtime = self.metadata.plots.get_date(
                year, country_code, plot_code, sampler_code, period
            )
        except ValueError:
            return None, None, None

        ts_type = self.metadata.plots.get_ts_type(year, country_code, plot_code, sampler_code)

        return days, dtime, ts_type

    def _get_tstype(self, start: datetime, stop: datetime) -> str:
        days = (stop - start).days

        return SurveyYear.get_tstype(days)

    def _clean_data_with_flags(
        self,
        data: list[float],
        time: list[datetime],
        flags: list[int],
        species: str,
    ) -> list[float]:
        data_array = np.array(data)
        flags_array = np.array(flags)
        years = np.array([i.year for i in time])

        for year in range(self.MIN_YEAR, self.MAX_YEAR):
            yr_flags = flags_array[np.where(years == year)]
            # yr_flags can have 0 length
            try:
                quality = np.sum(np.where(yr_flags == 0)) / len(yr_flags)
                if quality < self.QUALITY_LIMIT:
                    logger.warning(
                        f"Quality of {quality} found for {species} in year {year}. Setting data this year to NaN"
                    )
                    data_array[np.where(years == year)] = np.nan

            except RuntimeWarning:
                # yr_flags has 0 length
                logger.warning(f"No data for species {species} in year {year}.")

        return list(data_array)
