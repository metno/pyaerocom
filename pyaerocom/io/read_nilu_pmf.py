import fnmatch
import glob
import logging
import os
import re
from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd
from geonum.atmosphere import T0_STD, p0
from tqdm import tqdm

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.aux_var_helpers import (
    calc_vmro3max,
    compute_ac550dryaer,
    compute_ang4470dryaer_from_dry_scat,
    compute_sc440dryaer,
    compute_sc550dryaer,
    compute_sc700dryaer,
    compute_wetoxn_from_concprcpoxn,
    compute_wetoxs_from_concprcpoxs,
    compute_wetrdn_from_concprcprdn,
    concx_to_vmrx,
    vmrx_to_concx,
)
from pyaerocom.exceptions import (
    EbasFileError,
    MetaDataError,
    NotInFileError,
    TemporalResolutionError,
    TemporalSamplingError,
    UnitConversionError,
)
from pyaerocom.io.ebas_file_index import EbasFileIndex, EbasSQLRequest
from pyaerocom.io.ebas_nasa_ames import EbasFlagCol, EbasNasaAmesFile
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.helpers import _check_ebas_db_local_vs_remote
from pyaerocom.io.read_ebas import ReadEbas, ReadEbasOptions
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.molmasses import get_molmass
from pyaerocom.stationdata import StationData
from pyaerocom.tstype import TsType
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units_helpers import get_unit_conversion_fac

logger = logging.getLogger(__name__)


