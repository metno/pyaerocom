import logging
import os
from pathlib import Path

import numpy as np
import xarray

from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.variable import Variable
from pyaerocom.vertical_profile import VerticalProfile

logger = logging.getLogger(__name__)


class ReadEvdcOzoneSondeData(ReadUngriddedBase):
    """Interface for reading of EVDC ozone sonde data data"""

    #: Mask for identifying datafiles
    _FILEMASK = "evdc-sonde_*.nc"
    _FILEMASK_HARP = "evdc-sonde_*.nc"
    _FILEMASK_EVDC = "evdc-sonde_*.nc"

    #: version log of this class (for caching)
    __version__ = "0.01_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.EVDC_OZONE_SONDES_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EVDC_OZONE_SONDES_NAME]

    #: default variables for read method
    DEFAULT_VARS = ["conco33D", "vmro33D", "pro33D", "rh3D", "ps3D", "ts3D"]
    # O3_volume_mixing_ratio, O3_number_density, O3_partial_pressure, relative_humidity, pressure, temperature, wind_speed, wind_direction

    # These are applied to all files. If new cloud filter names are discovered they should be added here.
    # As of 20.08.24, however, there are still files with less reliable data which get through the filters.
    # https://github.com/metno/pyaerocom/issues/1310
    # CLOUD_FILTERS = {
    #     "cloud_mask_type": 0,  # "no_cloudmask_available manual_cloudmask automatic_cloudmask"
    #     "cirrus_contamination": 2,  # "not_available no_cirrus cirrus_detected"
    # }

    #: all data values that exceed this number will be set to NaN on read. This
    #: is because iris, xarray, etc. assign a FILL VALUE of the order of e36
    #: to missing data in the netcdf files
    # _MAX_VAL_NAN = 1e6

    #: variable name of altitude in files
    ALTITUDE_ID = "geopotential_height"

    #
    LONGITUDE_NAME = "longitude"
    LATITUDE_NAME = "latitude"
    ALTITUDE_NAME = "altitude"

    #: temporal resolution
    # Note: This is an approximation based on the fact that the sondes are flown more than once a day
    # as time the middle of the start and stop time rounded to the closed hour is used
    TS_TYPE = "3hourly"

    # DEFAULT_VARS = ["conco33D", "vmro33D", "pro33D", "rh3D", "ps3D", "ts3D"]
    # O3_volume_mixing_ratio, O3_number_density, O3_partial_pressure, relative_humidity, pressure, temperature, wind_speed, wind_direction
    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {
        "conco33D": "O3_volume_mixing_ratio",
        "vmro33D": "O3_number_density",
        "pro33D": "O3_partial_pressure",
        "rh3D": "relative_humidity",
        "ps3D": "pressure",
        "ts3D": "temperature",
    }

    LOCATION_VAR_NAME_HARP = "site_name"
    START_TIME_VAR_NAME_HARP = "datetime_start"
    STOP_TIME_VAR_NAME_HARP = "datetime_stop"

    #
    KEEP_ADD_META = [
        # "location",
        # "wavelength",
        # "zenith_angle",
        # "comment",
        # "shots",
        # "backscatter_evaluation_method",
    ]

    #: If true, the uncertainties are also read
    READ_UNCERTAINTIES = False

    PROVIDES_VARIABLES = list(VAR_NAMES_FILE)

    # EXCLUDE_CASES = ["cirrus.txt"]

    def __init__(self, data_id=None, data_dir: str | Path | None = None, format="HARP"):
        # initiate base class
        super().__init__(data_id=data_id, data_dir=str(data_dir))
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
        else:
            self.FILEMASK = self._FILEMASK_EVDC

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
        :param format:
        :return:
        """
        if self.format == "HARP":
            return self.read_file_harp(
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
        """Read EARLINET file and return it as instance of :class:`StationData`

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
        format : str
            supported formats are "HARP" or "EVDC"

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
        self.logger.debug(f"Reading file {filename}")
        with xarray.open_dataset(filename, engine="netcdf4", decode_timedelta=True) as data_in:
            try:
                data_out["station_id"] = data_out["station_name"] = data_in["site_name"].values
            except KeyError:
                logger.error(f"file {filename} does not contain a site name. Skipping")
                return data_out
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
                data_in[self.LONGITUDE_NAME].values[0]
            )
            data_out["station_coords"][self.LATITUDE_NAME] = np.float64(
                data_in[self.LATITUDE_NAME].values[0]
            )
            # Obs: geopotential height
            data_out["station_coords"][self.ALTITUDE_NAME] = np.float64(
                data_in[self.ALTITUDE_ID].values[0]
            )
            # these are the profile coordinates
            data_out[self.LONGITUDE_NAME] = np.float64(data_in[self.LONGITUDE_NAME].values)
            data_out[self.LATITUDE_NAME] = np.float64(data_in[self.LATITUDE_NAME].values)
            data_out[self.ALTITUDE_NAME] = np.float64(data_in[self.ALTITUDE_ID].values)

            # dtime is needed later again
            dtime = data_in["datetime_start"].values.astype("datetime64[s]")
            data_out["dtime"] = data_in["datetime_start"].astype("datetime64[s]")
            data_out["stopdtime"] = data_in["datetime_stop"].astype("datetime64[s]")

            for var in vars_to_read:
                data_out["var_info"][var] = {}
                err_read = False
                unit_ok = False
                outliers_removed = False
                has_altitude = False

                netcdf_var_name = self.VAR_NAMES_FILE[var]
                # check if the desired variable is in the file
                if netcdf_var_name not in data_in.variables:
                    self.logger.warning(f"Variable {var} not found in file {filename}")
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

                # we might need to adjust the units here later on

                # we might need to fill the StationData object a bit more later on

                # unames = self.VAR_UNIT_NAMES[netcdf_var_name]
                # for u in unames:
                #     if u in arr.attrs:
                #         unit = arr.attrs[u]
                # if unit is None:
                #     raise DataUnitError(f"Unit of {var} could not be accessed in file {filename}")
                # unit_fac = None
                # try:
                #     to_unit = self._var_info[var].units
                #     unit_fac = get_unit_conversion_fac(unit, to_unit)
                #     val *= unit_fac
                #     unit = to_unit
                #     unit_ok = True
                # except Exception as e:
                #     logger.warning(
                #         f"Failed to convert unit of {var} in file {filename} (Earlinet): "
                #         f"Error: {repr(e)}"
                #     )

                # import errors if applicable
                # err = np.nan
                # if read_uncertainties and var in self.ERR_VARNAMES:
                #     err_name = self.ERR_VARNAMES[var]
                #     if err_name in data_in.variables:
                #         err = np.squeeze(np.float64(data_in.variables[err_name]))
                #         if unit_ok:
                #             err *= unit_fac
                #         err_read = True

                # create instance of ProfileData
                profile = VerticalProfile(
                    data=val,
                    altitude=data_out[self.ALTITUDE_NAME],
                    dtime=dtime,
                    var_name=var,
                    data_err=err,
                    var_unit=unit,
                    altitude_unit=data_in[self.ALTITUDE_ID].attrs["units"],
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

    def read(
        self,
        vars_to_retrieve=None,
        files=None,
        first_file=None,
        last_file=None,
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
            if len(self.files) == 0:
                self.files = self.get_file_list(pattern=self._FILEMASK)
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

        VAR_IDX = -1
        for i, _file in enumerate(files):
            logger.info(f"Reading file {_file}")
            try:
                stat = self.read_file(
                    _file,
                    vars_to_retrieve=vars_to_retrieve,
                    read_uncertainties=read_err,
                    remove_outliers=remove_outliers,
                )
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
                self.logger.exception(
                    f"Failed to read file {os.path.basename(_file)} (ERR: {repr(e)})"
                )

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]

        return data_obj

    def get_file_list(self, pattern=None):
        """Perform recursive file search for all input variables

        Note
        ----
        Overloaded implementation of base class, since for EVDC the
        paths are dependending on the format

        Parameters
        ----------
        pattern : str, optional
            file name pattern applied to search

        Returns
        -------
        list
            list containing file paths
        """

        logger.info("Fetching EVDC data files. This might take a while...")
        searchpath = Path(self.data_dir)
        files = []
        for _file in searchpath.rglob(self.FILEMASK):
            if _file.is_file():
                files.append(str(_file))
        logger.info(f"Found {len(files)} EVDC data files in directory {self.data_dir}.")
        return files
