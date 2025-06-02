import logging
import os
import sys

import numpy as np
import pandas as pd
import xarray

from pyaerocom import const
from pyaerocom.exceptions import (
    DataDimensionError,
    DataUnitError,
    EarlinetFileError,
    VarNotAvailableError,
)
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.units.units_helpers import get_unit_conversion_fac
from pyaerocom.variable import Variable
from pyaerocom.vertical_profile import VerticalProfile

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)


class ReadEarlinet(ReadUngriddedBase):
    """Interface for reading of EARLINET data"""

    #: Mask for identifying datafiles
    _FILEMASK = "*.*"

    #: version log of this class (for caching)
    __version__ = "0.18_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.EARLINET_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EARLINET_NAME]

    #: default variables for read method
    DEFAULT_VARS = ["bsc532aer", "ec532aer"]

    # These are applied to all files. If new cloud filter names are discovered they should be added here.
    # As of 20.08.24, however, there are still files with less reliable data which get through the filters.
    # https://github.com/metno/pyaerocom/issues/1310
    CLOUD_FILTERS = {
        "cloud_mask_type": 0,  # "no_cloudmask_available manual_cloudmask automatic_cloudmask"
        "cirrus_contamination": 2,  # "not_available no_cirrus cirrus_detected"
    }

    #: all data values that exceed this number will be set to NaN on read. This
    #: is because iris, xarray, etc. assign a FILL VALUE of the order of e36
    #: to missing data in the netcdf files
    _MAX_VAL_NAN = 1e6

    #: variable name of altitude in files
    ALTITUDE_ID = "altitude"

    #: temporal resolution
    # Note: This is an approximation based on the fact that MOST of the data appears to be collected
    # at an hourly reoslution. Some files are a little less, but typically this is the case
    TS_TYPE = "hourly"

    VAR_PATTERNS_FILE = {
        "ec532aer": "_e0532",
        "ec355aer": "_e0355",
        "bsc532aer": "_b0532",
        "bsc355aer": "_b0355",
        "bsc1064aer": "_b1064",
        # "zdust": "*.e*", # not sure if EARLINET has this anymore
    }

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {
        "ec532aer": "extinction",
        "ec355aer": "extinction",
        "ec1064aer": "extinction",
        "bsc532aer": "backscatter",
        "bsc355aer": "backscatter",
        "bsc1064aer": "backscatter",
        "zdust": "DustLayerHeight",  # not sure if EARLINET has this anymore
    }

    META_NAMES_FILE = dict(
        location="location",
        start_utc="measurement_start_datetime",
        stop_utc="measurement_stop_datetime",
        # wavelength_det="DetectionWavelength_nm",
        # res_raw_m="ResolutionRaw_meter",
        instrument_name="system",
        comment="comment",
        PI="PI",
        dataset_name="title",
        # station_name="station_ID",
        website="references",
        wavelength_emis="wavelength",
        # detection_mode="DetectionMode",
        # res_eval="ResolutionEvaluated",
        # input_params="InputParameters",
        altitude="altitude",
        # eval_method="backscatter_evaluation_method",
    )
    #: metadata keys that are needed for reading (must be values in
    #: :attr:`META_NAMES_FILE`)
    META_NEEDED = [
        "location",
        "measurement_start_datetime",
        "measurement_start_datetime",
    ]

    #: Metadata keys from :attr:`META_NAMES_FILE` that are additional to
    #: standard keys defined in :class:`StationMetaData` and that are supposed
    #: to be inserted into :class:`UngriddedData` object created in :func:`read`
    KEEP_ADD_META = [
        "location",
        "wavelength",
        "zenith_angle",
        "comment",
        "shots",
        "backscatter_evaluation_method",
    ]

    #: Attribute access names for unit reading of variable data
    VAR_UNIT_NAMES = dict(
        extinction=["units"],
        backscatter=["units"],
        dustlayerheight=["units"],
        altitude="units",
    )
    #: Variable names of uncertainty data
    ERR_VARNAMES = dict(
        ec532aer="error_extinction",
        ec355aer="error_extinction",
    )

    #: If true, the uncertainties are also read (where available, cf. ERR_VARNAMES)
    READ_ERR = True

    PROVIDES_VARIABLES = list(VAR_PATTERNS_FILE)

    EXCLUDE_CASES = ["cirrus.txt"]

    def __init__(self, data_id=None, data_dir=None):
        # initiate base class
        super().__init__(data_id=data_id, data_dir=data_dir)
        # make sure everything is properly set up
        if not all(
            [x in self.VAR_PATTERNS_FILE for x in self.PROVIDES_VARIABLES]
        ):  # pragma: no cover
            raise AttributeError(
                "Please specify file search masks in "
                "header dict VAR_PATTERNS_FILE for each "
                "variable defined in PROVIDES_VARIABLES"
            )
        elif not all(
            [x in self.VAR_NAMES_FILE for x in self.PROVIDES_VARIABLES]
        ):  # pragma: no cover
            raise AttributeError(
                "Please specify file search masks in "
                "header dict VAR_NAMES_FILE for each "
                "variable defined in PROVIDES_VARIABLES"
            )
        #: private dictionary containing loaded Variable instances,
        self._var_info = {}

        #: files that are supposed to be excluded from reading
        self.exclude_files = []

        #: files that were actually excluded from reading
        self.excluded_files = []

        self.is_vertical_profile = True

    @override
    def read_file(self, filename, vars_to_retrieve=None, read_err=None, remove_outliers=True):
        """Read EARLINET file and return it as instance of :class:`StationData`

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        read_err : bool
            if True, uncertainty data is also read (where available).
        remove_outliers : bool
            if True, outliers are removed for each variable using the
            `minimum` and `maximum` attributes for that variable (accessed
            via pyaerocom.const.VARS[var_name]).

        Returns
        -------
        StationData
            dict-like object containing results
        """
        if read_err is None:  # use default setting
            read_err = self.READ_ERR
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        _vars = []
        for var in vars_to_retrieve:
            if (
                var in self.VAR_PATTERNS_FILE
            ):  # make sure to only read what is supported by this file
                if self.VAR_PATTERNS_FILE[var] in filename:
                    _vars.append(var)
            elif var in self.AUX_REQUIRES:
                _vars.append(var)
            else:
                raise VarNotAvailableError(f"{var} is not supported")

        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(_vars)

        # create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out["station_id"] = filename.split("/")[-1].split("_")[
            2
        ]  # loss of generality but should work. can also get from reading file if needed: data_in.station_ID
        data_out["data_id"] = self.data_id
        data_out["ts_type"] = self.TS_TYPE

        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            if var not in self._var_info:
                self._var_info[var] = Variable(var)
        var_info = self._var_info

        # Iterate over the lines of the file
        logger.debug(f"Reading file {filename}")

        with xarray.open_dataset(filename, engine="netcdf4", decode_timedelta=True) as data_in:
            for filter in self.CLOUD_FILTERS:
                if filter in data_in.variables:
                    if data_in.variables[filter].item() == self.CLOUD_FILTERS[filter]:
                        logger.debug(f"Skipping {filename} due to cloud filtering")
                        continue

            # getting the coords since no longer in metadata
            # Put also just in the attributes. not sure why appears twice
            data_out["station_coords"]["longitude"] = data_out["longitude"] = np.float64(
                data_in["longitude"].values
            )
            data_out["station_coords"]["latitude"] = data_out["latitude"] = np.float64(
                data_in["latitude"].values
            )
            data_out["altitude"] = np.float64(
                data_in[
                    "altitude"
                ].values  # altitude is defined in EARLINET in terms of altitude above sea level
            )  # Note altitude is an array for the data, station altitude is different

            data_out["station_coords"]["altitude"] = data_in.station_altitude.item()
            data_out["altitude_attrs"] = data_in[
                "altitude"
            ].attrs  # get attrs for altitude units + extra

            # get intersection of metadaa in ddataa_out and data_in
            for k, v in self.META_NAMES_FILE.items():
                if v in self.META_NEEDED:
                    _meta = data_in.attrs[v]
                else:
                    try:
                        _meta = data_in.attrs[v]
                    except Exception:  # pragma: no cover
                        _meta = None
                data_out[k] = _meta

            # get metadata expected in StationData but not in data_in's metadata
            data_out["wavelength_emis"] = data_in["wavelength"]
            data_out["shots"] = data_in["shots"].item()
            data_out["zenith_angle"] = np.float64(data_in["zenith_angle"])
            data_out["filename"] = filename
            if "Lev02" in filename:
                data_out["data_level"] = 2
            loc_split = data_in.attrs["location"].split(", ")
            data_out["station_name"] = loc_split[0]
            if len(loc_split) > 1:
                data_out["country"] = loc_split[1]

            dtime = (
                pd.Timestamp(data_in.measurement_start_datetime).to_numpy().astype("datetime64[s]")
            )
            stop = (
                pd.Timestamp(data_in.measurement_stop_datetime).to_numpy().astype("datetime64[s]")
            )

            # in case measurement goes over midnight into a new day
            if stop < dtime:
                stop = stop + np.timedelta64(1, "[D]")

            data_out["dtime"] = [dtime]
            data_out["stopdtime"] = [stop]
            data_out["has_zdust"] = False

            for var in vars_to_read:
                data_out["var_info"][var] = {}
                err_read = False
                unit_ok = False
                outliers_removed = False
                has_altitude = False

                netcdf_var_name = self.VAR_NAMES_FILE[var]
                # check if the desired variable is in the file
                if netcdf_var_name not in data_in.variables:
                    logger.warning(f"Variable {var} not found in file {filename}")
                    continue

                info = var_info[var]
                # xarray.DataArray
                arr = data_in.variables[netcdf_var_name]
                # the actual data as numpy array (or float if 0-D data, e.g. zdust)
                val = np.squeeze(np.float64(arr))  # squeeze to 1D array

                # CONVERT UNIT
                unit = None

                unames = self.VAR_UNIT_NAMES[netcdf_var_name]
                for u in unames:
                    if u in arr.attrs:
                        unit = arr.attrs[u]
                if unit is None:
                    raise DataUnitError(f"Unit of {var} could not be accessed in file {filename}")
                unit_fac = None
                try:
                    to_unit = self._var_info[var].units
                    unit_fac = get_unit_conversion_fac(unit, to_unit)
                    val *= unit_fac
                    unit = to_unit
                    unit_ok = True
                except Exception as e:
                    logger.warning(
                        f"Failed to convert unit of {var} in file {filename} (Earlinet): "
                        f"Error: {repr(e)}"
                    )

                # import errors if applicable
                err = np.nan
                if read_err and var in self.ERR_VARNAMES:
                    err_name = self.ERR_VARNAMES[var]
                    if err_name in data_in.variables:
                        err = np.squeeze(np.float64(data_in.variables[err_name]))
                        if unit_ok:
                            err *= unit_fac
                        err_read = True

                # 1D variable
                if var == "zdust":
                    if not val.ndim == 0:
                        raise DataDimensionError(
                            "Fatal: dust layer height data must be single value"
                        )

                    if unit_ok and info.minimum < val < info.maximum:
                        logger.warning(f"zdust value {val} out of range, setting to NaN")
                        val = np.nan

                    if np.isnan(val):
                        logger.warning(
                            f"Invalid value of variable zdust in file {filename}. Skipping...!"
                        )
                        continue

                    data_out["has_zdust"] = True
                    data_out[var] = val

                else:
                    if not val.ndim == 1:
                        raise DataDimensionError("Extinction data must be one dimensional")
                    elif len(val) == 0:
                        continue  # no data
                    # Remove NaN equivalent values
                    val[val > self._MAX_VAL_NAN] = np.nan

                    wvlg = var_info[var].wavelength_nm
                    wvlg_str = self.META_NAMES_FILE["wavelength_emis"]

                    assert data_in[wvlg_str].shape == (1,)
                    if not wvlg == float(data_in[wvlg_str][0]):
                        logger.info("No wavelength match")
                        continue

                    alt_id = self.ALTITUDE_ID
                    alt_data = data_in.variables[alt_id]

                    alt_vals = np.float64(alt_data)
                    alt_unit = alt_data.attrs[self.VAR_UNIT_NAMES[alt_id]]
                    to_alt_unit = get_standard_unit("alt")
                    if not alt_unit == to_alt_unit:
                        try:
                            alt_unit_fac = get_unit_conversion_fac(alt_unit, to_alt_unit)
                            alt_vals *= alt_unit_fac
                            alt_unit = to_alt_unit
                        except Exception as e:
                            logger.warning(f"Failed to convert unit: {repr(e)}")
                    has_altitude = True

                    # remove outliers from data, if applicable
                    if remove_outliers and unit_ok:
                        # REMOVE OUTLIERS
                        outlier_mask = np.logical_or(val < info.minimum, val > info.maximum)
                        val[outlier_mask] = np.nan

                        if err_read:
                            err[outlier_mask] = np.nan
                        outliers_removed = True
                    # remove outliers from errors if applicable
                    if err_read:
                        err[err > self._MAX_VAL_NAN] = np.nan

                    # create instance of ProfileData
                    profile = VerticalProfile(
                        data=val,
                        altitude=alt_vals,
                        dtime=dtime,
                        var_name=var,
                        data_err=err,
                        var_unit=unit,
                        altitude_unit=alt_unit,
                    )

                    # Write everything into profile
                    data_out[var] = profile

                data_out["var_info"][var].update(
                    unit_ok=unit_ok,
                    err_read=err_read,
                    outliers_removed=outliers_removed,
                    has_altitude=has_altitude,
                )
        return data_out

    @override
    def read(
        self,
        vars_to_retrieve=None,
        files=None,
        first_file=None,
        last_file=None,
        read_err=None,
        remove_outliers=True,
        pattern=None,
    ):
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
        read_err : bool
            if True, uncertainty data is also read (where available). If
            unspecified (None), then the default is used (cf. :attr:`READ_ERR`)
         pattern : str, optional
            string pattern for file search (cf :func:`get_file_list`)

        Returns
        -------
        UngriddedData
            data object
        """

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        if read_err is None:
            read_err = self.READ_ERR

        if files is None:
            if len(self.files) == 0:
                self.get_file_list(vars_to_retrieve, pattern=pattern)
            files = self.files

        # turn files into a list because I suspect there may be a bug if you don't do this
        if isinstance(files, str):
            files = [files]

        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)

        files = files[
            first_file : last_file + 1
        ]  # think need to +1 here in order to actually get desired subset

        self.read_failed = []

        data_obj = UngriddedData()
        data_obj.is_vertical_profile = True
        col_idx = data_obj.index
        meta_key = -1.0
        idx = 0

        # assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        # last_station_id = ''
        num_files = len(files)

        disp_each = int(num_files * 0.1)
        if disp_each < 1:
            disp_each = 1

        VAR_IDX = -1
        for i, _file in enumerate(files):
            if i % disp_each == 0:
                logger.info(f"Reading file {i + 1} of {num_files} ({type(self).__name__})")
            try:
                stat = self.read_file(
                    _file,
                    vars_to_retrieve=vars_to_retrieve,
                    read_err=read_err,
                    remove_outliers=remove_outliers,
                )
                if not any([var in stat.vars_available for var in vars_to_retrieve]):
                    logger.info(
                        f"Station {stat.station_name} contains none of the desired variables. Skipping station..."
                    )
                    continue
                # if last_station_id != station_id:
                meta_key += 1
                # Fill the metadata dict
                # the location in the data set is time step dependant!
                # use the lat location here since we have to choose one location
                # in the time series plot
                metadata[meta_key] = {}
                metadata[meta_key].update(stat.get_meta())
                for add_meta in self.KEEP_ADD_META:
                    if add_meta in stat:
                        metadata[meta_key][add_meta] = stat[add_meta]
                # metadata[meta_key]['station_id'] = station_id

                metadata[meta_key]["data_revision"] = self.data_revision
                metadata[meta_key]["variables"] = []
                metadata[meta_key]["var_info"] = {}
                # this is a list with indices of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                meta_idx[meta_key] = {}
                # last_station_id = station_id

                # Is floating point single value
                time = stat.dtime[0]
                for var in stat.vars_available:
                    if var not in data_obj.var_idx:
                        VAR_IDX += 1
                        data_obj.var_idx[var] = VAR_IDX

                    var_idx = data_obj.var_idx[var]

                    val = stat[var]
                    metadata[meta_key]["var_info"][var] = vi = {}
                    if isinstance(val, VerticalProfile):
                        altitude = val.altitude
                        data = val.data
                        add = len(data)
                        err = val.data_err
                        metadata[meta_key]["var_info"]["altitude"] = via = {}

                        vi.update(val.var_info[var])
                        via.update(val.var_info["altitude"])
                    else:
                        add = 1
                        altitude = np.nan
                        data = val
                        if var in stat.data_err:
                            err = stat.err[var]
                        else:
                            err = np.nan
                    vi.update(stat.var_info[var])
                    stop = idx + add
                    # check if size of data object needs to be extended
                    if stop >= data_obj._ROWNO:
                        # if totnum < data_obj._CHUNKSIZE, then the latter is used
                        data_obj.add_chunk(add)

                    # write common meta info for this station
                    data_obj._data[idx:stop, col_idx["latitude"]] = stat["station_coords"][
                        "latitude"
                    ]
                    data_obj._data[idx:stop, col_idx["longitude"]] = stat["station_coords"][
                        "longitude"
                    ]
                    data_obj._data[idx:stop, col_idx["altitude"]] = stat["station_coords"][
                        "altitude"
                    ]
                    data_obj._data[idx:stop, col_idx["meta"]] = meta_key

                    # write data to data object
                    data_obj._data[idx:stop, col_idx["time"]] = time
                    data_obj._data[idx:stop, col_idx["stoptime"]] = stat.stopdtime[0]
                    data_obj._data[idx:stop, col_idx["data"]] = data
                    data_obj._data[idx:stop, col_idx["dataaltitude"]] = altitude
                    data_obj._data[idx:stop, col_idx["varidx"]] = var_idx

                    if read_err:
                        data_obj._data[idx:stop, col_idx["dataerr"]] = err

                    if var not in meta_idx[meta_key]:
                        meta_idx[meta_key][var] = []
                    meta_idx[meta_key][var].extend(list(range(idx, stop)))

                    if var not in metadata[meta_key]["variables"]:
                        metadata[meta_key]["variables"].append(var)

                    idx += add

            except Exception as e:
                self.read_failed.append(_file)
                logger.exception(f"Failed to read file {os.path.basename(_file)} (ERR: {repr(e)})")

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]

        return data_obj

    def _get_exclude_filelist(self):  # pragma: no cover
        """Get list of filenames that are supposed to be ignored"""
        exclude = []
        import glob

        files = glob.glob(f"{self.data_dir}/EXCLUDE/*.txt")
        for i, file in enumerate(files):
            if os.path.basename(file) not in self.EXCLUDE_CASES:
                continue
            count = 0
            num = None
            indata = False
            with open(file) as f:
                for line in f:
                    if indata:
                        exclude.append(line.strip())
                        count += 1
                    elif "Number of" in line:
                        num = int(line.split(":")[1].strip())
                        indata = True

            if not count == num:
                raise EarlinetFileError(
                    "Number of excluded files does not match the number of files in the list"
                )
        self.exclude_files = list(dict.fromkeys(exclude))
        return self.exclude_files

    @override
    def get_file_list(self, vars_to_retrieve=None, pattern=None):
        """Perform recursive file search for all input variables

        Note
        ----
        Overloaded implementation of base class, since for Earlinet, the
        paths are variable dependent

        Parameters
        ----------
        vars_to_retrieve : list
            list of variables to retrieve
        pattern : str, optional
            file name pattern applied to search

        Returns
        -------
        list
            list containing file paths
        """

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        exclude = self._get_exclude_filelist()
        logger.info("Fetching EARLINET data files. This might take a while...")
        patterns = []
        for var in vars_to_retrieve:
            if var not in self.VAR_PATTERNS_FILE:
                raise VarNotAvailableError(f"Input variable {var} is not supported")

            _pattern = self.VAR_PATTERNS_FILE[var]
            if pattern is not None:
                if "." in pattern:
                    raise NotImplementedError("filetype delimiter . not supported")
                spl = _pattern.split(".")
                if "*" not in spl[0]:
                    raise AttributeError(f"Invalid file pattern: {_pattern}")
                spl[0] = spl[0].replace("*", pattern)
                _pattern = ".".join(spl)

            patterns.append(_pattern)

        matches = []
        for root, dirnames, files in os.walk(self.data_dir, topdown=True):
            paths = [os.path.join(root, f) for f in files]
            for _pattern in patterns:
                for path in paths:
                    file = os.path.basename(path)
                    if _pattern not in file:
                        continue
                    elif file in exclude:
                        self.excluded_files.append(path)
                    else:
                        matches.append(path)
        self.files = files = list(dict.fromkeys(matches))
        return files
