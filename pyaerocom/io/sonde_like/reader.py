import logging
import os
import sys
from pathlib import Path

import numpy as np
import xarray

from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.variable import Variable
from pyaerocom.vertical_profile import VerticalProfile
from .jdcal import MJD_JD2000, MJD_0, jd2gcal
from collections.abc import Iterable

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)


class ReadSondeLikeData(ReadUngriddedBase):
    """Interface for reading of EVDC ozone sonde data data"""

    # in the HDF files time is store as modified julian day starting the 1. January 2000
    # from https://pypi.org/project/jdcal/
    # MJD_JD2000 = 51544.5
    # MJD_0 = 2400000.5
    MJD_BASE = MJD_JD2000 + MJD_0 - 0.5

    #: Mask for identifying datafiles
    _FILEMASK = "evdc-sonde_*.nc"
    _FILEMASK_HARP = "evdc-sonde_*.nc"
    _SUFFIX_HARP = Path(_FILEMASK_HARP).suffix
    _FILEMASK_HDF = "balloon_sonde.*.h5"
    _SUFFIX_HDF = Path(_FILEMASK_HDF).suffix

    #: version log of this class (for caching)
    __version__ = "0.02_" + ReadUngriddedBase.__baseversion__

    #: default variables for read method
    DEFAULT_VARS = ["conco33d", "vmro33d", "pro33d", "rh3d", "ps3d", "ts3d"]

    #: variable name of altitude in files
    ALTITUDE_ID_HARP = "geopotential_height"
    ALTITUDE_ID_HDF = "ALTITUDE.GPH"

    # names for output data (and input data for HARP files)
    LONGITUDE_NAME = "longitude"
    LATITUDE_NAME = "latitude"
    ALTITUDE_NAME = "altitude"

    # HDF names
    LONGITUDE_NAME_HDF = "LONGITUDE"
    LATITUDE_NAME_HDF = "LATITUDE"
    ALTITUDE_NAME_HDF = "ALTITUDE.GPH"
    TIME_NAME_HDF = "DATETIME"

    #: temporal resolution
    # Note: This is an approximation based on the fact that the sondes are flown more than once a day
    # as time the middle of the start and stop time rounded to the closed hour is used
    TS_TYPE = "3hourly"

    LOCATION_VAR_NAME_HARP = "site_name"
    START_TIME_VAR_NAME_HARP = "datetime_start"
    STOP_TIME_VAR_NAME_HARP = "datetime_stop"
    UNIT_NAME_HARP = "units"

    # for HDF these are in the global attributes
    LOCATION_VAR_NAME_HDF = "DATA_LOCATION"
    START_TIME_VAR_NAME_HDF = "DATA_START_DATE"
    STOP_TIME_VAR_NAME_HDF = "DATA_STOP_DATE"
    # the hdf files also provide e.g. info about the PI which could be added here

    # HDF reading needs some more constants
    # These are attribute names
    HDF_UNIT_ATTR_NAME = "VAR_UNITS"
    HDF_VALID_MIN_ATTR_NAME = "VAR_VALID_MIN"
    HDF_VALID_MAX_ATTR_NAME = "VAR_VALID_MAX"
    HDF_FILL_VALUE_ATTR_NAME = "VAR_FILL_VALUE"

    # Not needed for now
    KEEP_ADD_META = []

    #: If true, the uncertainties are also read
    READ_UNCERTAINTIES = False

    # will be filled by the reading classes
    VAR_NAMES_FILE_HDF = {}
    VAR_NAMES_FILE_HARP = {}

    def __init__(self, data_id=None, data_dir: str | Path | None = None, format: str = "HARP"):
        # initiate base class
        if isinstance(data_id, Path):
            _data_dir = str(data_dir)
        else:
            _data_dir = data_dir
        super().__init__(data_id=data_id, data_dir=_data_dir)
        #: private dictionary containing loaded Variable instances,
        self._var_info = {}

        #: files that are supposed to be excluded from reading
        self.exclude_files = []

        #: files that were actually excluded from reading
        self.excluded_files = []

        self.is_vertical_profile = True
        self.format = format
        if format == "HARP":
            self.FILEMASK = self._FILEMASK_HARP
        elif format == "HDF":
            self.FILEMASK = self._FILEMASK_HDF
        elif format == "IAGOS_HARP":
            self.FILEMASK = self._FILEMASK_HARP
        else:
            raise NotImplementedError

    @override
    def read_file(
        self,
        filename,
        vars_to_retrieve=None,
        read_uncertainties=READ_UNCERTAINTIES,
        remove_outliers=True,
    ):
        """

        :param filename:
        :param vars_to_retrieve:
        :param read_uncertainties:
        :param remove_outliers:
        :return:
        list of files
        """
        _file = Path(filename)
        if _file.suffix == self._SUFFIX_HARP:
            return self.read_file_harp(
                filename,
                vars_to_retrieve=vars_to_retrieve,
                read_uncertainties=read_uncertainties,
                remove_outliers=remove_outliers,
            )
        elif _file.suffix == self._SUFFIX_HDF:
            return self.read_file_hdf(
                filename,
                vars_to_retrieve=vars_to_retrieve,
                read_uncertainties=read_uncertainties,
                remove_outliers=remove_outliers,
            )
        else:
            raise NotImplementedError

    def read_file_harp(
        self,
        filename,
        vars_to_retrieve=None,
        read_uncertainties=False,
        remove_outliers=True,
    ):
        """Read HARP file and return it as instance of :class:`StationData`

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        read_uncertainties : bool
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
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        _vars = []
        if vars_to_retrieve is None:
            vars_to_read = self.PROVIDES_VARIABLES
        else:
            vars_to_read = vars_to_retrieve

        # create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        logger.debug(f"Reading file {filename}")
        with xarray.open_dataset(filename, engine="netcdf4", decode_timedelta=True) as data_in:
            if "site_name" in data_in:
                # data_in["site_name"].values.tostring().decode("utf-8")
                data_out["station_id"] = data_out["station_name"] = str(
                    data_in["site_name"].values.astype(str)
                )
            elif "location_name" in data_in:
                data_out["station_id"] = data_out["station_name"] = (
                    # data_in["location_name"].values.tostring().decode("utf-8")
                    str(data_in["location_name"].values.astype(str))
                )
            else:
                # the IAGOS files don't contain a field for the station name
                # try the filename instead
                try:
                    # FRA is the station name
                    # iagos-o3_asc-L1-2025091309331502-FRA-20250913T093331-20250913T111111-0100-20250920T010046.nc
                    data_out["station_id"] = os.path.basename(filename).split("-")[4]
                except Exception:
                    logger.error(f"file {filename} does not contain a site name. Skipping...")
                    return None
            data_out["data_id"] = self.data_id
            data_out["ts_type"] = self.TS_TYPE
            data_out["station_name"] = data_out["station_id"]

            # create empty arrays for all variables that are supposed to be read
            # from file
            for var in vars_to_read:
                if var not in self._var_info:
                    self._var_info[var] = Variable(var)

            # Put also just in the attributes.
            # set station coords to the first location
            data_out["station_coords"][self.LONGITUDE_NAME] = np.float64(
                data_in[self.LONGITUDE_NAME].values[0]
            )
            data_out["station_coords"][self.LATITUDE_NAME] = np.float64(
                data_in[self.LATITUDE_NAME].values[0]
            )
            # Obs: geopotential height
            # min due to IAGOS descends data that have a decending altitude coordinate
            data_out["station_coords"][self.ALTITUDE_NAME] = np.float64(
                np.nanmin(data_in[self.ALTITUDE_ID_HARP].values)
            )
            # these are the profile coordinates
            data_out[self.LONGITUDE_NAME] = np.float64(data_in[self.LONGITUDE_NAME].values)
            data_out[self.LATITUDE_NAME] = np.float64(data_in[self.LATITUDE_NAME].values)
            data_out[self.ALTITUDE_NAME] = np.float64(data_in[self.ALTITUDE_ID_HARP].values)

            # dtime is needed later again
            dtime = data_in["datetime_start"].values.astype("datetime64[s]")
            data_out["dtime"] = data_in["datetime_start"].astype("datetime64[s]")
            data_out["stopdtime"] = data_in["datetime_stop"].astype("datetime64[s]")
            data_out["filename"] = filename

            for var in vars_to_read:
                data_out["var_info"][var] = {}
                err_read = False
                unit_ok = False
                outliers_removed = False
                has_altitude = False

                netcdf_var_name = self.VAR_NAMES_FILE_HARP[var]
                # check if the desired variable is in the file
                if netcdf_var_name not in data_in.variables:
                    logger.warning(f"Variable {var} not found in file {filename}")
                    continue

                # info = var_info[var]
                # xarray.DataArray
                arr = data_in.variables[netcdf_var_name]
                # the actual data as numpy array (or float if 0-D data, e.g. zdust)
                val = np.squeeze(np.float64(arr.values))  # squeeze to 1D array
                err = np.full_like(val, np.nan)
                if read_uncertainties:
                    try:
                        err = data_in.variables[f"{netcdf_var_name}_uncertainty"]
                        err_read = True
                    except KeyError:
                        pass

                # CONVERT UNIT
                unit = ""
                try:
                    unit = arr.attrs["units"]
                    unit_ok = True
                except KeyError:
                    pass

                # create instance of ProfileData
                profile = VerticalProfile(
                    data=val,
                    altitude=data_out[self.ALTITUDE_NAME],
                    dtime=dtime,
                    var_name=var,
                    data_err=err,
                    var_unit=unit,
                    altitude_unit=data_in[self.ALTITUDE_ID_HARP].attrs["units"],
                )

                # Write everything into profile
                data_out[var] = profile
                has_altitude = True

                data_out["var_info"][var].update(
                    unit_ok=unit_ok,
                    err_read=err_read,
                    outliers_removed=outliers_removed,
                    has_altitude=has_altitude,
                )
        return data_out

    def read_file_hdf(
        self,
        filename,
        vars_to_retrieve=None,
        read_uncertainties=False,
        remove_outliers=True,
    ):
        """Read EVDC hdf file and return it as instance of :class:`StationData`

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        read_uncertainties : bool
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
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        _vars = []
        if vars_to_retrieve is None:
            vars_to_read = self.PROVIDES_VARIABLES
        else:
            vars_to_read = vars_to_retrieve

        # create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        logger.debug(f"Reading file {filename}")

        # reading hdf5 file with the netcdf interface
        with xarray.open_dataset(filename) as data_in:
            # 1st, some checks that might prevent us from using the current data file:
            # - no station name provided
            # - the data file doesn't contain all variables we are after
            if self.LOCATION_VAR_NAME_HDF in data_in.attrs:
                data_out["station_id"] = data_out["station_name"] = data_in.attrs[
                    self.LOCATION_VAR_NAME_HDF
                ]
            else:
                logger.error(f"file {filename} does not contain a site name. Skipping")
                return None

            # check if all data variables are in the data file
            for var in vars_to_retrieve:
                netcdf_var_name = self.VAR_NAMES_FILE_HDF[var]
                # check if the desired variable is in the file
                if netcdf_var_name not in data_in.variables:
                    logger.info(f"Variable {var} not found in file {filename}. Skipping that file")
                    return None
            data_out["data_id"] = self.data_id
            data_out["ts_type"] = self.TS_TYPE

            # create empty arrays for all variables that are supposed to be read
            # from file
            for var in vars_to_read:
                if var not in self._var_info:
                    self._var_info[var] = Variable(var)

            # Put also just in the attributes.
            # set station coords to the first location
            data_out["station_coords"][self.LONGITUDE_NAME] = np.float64(
                data_in[self.LONGITUDE_NAME_HDF].values[0]
            )
            data_out["station_coords"][self.LATITUDE_NAME] = np.float64(
                data_in[self.LATITUDE_NAME_HDF].values[0]
            )
            # Obs: geopotential height
            data_out["station_coords"][self.ALTITUDE_NAME] = np.float64(
                data_in[self.ALTITUDE_ID_HDF].values[0]
            )
            # these are the profile coordinates
            data_out[self.LONGITUDE_NAME] = np.float64(data_in[self.LONGITUDE_NAME_HDF].values[0])
            data_out[self.LATITUDE_NAME] = np.float64(data_in[self.LATITUDE_NAME_HDF].values[0])
            data_out[self.ALTITUDE_NAME] = np.float64(data_in[self.ALTITUDE_ID_HDF].values)

            # dtime is needed later again
            dtime = self.get_seconds_since_epoch_from_hdf_time(data_in["DATETIME"].values)

            data_out["dtime"] = dtime[0].astype("datetime64[s]")
            data_out["stopdtime"] = dtime[-1].astype("datetime64[s]")
            data_out["filename"] = filename

            for var in vars_to_read:
                data_out["var_info"][var] = {}
                err_read = False
                unit_ok = False
                outliers_removed = False
                has_altitude = False

                netcdf_var_name = self.VAR_NAMES_FILE_HDF[var]
                arr = data_in.variables[netcdf_var_name]
                # the actual data as numpy array (or float if 0-D data, e.g. zdust)
                val = np.squeeze(np.float64(arr.values))  # squeeze to 1D array
                # replace fill value with np.nan
                val[
                    val
                    == np.float64(
                        data_in.variables[netcdf_var_name].attrs[self.HDF_FILL_VALUE_ATTR_NAME]
                    )
                ] = np.nan
                err = np.full_like(val, np.nan)
                if read_uncertainties:
                    try:
                        err = data_in.variables[f"{netcdf_var_name}_UNCERTAINTY.COMBINED.STANDARD"]
                        err_read = True
                    except KeyError:
                        pass

                # CONVERT UNIT
                unit = ""
                try:
                    unit = arr.attrs[self.HDF_UNIT_ATTR_NAME]
                    unit_ok = True
                except KeyError:
                    pass

                # we might need to adjust the units here later on

                # create instance of VerticalProfile
                profile = VerticalProfile(
                    data=val,
                    altitude=data_out[self.ALTITUDE_NAME],
                    dtime=dtime,
                    var_name=var,
                    data_err=err,
                    var_unit=unit,
                    altitude_unit=data_in[self.ALTITUDE_ID_HDF].attrs[self.HDF_UNIT_ATTR_NAME],
                )

                # Write everything into profile
                data_out[var] = profile
                has_altitude = True

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
        vars_to_retrieve: str | None = None,
        files: Iterable[str | Path] | None = None,
        first_file: int | None = None,
        last_file: int | None = None,
        read_err=READ_UNCERTAINTIES,
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

        if files is None:
            files = self.get_file_list(pattern=self.FILEMASK)
        if len(files) == 0:
            files = self.get_file_list(pattern=self.FILEMASK)
        # files = self.files

        # turn files into a list because I suspect there may be a bug if you don't do this
        if isinstance(files, str):
            files = [files]

        if files is not None and last_file is not None and first_file is not None:
            files = files[
                first_file : last_file + 1
            ]  # think need to +1 here in order to actually get desired subset
        elif files is not None and first_file is not None:
            files = files[first_file:]
        elif files is not None and last_file is not None:
            files = files[:last_file]

        self.files = files
        self.read_failed = []

        data_obj = UngriddedData()
        data_obj.is_vertical_profile = True
        col_idx = data_obj.index
        meta_key = -1.0
        idx = 0

        # assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        VAR_IDX = -1
        self.files_found = len(files)
        self.files_not_read = 0

        for i, _file in enumerate(files):
            logger.info(f"Reading file {_file}")
            try:
                stat = self.read_file(
                    _file,
                    vars_to_retrieve=vars_to_retrieve,
                    read_uncertainties=read_err,
                    remove_outliers=remove_outliers,
                )
                if stat is None:
                    self.files_not_read += 1
                    logger.info(f"File {_file} has no useful data. Skipping...")
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
                time = stat.dtime
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
                        metadata[meta_key]["var_info"][self.ALTITUDE_NAME] = via = {}

                        vi.update(val.var_info[var])
                        via.update(val.var_info[self.ALTITUDE_NAME])
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
                    data_obj._data[idx:stop, col_idx[self.LATITUDE_NAME]] = stat["station_coords"][
                        self.LATITUDE_NAME
                    ]
                    data_obj._data[idx:stop, col_idx[self.LONGITUDE_NAME]] = stat[
                        "station_coords"
                    ][self.LONGITUDE_NAME]
                    data_obj._data[idx:stop, col_idx[self.ALTITUDE_NAME]] = stat["station_coords"][
                        self.ALTITUDE_NAME
                    ]
                    data_obj._data[idx:stop, col_idx["meta"]] = meta_key

                    # write data to data object
                    data_obj._data[idx:stop, col_idx["time"]] = time
                    data_obj._data[idx:stop, col_idx["stoptime"]] = stat["stopdtime"]
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
        logger.info(
            f"reading summary: found {self.files_found} files, {self.files_not_read} didn't provide usable data."
        )

        return data_obj

    def get_file_list(self, pattern=None):
        """Perform recursive file search for all input variables

        Parameters
        ----------
        pattern : str, optional
            file name pattern applied to search

        Returns
        -------
        list
            list containing file paths
        """

        logger.info("Fetching sonde like data files. This might take a while...")
        searchpath = Path(self.data_dir)
        files = []
        for _file in searchpath.rglob(self.FILEMASK):
            if _file.is_file():
                files.append(str(_file))
        logger.info(f"Found {len(files)} sonde like data files in directory {self.data_dir}.")
        return files

    def get_seconds_since_epoch_from_hdf_time(self, indata: np.ndarray) -> np.ndarray:
        """
        small helper method to calculate seconds after epoch from the year 2000 based
        HDF time (stored is the Julian day number after 01-01-2000T00:00:00)

        This is not the most efficient way to do this!

        :param indata:
        :return:
        """
        from datetime import datetime

        outdata = None
        _inval = None
        if isinstance(indata, np.ndarray):
            outdata = np.zeros_like(indata, dtype="datetime64[us]")
            for i, _inval in enumerate(indata):
                temp_time_arr = jd2gcal(self.MJD_BASE, _inval)
                flt_hours = temp_time_arr[-1] * 24.0
                hours = int(flt_hours)
                flt_minutes = (flt_hours - hours) * 60
                minutes = int(flt_minutes)
                flt_seconds = (flt_minutes - minutes) * 60
                seconds = int(flt_seconds)
                microseconds = int((flt_seconds - seconds) * 1e6)
                bla = np.datetime64(
                    datetime(
                        temp_time_arr[0],
                        temp_time_arr[1],
                        temp_time_arr[2],
                        hours,
                        minutes,
                        seconds,
                        microseconds,
                    ),
                    "us",
                )
                outdata[i] = bla
        else:
            raise NotImplementedError

        return outdata


