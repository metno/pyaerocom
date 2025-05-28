import logging
import os
import warnings

import numpy as np
import pandas as pd

from pyaerocom.units.datetime import get_tot_number_of_seconds
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units import convert_unit

logger = logging.getLogger(__name__)


class ReadAasEtal(ReadUngriddedBase):
    """Read subset of GAW-TAD-EANET data related to Aas et al., 2019

    Paper URL: https://www.nature.com/articles/s41598-018-37304-0

    See Also
    ---------
    :class:`ReadUngriddedBase`
    """

    # name of files in GawTadSubsetAasEtAl
    _FILEMASK = "*.csv"  # fix

    #: version log of this class (for caching)
    __version__ = "0.09"

    COL_DELIM = ","

    #: Temporal resoloution
    TS_TYPE = "monthly"

    #: Name of dataset (OBS_ID)
    DATA_ID = "GAWTADsubsetAasEtAl"  #'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: value corresponding to invalid measurement
    # NAN_VAL = -9999.
    NAN_VAL = -999.0
    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    # This contains the mapping between the requested variables and what it is called in the files.

    COLNAMES_VARS = {}
    COLNAMES_VARS["concentration_mgS/L"] = ["concso4pr"]
    COLNAMES_VARS["concentration_ugS/m3"] = ["concso4", "concso2"]
    COLNAMES_VARS["precip_amount_mm"] = ["pr"]
    COLNAMES_VARS["deposition_kgS/ha"] = ["wetso4"]

    #: Dictionary mapping filenames to available variables in the respective files.
    FILES_CONTAIN = {}
    FILES_CONTAIN["monthly_so2.csv"] = ["concso2"]
    FILES_CONTAIN["monthly_so4_aero.csv"] = ["concso4"]
    FILES_CONTAIN["monthly_so4_precip.csv"] = ["wetso4", "pr", "concso4pr"]

    #: Dictionary mapping variable name to hard coded filenames.
    VARS_TO_FILES = {}
    VARS_TO_FILES["concso2"] = ["monthly_so2.csv"]
    VARS_TO_FILES["concso4"] = ["monthly_so4_aero.csv"]
    VARS_TO_FILES["pr"] = ["monthly_so4_precip.csv"]
    VARS_TO_FILES["wetso4"] = ["monthly_so4_precip.csv"]
    VARS_TO_FILES["concso4pr"] = ["monthly_so4_precip.csv"]

    # (from to unit)
    UNITCONVERSION = {
        "concso2": ("ug S/m3", "ug m-3"),
        "concso4": ("ug S/m3", "ug m-3"),
        "wetso4": ("kg S/ha", "kg m-2"),  #  s-1
        "concso4pr": ("mg S/L", "g m-3"),
    }

    # =============================================================================
    #     VAR_UNITS_READ={}
    #     VAR_UNITS_READ['concso2'] = 'ug m-3'
    #     VAR_UNITS_READ['concso4'] = 'ug m-3'
    #     VAR_UNITS_READ['pr']       = 'mm'
    #     VAR_UNITS_READ['wetso4']   = 'kg m-2 s-1'
    #     VAR_UNITS_READ['concso4pr'] = 'g m-3' # Removed sulphur from VAR_UNITS_READ mgS/L
    # =============================================================================
    #: :obj: `list` of :obj: `str`
    #: List containing all the variables available in this data set.
    PROVIDES_VARIABLES = list(VARS_TO_FILES)

    #: int: Number of available variables in this data set.
    num_vars = len(PROVIDES_VARIABLES)

    @property
    def DEFAULT_VARS(self):
        """Default variables (wrapper for :attr:`PROVIDES_VARIABLES`)"""
        return self.PROVIDES_VARIABLES

    def _get_time_stamps(self, df):
        tconv = lambda yr, m: np.datetime64(f"{yr:04d}-{m:02d}-{1:02d}", "s")  # noqa: E731
        dates_alt = [tconv(yr, m) for yr, m in zip(df.year.values, df.month.values)]
        return np.asarray(dates_alt)

    def read_file(self, filename, vars_to_retrieve):  #  -> List[StationData]:
        """Read one GawTadSubsetAasEtAl file

        ToDo
        ----
        Could be more efficient...

        Note
        ----
        One file contains all stations for one variable. This is unctypical
        for ground based observations since the data files are typically by
        station.

        Parameters
        ----------
        filename : str
            absolute path to filename to read

        vars_to_retrieve : list or str, optional
            list containing variable IDs that are supposed to be read.

        Returns
        -------
        station_list : list
            list of `StationData` objects containing data
        """
        station_list = []
        df = pd.read_csv(filename, sep=",", low_memory=False)
        # Converting month and year.

        df["dtime"] = self._get_time_stamps(df)

        # array av numpy.datetime64
        df.rename(columns={"Sampler": "instrument_name"}, inplace=True)
        grouped = df.groupby(by="station_name")

        # Looping over every station:
        for name, station_group in grouped:
            station_group = station_group.drop_duplicates(
                subset="dtime", keep="first"
            )  # Drops duplicate rows

            tvals = station_group["dtime"]

            stat = StationData()
            # Meta data
            stat["station_name"] = name

            stat["filename"] = filename
            stat["data_id"] = self.data_id
            stat["ts_type"] = self.TS_TYPE

            var_names = self.COLNAMES_VARS
            # Looping over all keys in the grouped data frame.
            for key in station_group:
                # Enters if the the key is a variable
                if key in var_names:
                    _var = np.intersect1d(var_names[key], vars_to_retrieve)
                    if len(_var) == 0:
                        continue
                    elif len(_var) > 1:
                        raise OSError("Found multiple matches...")
                    var = _var[0]
                    if var in self.UNITCONVERSION:
                        # Convert units
                        from_unit, to_unit = self.UNITCONVERSION[var]
                        values = pd.to_numeric(station_group[key], errors="coerce").values
                        stat[var] = convert_unit(
                            values, from_unit=from_unit, to_unit=to_unit, var_name=var
                        )

                        if var == "wetso4":
                            # TODO: quite hard coded...
                            numsecs = get_tot_number_of_seconds(ts_type=self.TS_TYPE, dtime=tvals)
                            stat[var] = stat[var] / numsecs

                            to_unit = "kg m-2 s-1"
                    else:
                        to_unit = key.split("_")[-1]
                        vals = pd.to_numeric(station_group[key], errors="coerce").values
                        # This should only be true for
                        stat[var] = vals

                    stat["var_info"][var] = {"units": to_unit}
                else:
                    if key == "dtime":
                        stat[key] = station_group[key].values
                    else:
                        # Store the meta data.
                        stat[key] = station_group[key].values[0]

            # =============================================================================
            #             # Since no altitude is provided in the files. Geodesy is used to approximate
            #             # altitude based on latitude and longitude.
            #             try:
            #                 s["altitude"] = geodesy.get_topo_altitude(lat=s.latitude,
            #                                                           lon=s.longitude)
            #             except ValueError as e:
            #                 s['altitude'] = np.nan
            #                 from pyaerocom import const
            #                 logger.warning(f'Failed to access altitude for {name}')
            # =============================================================================
            # Added the created station to the station list.
            station_list.append(stat)
        return station_list

    def read(self, vars_to_retrieve=None):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or `str`:, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded

        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.

        Returns
        -------
        UngriddedData : :class:`UngriddedData`
            data object

        """

        files = self.get_file_list()
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        data_obj = UngriddedData()

        meta_key = 0.0
        idx = 0
        varindex = -1

        # assign metadata object
        metadata = data_obj.metadata  # dict
        meta_idx = data_obj.meta_idx  # dict

        for file in files:
            filename = os.path.basename(file)
            if filename not in self.FILES_CONTAIN:
                raise OSError(f"Invalid file name {filename}, this should not happen.")
            var_matches = [var for var in vars_to_retrieve if var in self.FILES_CONTAIN[filename]]
            if len(var_matches) == 0:
                continue
            stat_list = self.read_file(file, vars_to_retrieve=var_matches)
            for stat in stat_list:
                # self.counter += 1
                metadata[meta_key] = {}
                metadata[meta_key].update(stat.get_meta())
                metadata[meta_key].update(stat.get_station_coords())
                metadata[meta_key]["data_id"] = self.data_id
                metadata[meta_key]["ts_type"] = self.TS_TYPE
                # metadata[meta_key]['variables'] = stat["variables"]
                # Is instrumentname
                if "instrument_name" in stat and stat["instrument_name"] is not None:
                    instr = stat["instrument_name"]
                else:
                    instr = self.INSTRUMENT_NAME

                metadata[meta_key]["instrument_name"] = instr
                metadata[meta_key]["data_revision"] = self.data_revision

                # this is a list with indices of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                meta_idx[meta_key] = {}

                num_times = len(stat["dtime"])
                num_vars = len(stat["var_info"])
                temp_vars = list(stat["var_info"])
                tconv = stat["dtime"].astype("datetime64[s]")
                times = np.float64(tconv)
                totnum = num_times * num_vars

                if (idx + totnum) >= data_obj._ROWNO:
                    # This results in a error because it doesn't want to multiply empty with nan
                    data_obj.add_chunk(totnum)

                metadata[meta_key]["var_info"] = {}
                for var_count, var in enumerate(temp_vars):
                    values = stat[var]
                    start = idx + var_count * num_times
                    stop = start + num_times

                    if var not in data_obj.var_idx:
                        varindex += 1
                        data_obj.var_idx[var] = varindex
                        var_idx = varindex
                    else:
                        var_idx = data_obj.var_idx[var]

                    metadata[meta_key]["var_info"][var] = stat["var_info"][var]

                    data_obj._data[start:stop, data_obj._LATINDEX] = stat["latitude"]
                    data_obj._data[start:stop, data_obj._LONINDEX] = stat["longitude"]
                    data_obj._data[start:stop, data_obj._ALTITUDEINDEX] = stat["altitude"]
                    data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key

                    # write data to data object
                    data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                    data_obj._data[start:stop, data_obj._DATAINDEX] = values
                    data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                    meta_idx[meta_key][var] = np.arange(start, stop)

                meta_key += 1
                idx += totnum

        data_obj._data = data_obj._data[:idx]
        # sanity check
        data_obj._check_index()
        return data_obj


def _check_line_endings(filename):
    """File that checks all line endings in an ascii file (not in use)"""
    ll = None
    wrong_endings = {}
    with open(filename) as f:
        prev = None
        for i, line in enumerate(f.readlines()):
            spl = line.split(",")
            if not spl[-1] == "\n":
                wrong_endings[i + 1] = line
            if ll is None:
                ll = len(spl)
            elif not len(spl) == ll:
                print(i)
                print(prev)
                print(spl)
                raise Exception
            prev = spl
    return wrong_endings


class ReadSulphurAasEtAl(ReadAasEtal):
    """Old name of :class:`ReadAasEtal`."""

    def __init__(self, *args, **kwargs):
        super(ReadAasEtal, self).__init__(*args, **kwargs)
        warnings.warn(
            "You are using an old name for class ReadAasEtal", DeprecationWarning, stacklevel=2
        )
