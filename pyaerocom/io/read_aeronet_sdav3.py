import os
import logging

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.aux_var_helpers import calc_od550aer, calc_od550gt1aer, calc_od550lt1aer
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom.stationdata import StationData

logger = logging.getLogger(__name__)


class ReadAeronetSdaV3(ReadAeronetBase):
    """Interface for reading Aeronet Sun SDA V3 Level 1.5 and 2.0 data

    .. seealso::

        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`

    """

    #: Mask for identifying datafiles
    _FILEMASK = "*.lev30"

    #: version log of this class (for caching)
    __version__ = "0.08_" + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_SUN_V3L2_SDA_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [
        const.AERONET_SUN_V3L15_SDA_DAILY_NAME,
        const.AERONET_SUN_V3L2_SDA_DAILY_NAME,
    ]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {
        const.AERONET_SUN_V3L15_SDA_DAILY_NAME: "daily",
        const.AERONET_SUN_V3L2_SDA_DAILY_NAME: "daily",
    }

    #: default variables for read method
    DEFAULT_VARS = ["od550aer", "od550gt1aer", "od550lt1aer", "od550dust"]

    #: value corresponding to invalid measurement
    NAN_VAL = -999.0

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE["od500gt1aer"] = "Coarse_Mode_AOD_500nm[tau_c]"
    VAR_NAMES_FILE["od500lt1aer"] = "Fine_Mode_AOD_500nm[tau_f]"
    VAR_NAMES_FILE["od500aer"] = "Total_AOD_500nm[tau_a]"
    VAR_NAMES_FILE["ang4487aer"] = "Angstrom_Exponent(AE)-Total_500nm[alpha]"
    VAR_NAMES_FILE["od500dust"] = "Coarse_Mode_AOD_500nm[tau_c]"

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
    META_NAMES_FILE["date"] = "Date_(dd:mm:yyyy)"
    META_NAMES_FILE["time"] = "Time_(hh:mm:ss)"
    META_NAMES_FILE["day_of_year"] = "Day_of_Year"

    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {
        "od550aer": ["od500aer", "ang4487aer"],
        "od550gt1aer": ["od500gt1aer", "ang4487aer"],
        "od550dust": ["od500gt1aer", "ang4487aer"],
        "od550lt1aer": ["od500lt1aer", "ang4487aer"],
    }

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {
        "od550aer": calc_od550aer,
        "od550gt1aer": calc_od550gt1aer,
        "od550dust": calc_od550gt1aer,
        "od550lt1aer": calc_od550lt1aer,
    }

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE)

    def read_file(self, filename, vars_to_retrieve=None, vars_as_series=False):
        """Read Aeronet SDA V3 file and return it in a dictionary

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

        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []

        # Iterate over the lines of the file
        logger.info(f"Reading file {filename}")

        with open(filename) as in_file:
            # skip first 4 lines
            in_file.readline()
            in_file.readline()
            in_file.readline()
            in_file.readline()

            # PI line
            dummy_arr = in_file.readline().strip().split(";")
            data_out["PI"] = dummy_arr[0].split("=")[1]
            data_out["PI_email"] = dummy_arr[1].split("=")[1]
            data_out["ts_type"] = self.TS_TYPE

            # skip this line
            in_file.readline()

            # put together a dict with the header string as key and the index number as value so that we can access
            # the index number via the header string
            col_index_str = in_file.readline()
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
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    logger.warning(
                        f"Variable {var} not available in file {os.path.basename(filename)}"
                    )

            for line in in_file:
                # process line
                dummy_arr = line.split(self.COL_DELIM)

                # copy the meta data (array of type string)
                for var in self.META_NAMES_FILE:
                    val = dummy_arr[col_index[var]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except Exception:
                        pass
                    data_out[var].append(val)

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string

                day, month, year = dummy_arr[col_index["date"]].split(":")
                datestring = "-".join([year, month, day])
                datestring = "T".join([datestring, dummy_arr[col_index["time"]]])
                # NOTE JGLISS: parsing timezone offset was removed on 22/2/19
                # since it is deprecated in recent numpy versions, for details
                # see https://www.numpy.org/devdocs/reference/arrays.datetime.html#changes-with-numpy-1-11
                # datestring = '+'.join([datestring, '00:00'])

                data_out["dtime"].append(np.datetime64(datestring))

                # copy the data fields
                for var, idx in vars_available.items():
                    val = np.float64(dummy_arr[idx])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)

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

        return data_out