class ReadEvdcOzoneSondeDataHarp(ReadSondeLikeData):
    """
    Interface for reading of EVDC ozone sonde data in HARP format as provides by the CAMS2-82 project via
    the CAMS validation server
    """

    #: Name of dataset (OBS_ID)
    DATA_ID = const.EVDC_OZONE_SONDES_NAME_HARP

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EVDC_OZONE_SONDES_NAME_HARP]

    VAR_NAMES_FILE_HARP = {
        "conco33d": "O3_volume_mixing_ratio",
        # "vmro33d": "O3_number_density",
        "vmro33d": "O3_volume_mixing_ratio",
        "pro33d": "O3_partial_pressure",
        "rh3d": "relative_humidity",
        "ps3d": "pressure",
        "ts3d": "temperature",
    }


class ReadIagosDataHarp(ReadSondeLikeData):
    """
    Interface for reading of IAGOS data in HARP format as provides by the CAMS2-82 project via
    the CAMS validation server
    """

    #: Name of dataset (OBS_ID)
    DATA_ID = const.IAGOS_NAME_HARP

    # IAGOS data has only one variable per file and the variable name encoded in the file name
    # add that to the filemask at the init method

    _VAR_FILE_SUFFIX = {}
    _VAR_FILE_SUFFIX["vmro33d"] = "o3"
    _VAR_FILE_SUFFIX["vmrco3d"] = "co"

    ALTITUDE_ID_HARP = "altitude"

    _FILEMASK = "iagos-*.nc"
    _FILEMASK_HARP = "iagos-*.nc"
    _FILEMASK_O3 = "iagos-o3*.nc"
    _FILEMASK_CO = "iagos-co*.nc"
    _SUFFIX_HARP = Path(_FILEMASK_HARP).suffix

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    VAR_NAMES_FILE_HARP = {
        "vmro33d": "O3_volume_mixing_ratio",
        "vmrco3d": "CO_volume_mixing_ratio",
        "ps3d": "pressure",
        "ts3d": "temperature",
    }

    PROVIDES_VARIABLES = list(VAR_NAMES_FILE_HARP)
    READ_UNCERTAINTIES = False

    def __init__(self, data_id=None, data_dir: str | Path | None = None):
        # initiate base class
        if isinstance(data_id, Path):
            _data_dir = str(data_dir)
        else:
            _data_dir = data_dir
        super().__init__(data_id=data_id, data_dir=_data_dir, format="IAGOS_HARP")

    def read(
        self,
        vars_to_retrieve: str | None = None,
        files: Iterable[str | Path] | None = None,
        first_file: int | None = None,
        last_file: int | None = None,
        read_err=READ_UNCERTAINTIES,
        remove_outliers=True,
        pattern=None,
    ):
        # for the IAGOS data each file contains either Ozone or CO data
        # adjust the file mask accordingly

        if "vmro33d" in vars_to_retrieve:
            self.FILEMASK = self._FILEMASK_O3
        elif "vmrco3d" in vars_to_retrieve:
            self.FILEMASK = self._FILEMASK_CO
        else:
            # pass for now
            pass

        return super().read(
            vars_to_retrieve, files, first_file, last_file, read_err, remove_outliers, pattern
        )