class ECFile:

    _HEAD_ROWS_MANDATORY = [0, 5, 8, 9, 10, 11]

    CONV_STR = lambda self, l: str(l.strip())
    CONV_PI = lambda self, l: "; ".join([x.strip() for x in l.split(";")])
    CONV_MULTIINT = lambda self, l: [int(x) for x in l.strip().split()]
    CONV_MULTIFLOAT = lambda self, l: [float(x) for x in l.strip().split()]
    CONV_INT = lambda self, l: int(l.strip())
    CONV_FLOAT = lambda self, l: float(l.strip())
    _STARTDATE_FMT = "%Y%m%d"

    meta_data = {
        "pi": "",
        "station_name": "",
        "station_code": "",
        "units": {"eBC_bb": "", "eBC_ff": "", "EBC": "", "Fraction": "1"},
        "start_date": "",
        "dtime": [],
        "revision_date": "",
        "station_latitude": -1,
        "station_longitude": -1,
        "station_altitude": -1,
        "missing_val": [],
        "resolution_code": "1h",
        "data_level": 3,
        "variables": ["eBC_bb", "eBC_ff", "EBC", "Fraction"],
        "matrix": "aerosol",
    }

    data = {}

    site_map = {
        "Berlin_Am": "",
        "Berlin_Fr": "",
        "Berlin_Na": "",
    }

    def __init__(self, file: str, sites_file: str) -> None:
        self.file = file
        self.sites_file = sites_file
        self._read_fastit()
        self._read_sites_file()

    def _read_fastit(self):
        path = "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/nilu_pmf/EIMPs_winter2017-2018_data/fasit.txt"
        self.fasit = {}
        with open(path) as f:
            for line in f:
                if len(line) > 1:
                    self.fasit[line.split()[1]] = float(line.split()[0])

    def read_file(self):
        with open(self.file) as f:
            [nb_header, _] = [int(i) for i in f.readline().split(",")]
            full_file = f.read().split("\n")

            header = full_file[: nb_header - 2]

            data = full_file[nb_header - 2 :]

        self._read_header(header)
        self._read_data(data)

    def _read_sites_file(self):
        df = pd.read_excel(self.sites_file)

        self.sites_df = df

    def _read_data(self, data):

        self.data["header"] = "Babs_bb   Babs_ff    eBC_ff    eBC_bb".split()
        # "Babs_bb   Babs_ff    eBC_ff    eBC_bb".split()  # data[0].split()[2:]

        data = [[float(i) for i in d.split()] for d in data[1:]]
        for i, d in enumerate(data):
            if len(d) == 0:
                data.pop(i)
        data = np.array(data)

        time = [
            pd.Timestamp(self.meta_data["start_date"] + timedelta(days=i))
            .round("60min")
            .to_pydatetime()
            for i in data[:, 0]
        ]

        data = data[:, 2:]
        s = data.shape
        new_data = np.zeros((s[0], s[1] + 2))
        for i, d in enumerate(data):
            # new_data[i, :-2] = np.where(np.isclose(d, self.meta_data["missing_val"]), np.nan, d)
            tmp = d
            tmp = np.where(np.isclose(tmp, self.meta_data["missing_val"]), np.nan, tmp)
            if np.isnan(tmp).any():
                tmp = np.ones_like(tmp) * np.nan
            new_data[i, :-2] = tmp
            ebc_data = (
                new_data[i, self.data["header"].index("eBC_bb")]
                + new_data[i, self.data["header"].index("eBC_ff")]
            )
            frac = new_data[i, self.data["header"].index("eBC_bb")] / ebc_data
            new_data[i, -2] = ebc_data
            new_data[i, -1] = frac

        self.data["header"].append("EBC")
        self.data["header"].append("Fraction")

        self.data["data"] = new_data
        # print("----------------------- \n")
        # print(self.meta_data["station_name"])
        # print(np.nanmean(new_data[:, 2]) / np.nanmean(new_data[:, 4]))
        # print(np.nanmean(new_data[:, 5]))
        # print("------------------------------------")
        # print("----------------------- \n")
        # print(self.meta_data["station_name"])
        # print(
        #     np.isclose(
        #         np.nanmean(new_data[:, self.data["header"].index("eBC_bb")])
        #         / np.nanmean(new_data[:, 4]),
        #         self.fasit[self.meta_data["station_name"]],
        #         rtol=0.05,
        #     )
        # )
        # print(
        #     np.nanmean(new_data[:, self.data["header"].index("eBC_bb")])
        #     / np.nanmean(new_data[:, 4]),
        #     self.fasit[self.meta_data["station_name"]],
        # )
        self.data["time"] = time

        self.meta_data["dtime"] = np.array([t.timestamp() for t in time])

    def _read_header(self, header: List[str]):
        self.meta_data["pi"] = self.CONV_PI(header[0])
        self.meta_data["station_name"] = self.CONV_STR(header[17].split(":")[1])
        self.meta_data["units"]["eBC_bb"] = self.CONV_STR(header[14].split(",")[1])
        self.meta_data["units"]["eBC_ff"] = self.CONV_STR(header[15].split(",")[1])
        self.meta_data["units"]["EBC"] = self.meta_data["units"]["eBC_ff"]

        self.meta_data["station_latitude"] = self.CONV_FLOAT(header[18].split(":")[1])
        self.meta_data["station_longitude"] = self.CONV_FLOAT(header[19].split(":")[1])
        self.meta_data["station_altitude"] = self.CONV_FLOAT(header[20].split(":")[1].strip()[:-1])

        # lon_filtered = self.sites_df.loc[abs(self.sites_df["long"] - self.meta_data["lon"]) < 0.01]

        # lat_filtered = lon_filtered.loc[abs(lon_filtered["lat"] - self.meta_data["lat"]) < 0.01]

        # assert (
        #     len(lat_filtered["EBAS code"]) == 1
        # ), f'{lat_filtered["EBAS code"]}, {self.meta_data["station_name"]}'
        # self.meta_data["station_code"] = list(lat_filtered["EBAS code"])[0]

        self.meta_data["start_date"] = datetime.strptime(
            "".join(header[5].split()[:3]), self._STARTDATE_FMT
        )
        self.meta_data["revision_date"] = datetime.strptime(
            "".join(header[5].split()[3:]), self._STARTDATE_FMT
        )

        self.meta_data["missing_val"] = np.array(self.CONV_MULTIFLOAT(header[10]))[1:]


