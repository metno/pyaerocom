import gzip
import logging
import os
import pathlib
import shutil
import tempfile

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.aux_var_helpers import calc_ang4487aer, calc_od550aer, calc_od550lt1ang
from pyaerocom.exceptions import AeronetReadError
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom.stationdata import StationData

logger = logging.getLogger(__name__)


class ReadAeronetSunV3(ReadAeronetBase):
    """Interface for reading Aeronet direct sun version 3 Level 1.5 and 2.0 data

    .. seealso::

        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`

    """

    #: Mask for identifying datafiles
    _FILEMASK = "*.lev*"

    #: version log of this class (for caching)
    __version__ = "0.12_" + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_SUN_V3L2_AOD_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [
        const.AERONET_SUN_V3L15_AOD_DAILY_NAME,
        const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME,
        const.AERONET_SUN_V3L2_AOD_DAILY_NAME,
        const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME,
    ]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {
        const.AERONET_SUN_V3L15_AOD_DAILY_NAME: "daily",
        const.AERONET_SUN_V3L2_AOD_DAILY_NAME: "daily",
    }

    #: default variables for read method
    DEFAULT_VARS = ["od550aer", "ang4487aer"]

    #: value corresponding to invalid measurement
    # NAN_VAL = -9999.
    NAN_VAL = -999.0

    #: Mappings for identifying variables in file
    VAR_PATTERNS_FILE = {"AOD_([0-9]*)nm": "od*aer"}

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE["od340aer"] = "AOD_340nm"
    VAR_NAMES_FILE["od440aer"] = "AOD_440nm"
    VAR_NAMES_FILE["od500aer"] = "AOD_500nm"
    # VAR_NAMES_FILE['od865aer'] = 'AOD_865nm'
    VAR_NAMES_FILE["od870aer"] = "AOD_870nm"
    VAR_NAMES_FILE["ang4487aer"] = "440-870_Angstrom_Exponent"

    #: dictionary specifying the file column names (values) for each
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    META_NAMES_FILE["data_quality_level"] = "Data_Quality_Level"
    META_NAMES_FILE["instrument_number"] = "AERONET_Instrument_Number"
    META_NAMES_FILE["station_name"] = "AERONET_Site"
    META_NAMES_FILE["latitude"] = "Site_Latitude(Degrees)"
    META_NAMES_FILE["longitude"] = "Site_Longitude(Degrees)"
    META_NAMES_FILE["altitude"] = "Site_Elevation(m)"
    META_NAMES_FILE["date"] = "Date(dd:mm:yyyy)"
    META_NAMES_FILE["time"] = "Time(hh:mm:ss)"
    META_NAMES_FILE["day_of_year"] = "Day_of_Year"

    META_NAMES_FILE_ALT = {"AERONET_Site": ["AERONET_Site_Name"]}
    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {
        "ang44&87aer": ["od440aer", "od870aer"],
        "od550aer": ["od440aer", "od500aer", "ang4487aer"],
        "od550lt1ang": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550aerh2o": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550bc": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550dust": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550nh4": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550oa": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550so4": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550ss": ["od440aer", "od500aer", "ang4487aer"],
        "proxyod550no3": ["od440aer", "od500aer", "ang4487aer"],
        "proxyzaerosol": ["od440aer", "od500aer", "ang4487aer"],
        "proxyzdust": ["od440aer", "od500aer", "ang4487aer"],
    }

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {
        "ang44&87aer": calc_ang4487aer,
        "od550aer": calc_od550aer,
        "od550lt1ang": calc_od550lt1ang,
        "proxyod550aerh2o": calc_od550aer,
        "proxyod550bc": calc_od550aer,
        "proxyod550dust": calc_od550aer,
        "proxyod550nh4": calc_od550aer,
        "proxyod550oa": calc_od550aer,
        "proxyod550so4": calc_od550aer,
        "proxyod550ss": calc_od550aer,
        "proxyod550no3": calc_od550aer,
        "proxyzaerosol": calc_od550aer,
        "proxyzdust": calc_od550aer,
    }

    UNITS = {
        "proxyzdust": "km",
        "proxyzaerosol": "km",
    }

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE)

    def read_file(self, filename, vars_to_retrieve=None, vars_as_series=False):
        """Read Aeronet Sun V3 level 1.5 or 2 file

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
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        # create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.data_id
        # create empty arrays for meta information
        for item in self.META_NAMES_FILE:
            data_out[item] = []

        # Iterate over the lines of the file
        logger.info(f"Reading file {filename}")
        # enable alternative reading of .gz files here to save space on the file system
        suffix = pathlib.Path(filename).suffix
        tmp_name = filename
        if suffix == ".gz":
            f_out = tempfile.NamedTemporaryFile(delete=False)
            with gzip.open(filename, "r") as f_in:
                shutil.copyfileobj(f_in, f_out)
            filename = f_out.name
            f_out.close()

        try:
            with open(filename) as in_file:
                lines = in_file.readlines()
        except UnicodeDecodeError:
            with open(filename, encoding="ISO-8859-1") as in_file:
                lines = in_file.readlines()
        except OSError:
            # faulty gzip file, but also the gzip class raises some exceptions
            if suffix == ".gz":
                os.remove(f_out.name)
            raise AeronetReadError(f"gzip error in file {tmp_name}")

        _lines_ignored = []

        line_idx = 4
        _lines_ignored.append(lines[0 : line_idx - 1])

        # PI line
        dummy_arr = lines[line_idx].strip().split(";")
        line_idx += 1
        data_out["PI"] = dummy_arr[0].split("=")[1]
        data_out["PI_email"] = dummy_arr[1].split("=")[1]
        data_out["ts_type"] = self.TS_TYPE

        data_type_comment = lines[line_idx]
        line_idx += 1

        _lines_ignored.append(data_type_comment)
        logger.debug(f"Data type comment: {data_type_comment}")

        # put together a dict with the header string as key and the index number as value so that we can access
        # the index number via the header string
        col_index_str = lines[line_idx]
        line_idx += 1

        if col_index_str != self._last_col_index_str:
            logger.info("Header has changed, reloading col_index map")
            self._update_col_index(col_index_str)
        col_index = self.col_index

        # dependent on the station, some of the required input variables
        # may not be provided in the data file. These will be ignored
        # in the following list that iterates over all data rows and will
        # be filled below, with vectors containing NaNs after the file
        # reading loop
        vars_available = {}
        for var in vars_to_read:
            data_out[var] = []
            if var in col_index:
                vars_available[var] = col_index[var]
            else:
                logger.warning(
                    f"Variable {var} not available in file {os.path.basename(filename)}"
                )
        pl = None

        for i, line in enumerate(lines[line_idx:]):
            # process line
            dummy_arr = line.split(self.COL_DELIM)

            if pl is not None and len(dummy_arr) != len(pl):
                logger.warning(f"Data line {i} in {filename} is corrupt, skipping...")
                continue
            # copy the meta data (array of type string)
            for var in self.META_NAMES_FILE:
                try:
                    val = dummy_arr[col_index[var]]
                except IndexError as e:
                    logger.warning(repr(e))

                try:
                    # e.g. lon, lat, altitude
                    val = float(val)
                except Exception:
                    pass
                data_out[var].append(val)

            # This uses the numpy datestring64 functions that e.g. also
            # support Months as a time step for timedelta
            # Build a proper ISO 8601 UTC date string
            day, month, year = dummy_arr[col_index["date"]].split(":")
            datestring = "-".join([year, month, day])
            datestring = "T".join([datestring, dummy_arr[col_index["time"]]])
            # NOTE JGLISS: parsing timezone offset was removed on 22/2/19
            # since it is deprecated in recent numpy versions, for details
            # see https://www.numpy.org/devdocs/reference/arrays.datetime.html#changes-with-numpy-1-11
            # datestring = '+'.join([datestring, '00:00'])

            data_out["dtime"].append(np.datetime64(datestring))

            for var, idx in vars_available.items():
                val = np.float64(dummy_arr[idx])
                if val == self.NAN_VAL:
                    val = np.nan
                data_out[var].append(val)

            pl = dummy_arr

        # remove the temp file in case the input file was a gz file
        if suffix == ".gz":
            os.remove(f_out.name)

        # convert all lists to numpy arrays
        data_out["dtime"] = np.asarray(data_out["dtime"])

        for item in self.META_NAMES_FILE:
            data_out[item] = np.asarray(data_out[item])

        for var in vars_to_read:
            if var in vars_available:
                array = np.asarray(data_out[var])
            else:
                array = np.zeros(len(data_out["dtime"])) * np.nan
            data_out[var] = array

        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)

        # convert data vectors to pandas.Series (if applicable)
        if vars_as_series:
            for var in vars_to_read + vars_to_compute:
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var], index=data_out["dtime"])
                else:
                    del data_out[var]
        logger.debug(f"The following lines were ignored: {_lines_ignored}")
        return data_out
