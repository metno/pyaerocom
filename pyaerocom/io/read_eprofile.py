import logging
import os
import sys

import numpy as np
import xarray

from pyaerocom import const
from pyaerocom.units import convert_unit
from pyaerocom.exceptions import DataUnitError, DataDimensionError, EprofileFileError
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units.units_helpers import get_unit_conversion_fac
from pyaerocom.variable import Variable
from pyaerocom.vertical_profile import VerticalProfile
from pathlib import Path

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


logger = logging.getLogger(__name__)


class ReadEprofile(ReadUngriddedBase):
    """Interface for reading of EARLINET data"""

    #: Mask for identifying datafiles
    _FILEMASK = "*.nc*"

    #: version log of this class (for caching)
    __version__ = "0.01_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.EPROFILE_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EPROFILE_NAME]

    #: default variables for read method
    DEFAULT_VARS = ["ec1064aer", "bsc1064aer"]

    CLOUD_FILTERS = {}

    #: all data values that exceed this number will be set to NaN on read. This
    #: is because iris, xarray, etc. assign a FILL VALUE of the order of e36
    #: to missing data in the netcdf files
    _MAX_VAL_NAN = 1e6

    #: variable name of altitude in files
    ALTITUDE_ID = "altitude"

    #: temporal resolution
    # TODO: check this
    TS_TYPE = "hourly"

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    # TODO: add aod
    VAR_NAMES_FILE = {
        "ec1064aer": "extinction",
        "bsc1064aer": "attenuated_backscatter_0",
    }

    META_NAMES_FILE = dict(
        station_longitude="station_longitude",
        station_latitude="station_latitude",
        station_altitude="station_altitude",
        instrument_name="instrument_id",
        instrument_type="instrument_type",
        comment="comment",
        PI="principal_investigator",
        institution="institution",
        dataset_name="title",
        website="references",
        wavelength_emis="l0_wavelength",
        altitude="altitude",
        history="history",
        overlap_is_corrected="overlap_is_corrected",
    )
    #: metadata keys that are needed for reading (must be values in
    #: :attr:`META_NAMES_FILE`)
    META_NEEDED = [
        "station_longitude",
        "station_latitude",
        "station_altitude",
    ]

    #: Metadata keys from :attr:`META_NAMES_FILE` that are additional to
    #: standard keys defined in :class:`StationMetaData` and that are supposed
    #: to be inserted into :class:`UngriddedData` object created in :func:`read`
    KEEP_ADD_META = [
        "comment",
    ]

    #: Attribute access names for unit reading of variable data
    VAR_UNIT_NAMES = dict(
        extinction=["unit"],  # TODO: needs checking
        attenuated_backscatter_0=["units"],
        altitude=["units"],
    )
    #: Variable names of uncertainty data
    ERR_VARNAMES = dict()

    PROVIDES_VARIABLES = list(DEFAULT_VARS)

    EXCLUDE_CASES = []

    def __init__(self, data_id=None, data_dir=None):
        # initiate base class
        super().__init__(data_id=data_id, data_dir=data_dir)

        #: private dictionary containing loaded Variable instances,
        self._var_info = {}

        #: files that are supposed to be excluded from reading
        self.exclude_files = []

        #: files that were actually excluded from reading
        self.excluded_files = []

        self.is_vertical_profile = True

    @override
    def read_file(self, filename, vars_to_retrieve=None, remove_outliers=True) -> StationData:
        """Read EARLINET file and return it as instance of :class:`StationData`

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
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

        for var in vars_to_retrieve:
            if var in self.VAR_NAMES_FILE:  # make sure to only read what is supported by this file
                _vars.append(var)
            elif var in self.AUX_REQUIRES:
                _vars.append(var)
            else:
                raise ValueError(f"{var} is not supported")
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(_vars)

        # create empty data object (is dictionary with extended functionality)
        data_out = StationData()
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
            data_out["station_coords"]["longitude"] = data_out["longitude"] = (
                data_in.station_longitude
            )
            data_out["station_coords"]["latitude"] = data_out["latitude"] = (
                data_in.station_latitude
            )
            data_out["altitude"] = (
                data_in.altitude.values
            )  # Note altitude is an array for the data, station altitude is different
            data_out["station_coords"]["altitude"] = data_in.station_altitude
            data_out["altitude_attrs"] = (
                data_in.altitude.attrs
            )  # get attrs for altitude units + extra

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
            data_out["wavelength_emis"] = data_in.l0_wavelength
            data_out["zenith_angle"] = data_in.z_ref.values
            data_out["filename"] = filename

            loc_split = data_in.attrs["site_location"].split(", ")
            data_out["station_name"] = loc_split[0]
            if len(loc_split) > 1:
                data_out["country"] = loc_split[1]

            data_out["dtime"] = data_in.time.values

            for var in vars_to_read:
                data_out["var_info"][var] = {}
                unit_ok = False
                outliers_removed = False
                has_altitude = False

                netcdf_var_name = self.VAR_NAMES_FILE[var]
                # check if the desired variable is in the file
                if netcdf_var_name not in data_in.variables:
                    logger.warning(f"Variable {var} not found in file {filename}")
                    continue

                info = var_info[var]
                arr = data_in.variables[netcdf_var_name]
                val = np.squeeze(np.float64(arr))  # squeeze to 1D array

                # CONVERT UNIT
                unit = None

                unames = self.VAR_UNIT_NAMES[netcdf_var_name]
                for u in unames:
                    if u in arr.attrs:
                        unit = arr.attrs[u]
                if unit is None:
                    raise DataUnitError(f"Unit of {var} could not be accessed in file {filename}")
                if len(unit) > 0:
                    try:
                        to_unit = self._var_info[var].units
                        val = convert_unit(val, from_unit=unit, to_unit=to_unit)
                        unit = to_unit
                        unit_ok = True
                    except Exception as e:
                        logger.warning(
                            f"Failed to convert unit of {var} in file {filename} (EPROFILE): "
                            f"Error: {repr(e)}"
                        )
                else:
                    logger.warning(
                        f"Failed to convert unit of {var} in file {filename} (EPROFILE): Meaningful unit not found in file, so assuming unit_ok = True and that the units in the data are the same as in variables.ini"
                    )
                    unit_ok = True
                    unit = self._var_info[var].units

                if not val.ndim == 2:
                    raise DataDimensionError("EPROFILE data must be two dimensional")
                elif len(val) == 0:
                    continue  # no data
                # Remove NaN equivalent values
                val[val > self._MAX_VAL_NAN] = np.nan

                wvlg = var_info[var].wavelength_nm
                wvlg_str = self.META_NAMES_FILE["wavelength_emis"]

                if not wvlg == data_in.attrs[wvlg_str]:
                    logger.info("No wavelength match")
                    continue

                alt_data = data_in.variables[self.ALTITUDE_ID]

                alt_unit = alt_data.attrs["units"]
                to_alt_unit = const.VARS["alt"].units
                if not alt_unit == to_alt_unit:
                    try:
                        alt_unit_fac = get_unit_conversion_fac(alt_unit, to_alt_unit)
                        alt_data *= alt_unit_fac
                        alt_unit = to_alt_unit
                    except Exception as e:
                        logger.warning(f"Failed to convert unit: {repr(e)}")
                has_altitude = True

                # remove outliers from data, if applicable
                if remove_outliers and unit_ok:
                    # REMOVE OUTLIERS
                    outlier_mask = np.logical_or(val < info.minimum, val > info.maximum)
                    val[outlier_mask] = np.nan
                    outliers_removed = True

                # create instance of ProfileData
                profile = VerticalProfile(
                    data=val,
                    altitude=alt_data.values,
                    dtime=data_in.time.values,
                    var_name=var,
                    data_err=np.nan,  # EPROFILE does not provide error data
                    var_unit=unit,
                    altitude_unit=alt_unit,
                )

                # Write everything into profile
                data_out[var] = profile

            data_out["var_info"][var].update(
                unit_ok=unit_ok,
                err_read=False,  # EPROFILE foes not provide error data
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
        remove_outliers=True,
        pattern=None,
    ) -> UngriddedData:
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

        # if read_err is None:
        #     read_err = self.READ_ERR

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

        files = files[first_file : last_file + 1]

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
                    remove_outliers=remove_outliers,
                )
                if not any([var in stat.vars_available for var in vars_to_retrieve]):
                    logger.info(
                        f"Station {stat.station_name} contains none of the desired variables. Skipping station..."
                    )
                    continue
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
                # time = stat.dtime[0] # LB: Check this
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
                        add = np.prod(data.shape)
                        # err = val.data_err
                        metadata[meta_key]["var_info"]["altitude"] = via = {}

                        vi.update(val.var_info[var])
                        via.update(val.var_info["altitude"])
                    else:
                        add = 1
                        altitude = np.nan
                        data = val
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
                    data_obj._data[idx:stop, col_idx["time"]] = np.repeat(
                        stat.dtime, data.shape[-1]
                    )
                    data_obj._data[idx:stop, col_idx["stoptime"]] = np.repeat(
                        stat.dtime, data.shape[-1]
                    )
                    data_obj._data[idx:stop, col_idx["data"]] = data.flatten()
                    data_obj._data[idx:stop, col_idx["dataaltitude"]] = np.tile(
                        altitude, data.shape[0]
                    )
                    data_obj._data[idx:stop, col_idx["varidx"]] = var_idx

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

        files = files = (Path(self.data_dir) / "EXCLUDE").glob("*.txt")
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
                raise EprofileFileError(
                    f"Number of excluded files in {file} does not match the number of files found in the file"
                )
        self.exclude_files = list(dict.fromkeys(exclude))
        return self.exclude_files

    @override
    def get_file_list(self) -> list[Path]:
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
        exclude_files = {Path(file) for file in self._get_exclude_filelist()}
        if self.data_dir is None:
            raise ValueError("No data directory set")
        logger.info("Fetching EPROFILE data files...")

        all_files = set(f for f in Path(self.data_dir).rglob(self._FILEMASK) if f.is_file())
        files = list(all_files - exclude_files)
        self.files = files
        return files