class ReadEvdcOzoneSondeDataHdf(ReadSondeLikeData):
    """
    Interface for reading of EVDC ozone sonde data in HDF5 format

    IMPORTANT NOTE:
    The EVDC data is a mixture of files in HDF4 and HDF5 format. Because we don't want to add pyhdf as a dependency,
    the design decision has been made that only HDF5 files will be read by this reader (Because xarray can read those
    via the standard netcdf4 reader.

    Existing HDF4 file can be easily converted to HDF5 / netcdf4 with the command
    ncks -4 <hdf4 file> <hdf5 file>

    This reader needs the file extension to be ".h5"

    The outcome of the command above is a hdf5 file that is not entirely of the same format as the EVDC HDF5 files,
    but similar enough so that the code in this package can read it.
    The dimensions are different, but the variable names are the same.
    """

    #: Name of dataset (OBS_ID)
    DATA_ID = const.EVDC_OZONE_SONDES_NAME_HDF

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EVDC_OZONE_SONDES_NAME_HDF]

    VAR_NAMES_FILE_HDF = {
        "conco33d": "O3.MIXING.RATIO.VOLUME_INSITU",
        "vmro33d": "O3.NUMBER.DENSITY_INSITU",
        "pro33d": "O3.PARTIAL.PRESSURE_INSITU",
        "rh3d": "HUMIDITY.RELATIVE_INSITU",
        "ps3d": "PRESSURE_INSITU",
        "ts3d": "TEMPERATURE_INSITU",
    }

    PROVIDES_VARIABLES = list(VAR_NAMES_FILE_HDF)

    def __init__(self, data_id=None, data_dir: str | Path | None = None):
        # initiate base class
        if isinstance(data_id, Path):
            _data_dir = str(data_dir)
        else:
            _data_dir = data_dir
        super().__init__(data_id=data_id, data_dir=_data_dir, format="HDF")
