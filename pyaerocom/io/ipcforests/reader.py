import fnmatch
import logging
import os
import re
from statistics import quantiles

import numpy as np
from geonum.atmosphere import T0_STD, p0
from metadata import MetadataReader, Station
from tqdm import tqdm

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.molmasses import get_molmass
from pyaerocom.stationdata import StationData
from pyaerocom.tstype import TsType
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)


class ReadIPCForest(ReadUngriddedBase):

    #: version log of this class (for caching)
    __version__ = "0.1_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.IPCFORESTS_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.IPCFORESTS_NAME]

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
    }

    def __init__(self, data_id=None, data_dir=None):
        super().__init__(data_id, data_dir)

        self.metadata = None
        # self.data_dir = data_dir

        if data_dir is not None:
            self.metadata = MetadataReader(data_dir)

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
        ...

    def PROVIDES_VARIABLES(self):
        """List of variables that are provided by this dataset

        Note
        ----
        May be implemented as global constant in header
        """
        pass

    def DEFAULT_VARS(self):
        """List containing default variables to read"""
        pass

    def read_file(self, filename, vars_to_retrieve=None):
        """Read single file

        Parameters
        ----------
        filename : str
            string specifying filename
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded

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
            raise ValueError(f"Metadata is not read yet")

        with open(filename, "r") as f:
            f.readline()
            for line_nr, line in tqdm(enumerate(f)):
                words = line.split(";")
                year = int(words[0])
                country_code = int(words[1])
                partner_code = int(words[2])
                plot_code = int(words[3])
                sampler_code = int(words[9])

                period = int(words[6])

                quantity = words[47]
                if quantity == "" or quantity == "0":
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
                except KeyError as e:
                    logger.warning(
                        f"Year {year} can't be found for {country_code=}, {plot_code=}, {sampler_code=}. Only years found are {self.metadata.plots.plots[country_code][plot_code][sampler_code].survey_years.keys()}"
                    )
                    continue

                try:

                    days = self.metadata.plots.get_days(
                        year, country_code, plot_code, sampler_code
                    )
                except ValueError as e:
                    logger.warning(repr(e))
                    continue

                try:
                    dtime = self.metadata.plots.get_date(
                        year, country_code, plot_code, sampler_code, period
                    )
                except ValueError:
                    continue

                ts_type = self.metadata.plots.get_ts_type(
                    year, country_code, plot_code, sampler_code
                )
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

                for species in self.VAR_POSITION:
                    conc = self._get_species_conc(words[self.VAR_POSITION[species]])

                    conc *= 1e-6 * quantity / days

                    stations[station_name][ts_type].add_measurement(
                        species, dtime, conc, "mg m-2 d-1"
                    )

        station_datas = []
        for station_name in stations:
            for ts_type in stations[station_name]:
                station = stations[station_name][ts_type]
                station_data = StationData()
                station_data.var_info = BrowseDict(**station.var_info)
                for species in station.data.keys():
                    station_data[species] = station.data[species]
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

                station_datas.append(station_data)

        breakpoint()
        return UngriddedData.from_station_data(station_datas)

    def _get_species_conc(self, conc_str: str) -> float:
        return float(conc_str) if conc_str != "" else np.nan


if __name__ == "__main__":
    reader = ReadIPCForest(
        data_dir="/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/ipc-forests/dep"
    )
    filename = "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/ipc-forests/dep/dp_dem.csv"
    data = reader.read_file(filename)