class ReadNILUPMF(ReadUngriddedBase):
    """Interface for reading EBAS data

    Parameters
    ----------
    data_id
        string specifying either of the supported datasets that are defined
        in ``SUPPORTED_DATASETS``
    data_dir : str
        directory where data is located (NOTE: needs to point to the
        directory that contains the "ebas_file_index.sqlite3" file and not
        to the underlying directory "data" which contains the actual
        NASA Ames files.)

    TODO
    ----
    - Check for negative values vs. detection limit
    - Read uncertainties from percentiles (where available)
    """

    #: version log of this class (for caching)
    __version__ = "0.01_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.NILU_PMF_NAME

    #: File mask
    _FILEMASK = "*.nas"

    #: Name of subdirectory containing data files (relative to
    #: :attr:`data_dir`)
    FILE_SUBDIR_NAME = ""

    #: Name of sqlite database file
    # SQL_DB_NAME = "ebas_file_index.sqlite3"

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.NILU_PMF_NAME]

    #: For the following data IDs, the sqlite database file will be cached if
    #: const.EBAS_DB_LOCAL_CACHE is True
    # CACHE_SQLITE_FILE = [const.EBAS_MULTICOLUMN_NAME]

    TS_TYPE = "undefined"

    MERGE_STATIONS = {
        # "Birkenes": "Birkenes II",
        # "Rörvik": "Råö",
        # "Vavihill": "Hallahus",
        # "Virolahti II": "Virolahti III",
    }
    #'Trollhaugen'    : 'Troll'}
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

    PROVIDED_VARS = dict(
        concecff="eBC_bb",
        concecbb="eBC_ff",
        concebc="EBC",
        ebcfrac="Fraction",
        concoc="OC",
        concec="EC",
        conclevoglucosan="levoglucosan",
    )

    PROVIDED_VARS_REV = dict(
        eBC_bb="concecbb",
        eBC_ff="concecff",
        EBC="concebc",
        Fraction="ebcfrac",
        OC="concoc",
        EC="concec",
        levoglucosan="conclevoglucosan",
    )

    #: variables required for computation of auxiliary variables
    AUX_REQUIRES = {}

    #: Meta information supposed to be migrated to computed variables
    AUX_USE_META = {}
    #: Functions supposed to be used for computation of auxiliary variables
    AUX_FUNS = {}

    #: Custom reading options for individual variables. Keys need to be valid
    #: attributes of :class:`ReadEbasOptions` and anything specified here (for
    #: a given variable) will be overwritten from the defaults specified in
    #: the options class.
    VAR_READ_OPTS = {}

    #: list of EBAS data files that are flagged invalid and will not be imported
    IGNORE_FILES = []

    #: Ignore data columns in NASA Ames files that contain any of the listed
    #: attributes
    IGNORE_COLS_CONTAIN = ["fraction", "artifact"]

    def __init__(self, data_id=None, data_dir=None):

        super().__init__(data_id=data_id, data_dir=data_dir)

        self._opts = {"default": ReadEbasOptions()}

        # self.opts = ReadEbasOptions()
        #: loaded instances of aerocom variables (instances of
        #: :class:`Variable` object, is written in get_file_list
        self._loaded_aerocom_vars = {}

        #: loaded instances of variables in EBAS namespace (instances of
        #: :class:`EbasVarInfo` object, is updated in read_file
        self._loaded_ebas_vars = {}

        self._file_dir = None

        self.files_failed = []
        self._read_stats_log = BrowseDict()

        #: Originally retrieved file lists from SQL database, for each variable
        #: individually
        self._lists_orig = {}

        #: this is filled in method get_file_list and specifies variables
        #: to be read from each file
        self.files_contain = []

        self._all_stats = None

    @property
    def PROVIDES_VARIABLES(self):
        """List of variables provided by the interface"""
        return self.PROVIDED_VARS

    @property
    def DEFAULT_VARS(self):
        """
        list: list of default variables to be read

        Note
        ----
        Currently a wrapper for :attr:`PROVIDES_VARIABLES`
        """
        return self.PROVIDES_VARIABLES

    @property
    def file_dir(self):
        """Directory containing EBAS NASA Ames files"""
        if self._file_dir is not None:
            return self._file_dir
        return os.path.join(self.data_dir, self.FILE_SUBDIR_NAME)

    @file_dir.setter
    def file_dir(self, val):
        if not isinstance(val, str) or not os.path.exists(val):
            raise FileNotFoundError("Input directory does not exist")
        self._file_dir = val

    def read(
        self, vars_to_retrieve=None, first_file=None, last_file=None, files=None, **constraints
    ):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file
            in the list is used
        files : list
             list of files
        **constraints
            further reading constraints deviating from default (default
            info for each AEROCOM variable can be found in `ebas_config.ini <
            https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/
            ebas_config.ini>`__). For details on possible input parameters
            see :class:`EbasSQLRequest` (or `this tutorial <http://aerocom.met.no
            /pyaerocom/tutorials.html#ebas-file-query-and-database-browser>`__)

        Returns
        -------
        UngriddedData
            data object
        """
        vars_to_retrieve = self._precheck_vars_to_retrieve(vars_to_retrieve)
        # check_vars_to_retrieve is implemented in template base class
        (vars_to_read, vars_to_compute) = self.check_vars_to_retrieve(vars_to_retrieve)

        all_vars = vars_to_read + vars_to_compute

        constraints = {}  # self._init_read_opts(all_vars, constraints)

        if files is None:
            self.get_file_list(vars_to_retrieve, **constraints)
            files = self.files

        else:
            if isinstance(files, str):  # single file
                files = [files]
            files_contain = [vars_to_retrieve] * len(files)

        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]

        data = self._read_files(files, vars_to_retrieve, constraints)
        data.clear_meta_no_data()

        return data

    def _read_files(self, files, vars_to_retrieve, constraints):
        """Helper that reads list of files into UngriddedData

        Note
        ----
        This method is not supposed to be called directly but is used in
        :func:`read` and serves the purpose of parallel loading of data
        """
        self.files_failed = []
        data_obj = UngriddedData(num_points=1000000)

        # # Add reading options to filter "history of UngriddedDataObject"
        filters = {}
        filters.update(constraints)
        data_obj._add_to_filter_history(filters)

        meta_key = 0.0
        idx = 0

        # assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        # counter that is updated whenever a new variable appears during read
        # (is used for attr. var_idx in UngriddedData object)
        var_count_glob = -1
        logger.info(f"Reading NILU data from {self.file_dir}")
        num_files = len(files)
        for i in tqdm(range(num_files)):
            _file = files[i]

            station_data = self.read_file(_file)

            # try:
            #     station_data = self.read_file(_file)

            # except (
            #     NotInFileError,
            #     EbasFileError,
            #     TemporalResolutionError,
            #     TemporalSamplingError,
            # ) as e:
            #     self.files_failed.append(_file)
            #     self.logger.warning(f"Skipping reading of NILU file: {_file}. Reason: {repr(e)}")
            #     continue
            # except Exception as e:
            #     self.files_failed.append(_file)
            #     logger.warning(f"Skipping reading of NILU file: {_file}. Reason: {repr(e)}")
            #     continue

            # Fill the metatdata dict
            # the location in the data set is time step dependent!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = {}
            metadata[meta_key].update(station_data.get_meta(add_none_vals=True))

            if "station_name_orig" in station_data:
                metadata[meta_key]["station_name_orig"] = station_data["station_name_orig"]

            metadata[meta_key]["data_revision"] = self.data_revision
            metadata[meta_key]["var_info"] = {}
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            meta_idx[meta_key] = {}

            num_times = len(station_data["dtime"])

            contains_vars = list(station_data.var_info)
            # access array containing time stamps
            # TODO: check using index instead (even though not a problem here
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data["dtime"])

            append_vars = [x for x in np.intersect1d(vars_to_retrieve, contains_vars)]

            totnum = num_times * len(append_vars)
            # check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                # if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)

            for var_count, var in enumerate(append_vars):
                # data values
                values = station_data[var]

                # get start / stop index for this data vector
                start = idx + var_count * num_times
                stop = start + num_times

                if not var in data_obj.var_idx:
                    var_count_glob += 1
                    var_idx = var_count_glob
                    data_obj.var_idx[var] = var_idx
                else:
                    var_idx = data_obj.var_idx[var]

                # write common meta info for this station (data lon, lat and
                # altitude are set to station locations)
                data_obj._data[start:stop, data_obj._LATINDEX] = station_data["latitude"]
                data_obj._data[start:stop, data_obj._LONINDEX] = station_data["longitude"]
                data_obj._data[start:stop, data_obj._ALTITUDEINDEX] = station_data["altitude"]
                data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key

                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times

                data_obj._data[start:stop, data_obj._DATAINDEX] = values

                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                if var in station_data.data_flagged:
                    invalid = station_data.data_flagged[var]
                    data_obj._data[start:stop, data_obj._DATAFLAGINDEX] = invalid
                if var in station_data.data_err:
                    errs = station_data.data_err[var]
                    data_obj._data[start:stop, data_obj._DATAERRINDEX] = errs

                var_info = station_data["var_info"][var]
                metadata[meta_key]["var_info"][var] = {}
                metadata[meta_key]["var_info"][var].update(var_info)
                meta_idx[meta_key][var] = np.arange(start, stop)

            metadata[meta_key]["variables"] = append_vars
            idx += totnum
            meta_key += 1

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]

        num_failed = len(self.files_failed)
        if num_failed > 0:
            logger.warning(f"{num_failed} out of {num_files} could not be read...")
        return data_obj

    def read_file(
        self, filename, vars_to_retrieve=None, _vars_to_read=None, _vars_to_compute=None
    ):
        """Read EBAS NASA Ames file

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read, if None (and if not
            both of the alternative possible parameters ``_vars_to_read`` and
            ``_vars_to_compute`` are specified explicitely) then the default
            settings are used

        Returns
        -------
        StationData
            dict-like object containing results
        """
        # implemented in base class
        # if _vars_to_read is None or _vars_to_compute is None:
        #     (vars_to_read, vars_to_compute) = self.check_vars_to_retrieve(vars_to_retrieve)
        # else:
        #     vars_to_read, vars_to_compute = _vars_to_read, _vars_to_compute

        file_reader = ECFile

        file = file_reader(
            filename,
            sites_file="/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/nilu_pmf/EIMPs_winter2017-2018_data/Sites_EBC-campaign.xlsx",
        )
        file.read_file()

        data_out = StationData()

        data_out = self._add_meta(data_out, file)

        freq_ebas = data_out["ts_type"]  # resolution code
        # store the raw EBAS meta dictionary (who knows what for later ;P )
        # data_out['ebas_meta'] = meta
        data_out["var_info"] = {}
        for var in file.meta_data["variables"]:
            # opts = self.get_read_opts(var)
            data_out["var_info"][self.PROVIDED_VARS_REV[var]] = {}

            # _col = file.var_defs[colnum]
            var_index = file.data["header"].index(var)
            data = file.data["data"][:, var_index]

            # if opts.eval_flags:
            #     invalid = ~file.flag_col_info[_col.flag_col].valid
            #     data_out.data_flagged[var] = invalid

            meta = file.meta_data

            data_out[self.PROVIDED_VARS_REV[var]] = data

            data_out["var_info"][self.PROVIDED_VARS_REV[var]]["units"] = meta["units"][var]

            # var_info = _col.to_dict()
            # data_out["var_info"][var].update(var_info)

            # if opts.convert_units:
            #     try:
            #         data_out = self._convert_varunit_stationdata(data_out, var)
            #     except UnitConversionError:
            #         if opts.try_convert_vmr_conc:
            #             data_out = self._try_convert_vmr_conc(
            #                 data_out, var, var_info, file.meta
            #             )  # raises UnitConversionError if it is not possible
            #         else:
            #             raise

        if len(data_out["var_info"]) == 0:
            raise EbasFileError(
                f"All data columns of specified input variables are NaN in {filename}"
            )

        dtime = file.meta_data["dtime"]

        data_out["dtime"] = dtime
        data_out["start_meas"] = file.data["time"][0]
        data_out["stop_meas"] = file.data["time"][-1]

        # if self.readopts_default.ensure_correct_freq:
        #     self._flag_incorrect_frequencies(data_out)
        return data_out

    def _add_meta(self, data_out, file: ECFile):
        meta = file.meta_data
        name = meta["station_name"].replace("/", ";")

        # data_out["framework"] = file.project_association
        data_out["filename"] = os.path.basename(file.file)
        data_out["data_id"] = self.data_id
        data_out["PI"] = meta["pi"]
        data_out["station_id"] = meta["station_code"]
        data_out["set_type_code"] = "Surface"
        data_out["station_name"] = name
        # if name in self.MERGE_STATIONS:
        #     data_out["station_name"] = self.MERGE_STATIONS[name]
        #     data_out["station_name_orig"] = name
        # else:
        #     data_out["station_name"] = name

        # write meta information
        tres_code = meta["resolution_code"]
        try:
            ts_type = self.TS_TYPE_CODES[tres_code]
        except KeyError:
            ival = re.findall(r"\d+", tres_code)[0]
            code = tres_code.split(ival)[-1]
            if not code in self.TS_TYPE_CODES:
                raise NotImplementedError(f"Cannot handle EBAS resolution code {tres_code}")
            ts_type = ival + self.TS_TYPE_CODES[code]
            self.TS_TYPE_CODES[tres_code] = ts_type

        data_out["ts_type"] = ts_type
        # altitude of station
        try:
            altitude = float(meta["station_altitude"])
        except Exception:
            altitude = np.nan
        try:
            meas_height = float(meta["measurement_height"].split(" ")[0])
        except KeyError:
            meas_height = 0.0

        data_alt = altitude + meas_height

        # file specific meta information
        # data_out.update(meta)
        data_out["latitude"] = float(meta["station_latitude"])
        data_out["longitude"] = float(meta["station_longitude"])
        data_out["altitude"] = data_alt
        data_out["meas_height"] = meas_height
        data_out["station_altitude"] = altitude

        # data_out["instrument_name"] = meta["instrument_name"]
        # data_out["instrument_type"] = meta["instrument_type"]

        data_out["matrix"] = meta["matrix"]
        data_out["revision_date"] = meta["revision_date"]

        setting, land_use, gaw_type, lev = None, None, None, None
        if "station_setting" in meta:
            setting = meta["station_setting"]

        if "station_land_use" in meta:
            land_use = meta["station_land_use"]

        if "station_gaw_type" in meta:
            gaw_type = meta["station_gaw_type"]

        if "data_level" in meta:
            try:
                lev = int(meta["data_level"])
            except Exception:
                pass

        data_out["station_setting"] = setting
        data_out["station_land_use"] = land_use
        data_out["station_gaw_type"] = gaw_type

        # NOTE: may be also defined per column in attr. var_defs

        data_out["data_level"] = lev

        return data_out

    def _precheck_vars_to_retrieve(self, vars_to_retrieve):
        """
        Make sure input variables are supported and are only provided once

        Parameters
        ----------
        vars_to_retrieve : str or list, or similar
            make sure input variable names are in AeroCom convention

        Raises
        ------
        ValueError
            if the same variable is input more than one time
        VariableDefinitionError
            if one of the input variables is not supported

        Returns
        -------
        list
            list of variables to be retrieved
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        out = []
        for var in vars_to_retrieve:
            out.append(self.var_info(var).var_name_aerocom)
        return out

    def var_info(self, var_name):
        """Aerocom variable info for input var_name"""
        if not var_name in self._loaded_aerocom_vars:
            self._loaded_aerocom_vars[var_name] = const.VARS[var_name]
        return self._loaded_aerocom_vars[var_name]


if __name__ == "__main__":
    path = "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/nilu_pmf/EIMPs_winter2017-2018_data/EIMPs_winter2017_2018_absorption_PMF"
    sites_file = "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/obs/nilu_pmf/EIMPs_winter2017-2018_data/Sites_EBC-campaign.xlsx"
    for file in glob.glob(f"{path}/*.nas"):
        ecfile = ECFile(file, sites_file)
        ecfile.read_file()
