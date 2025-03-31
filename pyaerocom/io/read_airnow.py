import codecs
import logging
import os
from glob import glob

import numpy as np
import pandas as pd
from tqdm import tqdm

from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.io import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

logger = logging.getLogger(__name__)


class ReadAirNow(ReadUngriddedBase):
    """
    Reading routine for North-American Air Now observations
    """

    # Data type of files
    _FILETYPE = ".dam"

    # File search mask to recursively retrieve list of data files
    _FILEMASK = f"/monthly/*{_FILETYPE}"

    #: Version log of this class (for caching)
    __version__ = "0.12"

    #: Column delimiter
    FILE_COL_DELIM = "|"

    #: Columns in data files
    FILE_COL_NAMES = [
        "date",
        "time",
        "station_id",
        "station_name",
        "time_zone",
        "variable",
        "unit",
        "value",
        "institute",
    ]
    # will be used millions of times, therefore store it
    FILE_COL_ROW_NUMBER = len(FILE_COL_NAMES)

    # row # for the variable
    ROW_VAR_COL = 5

    #: Mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
        "aqsid": "station_id",
        "name": "station_name",
        "lat": "latitude",
        "lon": "longitude",
        "elevation": "altitude",
        "city": "city",
        "address": "address",
        "timezone": "timezone",
        "environment": "area_classification",
        "populationclass": "station_classification",
        "modificationdate": "modificationdate",
        "comment": "comment",
    }

    #: conversion functions for metadata dtypes
    STATION_META_DTYPES = {
        "station_id": str,
        "station_name": str,
        "latitude": float,
        "longitude": float,
        "altitude": float,
        "city": str,
        "address": str,
        "timezone": str,
        "area_classification": str,
        "station_classification": str,
        "modificationdate": str,
        "comment": str,
    }

    # strings to be replaced in original station names
    REPLACE_STATNAME = {"&": "and", "/": " ", ":": " ", ".": " ", "'": ""}

    # Years in timestamps in the files are 2-digit (e.g. 20 for 2020)
    BASEYEAR = 2000

    #: Name of dataset (OBS_ID)
    DATA_ID = "AirNow"

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: Units found in data files
    UNIT_MAP = {
        "C": "celsius",
        "M/S": "m s-1",
        "MILLIBAR": "mbar",
        "MM": "mm",
        "PERCENT": "%",
        "PPB": "ppb",
        "PPM": "ppm",
        "UG/M3": "ug m-3",
        "WATTS/M2": "W m-2",
    }

    #: Variable names in data files
    VAR_MAP = {
        "concbc": "BC",
        "concpm10": "PM10",
        "concpm25": "PM2.5",
        "vmrco": "CO",
        "vmrnh3": "NH3",
        "vmrno": "NO",
        "vmrno2": "NO2",
        "vmrnox": "NOX",
        "vmrnoy": "NOY",
        "vmro3": "OZONE",
        "vmrso2": "SO2",
    }

    #: List of variables that are provided
    PROVIDES_VARIABLES = list(VAR_MAP)

    #: Default variables
    DEFAULT_VARS = PROVIDES_VARIABLES

    #: Frequency of measurements
    TS_TYPE = "hourly"

    #: file containing station metadata
    STAT_METADATA_FILENAME = "allStations_20191224.csv"

    def __init__(self, data_id=None, data_dir=None):
        super().__init__(data_id=data_id, data_dir=data_dir)
        self.make_datetime64_array = np.vectorize(self._date_time_str_to_datetime64)
        self._station_metadata = None

    @property
    def station_metadata(self):
        """Dictionary containing global metadata for each site"""
        if self._station_metadata is None:
            self._init_station_metadata()
        return self._station_metadata

    def _date_time_str_to_datetime64(self, date, time):
        """
        Convert date and time string into datetime64 object

        Parameters
        ----------
        date : str
            date string as mm/dd/yy as in data files
        time : str
            time of the day as HH:MM

        Returns
        -------
        datetime64[s]
        """
        mm, dd, yy = date.split("/")
        yr = str(self.BASEYEAR + int(yy))
        # returns as datetime64[s]
        return np.datetime64(f"{yr}-{mm}-{dd}T{time}:00")

    def _read_metadata_file(self):
        """
        Read station metadatafile

        Returns
        -------
        cfg : pandas.DataFrame
            metadata dataframe

        """
        fn = os.path.join(self.data_dir, self.STAT_METADATA_FILENAME)
        cfg = pd.read_csv(fn, sep=",", converters={"aqsid": lambda x: str(x)})
        return cfg

    def _correct_station_name(self, station_name):
        """
        Remove unwanted chars from original station names

        Parameters
        ----------
        station_name : str
            original station name

        Returns
        -------
        str
            station name cleaned of chars defined in :attr:`REPLACE_STATNAME`

        """
        for search, replace in self.REPLACE_STATNAME.items():
            station_name = station_name.replace(search, replace)
        return station_name

    def _init_station_metadata(self):
        """
        Initiate metadata for all stations

        Returns
        -------
        dict
            dictionary with metadata dictionaries for all stations

        """
        cfg = self._read_metadata_file()
        meta_map = self.STATION_META_MAP

        cols = list(cfg.columns.values)
        col_idx = {}
        for from_meta, to_meta in meta_map.items():
            col_idx[to_meta] = cols.index(from_meta)

        arr = cfg.values
        dtypes = self.STATION_META_DTYPES
        stats = {}
        for row in arr:
            stat = {}
            for meta_key, col_num in col_idx.items():
                stat[meta_key] = dtypes[meta_key](row[col_num])
            sid = stat["station_id"]

            stat["station_name"] = self._correct_station_name(stat["station_name"])
            stat["data_id"] = self.data_id
            stat["ts_type"] = self.TS_TYPE
            stats[sid] = stat
        self._station_metadata = stats
        return stats

    def get_file_list(self):
        """
        Retrieve list of data files

        Returns
        -------
        list
        """
        basepath = self.data_dir
        pattern = f"{basepath}{self._FILEMASK}"
        files = sorted(glob(pattern))
        return files

    def _read_file(self, file):
        """
        Read one datafile using :func:`pandas.read_csv`

        Parameters
        ----------
        file : str
            file path

        Returns
        -------
        df : pandas.DataFrame
            DataFrame containing the file data

        """

        # try utf_8 and cp863 reading first, then
        # determine file encoding and provide that to pandas
        # just determining the encoding is too slow given the # of files
        # Airbase consists of
        # just trying a couple of encodings and not determining the encoding all
        # the time speeds up reading by a factor of 5
        # make sure certain dtypes are set for a few rows (e.g. station code as str)
        try:
            encoding = "utf_8"
            df = pd.read_csv(
                file,
                sep=self.FILE_COL_DELIM,
                names=self.FILE_COL_NAMES,
                encoding=encoding,
                on_bad_lines="skip",
                dtype={2: str, 4: float, 7: float},
            )
        except UnicodeDecodeError:
            encoding = "cp863"
            df = pd.read_csv(
                file,
                sep=self.FILE_COL_DELIM,
                names=self.FILE_COL_NAMES,
                encoding=encoding,
                on_bad_lines="skip",
                dtype={2: str, 4: float, 7: float},
            )
        except Exception:
            encoding = self.get_file_encoding(file)
            df = pd.read_csv(
                file,
                sep=self.FILE_COL_DELIM,
                names=self.FILE_COL_NAMES,
                encoding=encoding,
                on_bad_lines="skip",
                dtype={
                    2: str,
                    4: float,
                    7: float,
                },
            )
        return df

    def _read_files(self, files, vars_to_retrieve):
        """
        Read input variables from list of files

        Parameters
        ----------
        files : list
            list of data files
        vars_to_retrieve : list
            list of variables to retrieve

        Raises
        ------
        NotImplementedError
            if several timezones are assigned to the same station
        AttributeError
            if data unit is unknown

        Returns
        -------
        stats : list
            list of StationData objects

        """
        logger.info("Read AirNow data file(s)")
        file_vars_to_retrieve = [self.VAR_MAP[x] for x in vars_to_retrieve]

        arrs = []
        unique_stat_ids = None
        for i in tqdm(range(len(files)), disable=None):
            fp = files[i]
            filedata = self._read_file(fp)
            for i, filevar in enumerate(file_vars_to_retrieve):
                arrs.append(filedata[filedata["variable"] == filevar].values)
                if unique_stat_ids is None:
                    unique_stat_ids = np.unique(
                        arrs[-1][:, self.FILE_COL_NAMES.index("station_id")]
                    )
                else:
                    try:
                        unique_stat_ids = np.union1d(
                            unique_stat_ids,
                            np.unique(arrs[-1][:, self.FILE_COL_NAMES.index("station_id")]),
                        )
                    except (ValueError, TypeError):
                        print(arrs[-1][:, self.FILE_COL_NAMES.index("station_id")])
                        raise DataRetrievalError(
                            f"file {fp}: error in creating unique stationlist"
                        )
        if len(arrs) == 0:
            raise DataRetrievalError("None of the input variables could be found in input list")
        return self._filedata_to_statlist(arrs, vars_to_retrieve, unique_stat_ids=unique_stat_ids)

    def _filedata_to_statlist(
        self,
        arrs: list[np.ndarray],
        vars_to_retrieve: list[str],
        unique_stat_ids: list[str] = None,
    ) -> list[StationData]:
        """
        Convert loaded filedata into list of StationData objects

        Parameters
        ----------
        arrs : list
            list of numpy arrays extracted from each file
            (see :func:`_read_files`).
        vars_to_retrieve : list
            list of variables to be retrieved from input data.


        Returns
        -------
        stats : list
            list of :class:`StationData` objects, one for each var and station.
            :type unique_stat_ids: object

        """
        # doubling of RAM usage!
        data = np.concatenate(arrs)
        # so kill the input data right afterwards
        arrs = None

        logger.info("Converting filedata to list of StationData")
        stat_meta = self.station_metadata
        stat_ids = list(stat_meta)
        varcol = self.FILE_COL_NAMES.index("variable")
        statcol = self.FILE_COL_NAMES.index("station_id")
        tzonecol = self.FILE_COL_NAMES.index("time_zone")
        unitcol = self.FILE_COL_NAMES.index("unit")
        valcol = self.FILE_COL_NAMES.index("value")

        stats = []
        # shortcut for limited testing dataset because the code
        # below the try statement fails with testing:
        # E               ValueError: cannot call `vectorize` on size 0 inputs unless `otypes` is set
        # ../../../mambaforge/envs/pyadev-applied/lib/python3.11/site-packages/numpy/lib/function_base.py:2363: ValueError
        try:
            dtime = self.make_datetime64_array(data[:, 0], data[:, 1])
        except ValueError:
            raise DataRetrievalError("None of the input variables could be found in input list")

        for var in vars_to_retrieve:
            # extract only variable data (should speed things up)
            var_in_file = self.VAR_MAP[var]
            mask = data[:, varcol] == var_in_file
            # another RAM consuming op, the mask can just be used all the time (for the price of readability...)
            subset = data[mask]
            dtime_subset = dtime[mask]
            # there are stations with a all numeric station ID, but type hints in pd.read_csv made sure
            # they are read as str...
            if unique_stat_ids is None:
                statlist = np.unique(subset[:, statcol])
            else:
                statlist = unique_stat_ids
            for stat_id in tqdm(statlist, desc=var, disable=None):
                if stat_id not in stat_ids:
                    continue
                statmask = subset[:, statcol] == stat_id
                if statmask.sum() == 0:
                    continue
                # RAM consuming op...
                statdata = subset[statmask]
                timestamps = dtime_subset[statmask]
                # timezone offsets (there's a half hour time zone!, so float)
                # not sure why the astype(float) is needed in between, but it does not work without...
                toffs = statdata[:, tzonecol].astype(float).astype("timedelta64[h]")
                timestamps += toffs
                stat = StationData(**stat_meta[stat_id])

                vals = statdata[:, valcol]
                units = np.unique(statdata[:, unitcol])
                # errors that did not occur in v0 but that may occur
                assert len(units) == 1
                assert units[0] in self.UNIT_MAP
                stat["dtime"] = timestamps
                stat["timezone"] = "UTC"
                stat[var] = vals
                unit = self.UNIT_MAP[units[0]]
                stat["var_info"][var] = dict(units=unit)
                stats.append(stat)
        return stats

    def read_file(self, filename, vars_to_retrieve=None):
        """
        This method is returns just the raw content of a file as a dict

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects

        Returns
        -------
        StationData
            dict-like object containing results

        Raises
        ------
        NotImplementedError
        """

        # unfortunately the files have different encodings, so we have to try them
        # on the entire file first
        ret_data = {}
        encoding = "utf_8"
        try:
            with open(filename, encoding=encoding) as infile:
                linedata = infile.readlines()
        except UnicodeDecodeError:
            encoding = "cp863"
            with open(filename, encoding=encoding) as infile:
                linedata = infile.readlines()
        except Exception:
            logger.info(f"unforeseen encoding in file {filename}! Trying to determine encoding")
            try:
                encoding = self.get_file_encoding(filename)
                logger.info(f"determined encoding: {encoding}")
                with open(filename, encoding=encoding) as infile:
                    linedata = infile.readlines()
            except MemoryError:
                logger.info("could not determine encoding due to MemoryError: Skipping file...")
                raise DataRetrievalError(
                    "could not determine encoding due to MemoryError: Skipping file..."
                )
                return ret_data

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        file_vars_to_retrieve = [self.VAR_MAP[x] for x in vars_to_retrieve]

        tot_lines_retrieved = 0
        for var in vars_to_retrieve:
            ret_data[var] = {}
            ret_data[var]["lines_retrieved"] = 0
            ret_data[var]["linedata"] = []

            for line in linedata:
                line_arr = line.split(self.FILE_COL_DELIM)
                # skip malformed lines
                if len(line_arr) != self.FILE_COL_ROW_NUMBER:
                    continue
                # skip lines that do not contain data of an interesting variable
                if line_arr[self.ROW_VAR_COL] not in file_vars_to_retrieve:
                    continue

                # make the numerical values numerical here already
                line_arr[4] = float(line_arr[4])
                line_arr[7] = float(line_arr[7])
                ret_data[var]["linedata"].append(line_arr)
                ret_data[var]["lines_retrieved"] += 1
                tot_lines_retrieved += 1
        return ret_data

    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):
        """
        Read variable data

        Parameters
        ----------
        vars_to_retrieve : str or list, optional
            List of variables to be retrieved. The default is None.
        first_file : int, optional
            Index of first file to be read. The default is None, in which case
            index 0 in file list is used.
        last_file : int, optional
            Index of last file to be read. The default is None, in which case
            last index in file list is used.

        Returns
        -------
        data : UngriddedData
            loaded data object.

        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        self._init_station_metadata()
        files = self.get_file_list()
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]

        stats = self._read_files(files, vars_to_retrieve)

        data = UngriddedData.from_station_data(
            stats, add_meta_keys=["timezone", "area_classification", "station_classification"]
        )

        return data

    # the following has been stolen from
    # https://stackoverflow.com/questions/44402983/how-to-read-the-file-without-encoding-and-extract-desired-urls-with-python3
    def get_file_bom_encoding(self, filename):
        with open(filename, "rb") as openfileobject:
            line = str(openfileobject.readline())
            if line[2:14] == str(codecs.BOM_UTF8).split("'")[1]:
                return "utf_8"
            if line[2:10] == str(codecs.BOM_UTF16_BE).split("'")[1]:
                return "utf_16"
            if line[2:10] == str(codecs.BOM_UTF16_LE).split("'")[1]:
                return "utf_16"
            if line[2:18] == str(codecs.BOM_UTF32_BE).split("'")[1]:
                return "utf_32"
            if line[2:18] == str(codecs.BOM_UTF32_LE).split("'")[1]:
                return "utf_32"
        return ""

    def get_all_file_encodings(self, filename):
        encoding_list = []
        encodings = (
            "utf_8",
            "cp863",
            "utf_16",
            "utf_16_le",
            "utf_16_be",
            "utf_32",
            "utf_32_be",
            "utf_32_le",
            "cp850",
            "cp437",
            "cp852",
            "cp1252",
            "cp1250",
            "ascii",
            "utf_8_sig",
            "big5",
            "big5hkscs",
            "cp037",
            "cp424",
            "cp500",
            "cp720",
            "cp737",
            "cp775",
            "cp855",
            "cp856",
            "cp857",
            "cp858",
            "cp860",
            "cp861",
            "cp862",
            "cp864",
            "cp865",
            "cp866",
            "cp869",
            "cp874",
            "cp875",
            "cp932",
            "cp949",
            "cp950",
            "cp1006",
            "cp1026",
            "cp1140",
            "cp1251",
            "cp1253",
            "cp1254",
            "cp1255",
            "cp1256",
            "cp1257",
            "cp1258",
            "euc_jp",
            "euc_jis_2004",
            "euc_jisx0213",
            "euc_kr",
            "gb2312",
            "gbk",
            "gb18030",
            "hz",
            "iso2022_jp",
            "iso2022_jp_1",
            "iso2022_jp_2",
            "iso2022_jp_2004",
            "iso2022_jp_3",
            "iso2022_jp_ext",
            "iso2022_kr",
            "latin_1",
            "iso8859_2",
            "iso8859_3",
            "iso8859_4",
            "iso8859_5",
            "iso8859_6",
            "iso8859_7",
            "iso8859_8",
            "iso8859_9",
            "iso8859_10",
            "iso8859_13",
            "iso8859_14",
            "iso8859_15",
            "iso8859_16",
            "johab",
            "koi8_r",
            "koi8_u",
            "mac_cyrillic",
            "mac_greek",
            "mac_iceland",
            "mac_latin2",
            "mac_roman",
            "mac_turkish",
            "ptcp154",
            "shift_jis",
            "shift_jis_2004",
            "shift_jisx0213",
        )
        for e in encodings:
            try:
                fh = codecs.open(filename, "r", encoding=e)
                fh.readlines()
            except UnicodeDecodeError:
                fh.close()
            except UnicodeError:
                fh.close()
            else:
                encoding_list.append([e])
                fh.close()
                continue
        return encoding_list

    def get_file_encoding(self, filename):
        file_encoding = self.get_file_bom_encoding(filename)
        if file_encoding != "":
            return file_encoding
        encoding_list = self.get_all_file_encodings(filename)
        file_encoding = str(encoding_list[0][0])
        if file_encoding[-3:] == "_be" or file_encoding[-3:] == "_le":
            file_encoding = file_encoding[:-3]
        return file_encoding
