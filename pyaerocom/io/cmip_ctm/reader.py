# from collections.abc import Callable
import functools
import logging
import os
import re
# import warnings

import numpy as np
import xarray as xr
from pyaerocom import const
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.gridded_reader import GriddedReader
from pyaerocom.projection_information import ProjectionInformation
from pyaerocom.units.helpers import get_standard_unit
from pyaerocom.units.units import Unit

# from .additional_variables import (
#     add_dataarrays,
#     calc_concNhno3,
#     calc_concNnh3,
#     calc_concNnh4,
#     calc_concNno,
#     calc_concNno2,
#     calc_concNno3pm10,
#     calc_concNno3pm25,
#     calc_concno3pm10,
#     calc_concno3pm25,
#     calc_concso4t,
#     calc_concSso2,
#     calc_concsspm25,
#     calc_conNtnh_emep,
#     calc_conNtno3_emep,
#     calc_vmrno2,
#     calc_vmro3,
#     calc_vmrox_from_conc,
#     identity,
#     subtract_dataarrays,
#     update_EC_units,
#     calc_ratpm10pm25,
#     calc_ratpm25pm10,
# )
from .model_variables import cmip_variables
import pathlib

logger = logging.getLogger(__name__)


class ReadCmipCtm(GriddedReader):
    """
    Class for reading CMIP formatted model output. CMIP6 for now.

    Parameters
    ----------
    data_id : str
        string ID of model (e.g. "MPI-ESM-1-2-HAM")
    data_dir : str
        Base directory of CMIP data, containing one or more netcdf files.

    Attributes
    ----------
    data_id : str
        ID of model
    """

    #: supported filename template, freq-placeholder is for frequencies
    FILE_FREQ_TEMPLATE = "Base_{freq}.nc"

    #: frequencies encoded in filenames
    FREQ_CODES = {
        "hour": "hourly",
        "day": "daily",
        "month": "monthly",
        "fullrun": "yearly",
    }

    REVERSE_FREQ_CODES = {
        "hourly": "hour",
        "daily": "day",
        "monthly": "month",
        "yearly": "fullrun",
    }

    # DEFAULT_FILE_NAME = "Base_day.nc"

    #: pattern for 4-digit years for 19XX and 20XX used for trend subdirectories
    YEAR_PATTERN = r".*((?:19|20)\d\d).*"

    class _PrivateFields:
        filename: str | None = None
        filedata: xr.Dataset | None = None
        filepaths: list[str] | None = None
        files: list[str] | None = None
        data_dir: str | None = None
        file_pattern: re.Pattern
        ts_type: str | None = None

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | None = None,
        *,
        file_pattern: str | None = None,
        **kwargs,
    ):
        # opened dataset (for performance boost), will be reset if data_dir is
        # changed
        self._private = self._PrivateFields()

        self.var_map = cmip_variables()

        if file_pattern is None:
            # example CMIP data file name:
            # od550aer_AERmon_MPI-ESM-1-2-HAM_historical_r1i1p1f1_gn_185001-201412.nc
            file_pattern = rf".*{data_id}.*\.nc$"
        elif isinstance(file_pattern, str):
            file_pattern = file_pattern.format(freq=f"({'|'.join(self.FREQ_CODES.keys())})")
        else:
            raise TypeError(
                f"file_pattern should be of type str or None. Got {type(file_pattern)}"
            )

        try:
            file_pattern = re.compile(file_pattern)
        except re.error as e:
            raise ValueError(
                f"Provided file_pattern '{file_pattern}' can't be compiled to re.Pattern."
            ) from e

        self._private.file_pattern = file_pattern
        logger.info(
            f"Matching valid CMIP files based on the following regular expression: '{file_pattern.pattern}'"
        )

        if data_dir is not None:
            if not isinstance(data_dir, str) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")

            self._data_dir = data_dir

        self._data_id = data_id
        # self._private.filename = self.DEFAULT_FILE_NAME

    def _search_all_files(self):
        # folders = self._get_trend_folders_from_folder()
        # self._filepaths = self._get_files_from_folders(folders)
        pass

    def _get_files_from_folders(self, folders: list[str]):
        files: list[str] = []
        for d in folders:
            files += self._check_files_in_data_dir(d)
        return files

    @staticmethod
    @functools.cache
    def _get_year_from_nc(filename: str) -> int:
        with xr.open_dataset(filename, decode_timedelta=True) as nc:
            return np.mean(nc["time"][:]).data.astype("datetime64[Y]").astype(int) + 1970

    def _get_yrs_from_filepaths(self) -> list[str]:
        """Get available years of data from the filepaths. The year of the first
        Base_*.nc dataset in the filepath is read from the time-variable of the nc-file.

        :return: list of years as str
        """
        fps = self._filepaths
        yrs = []
        for fp in fps:
            try:
                yr = ReadCmipCtm._get_year_from_nc(fp)
            except Exception as ex:
                raise ValueError(f"Could not find any year in {fp}: {ex}")
            yrs.append(str(yr))

        return sorted(list(set(yrs)))

    def _get_tst_from_file(self, file: str):
        _, fname = os.path.split(file)

        # Note: This is to maintain previous functionality which would raise error if file did not match
        # Base_{freq} template. I am not sure if this should be the responsibility of this function, and
        # alternatively this can be removed (including the test).
        if self._private.file_pattern.match(file) is None:
            raise ValueError(
                f"The file '{file}' does not match file_pattern '{self._private.file_pattern}'"
            )

        for freq, tst in self.FREQ_CODES.items():
            if freq in fname:
                return tst

    def _clean_filepaths(self, filepaths: list[str], yrs: list[str], ts_type: str):
        clean_paths: set[str] = set()
        found_yrs: set[str] = set()

        yrs = [int(yr) for yr in yrs]
        for path in filepaths:
            file = os.path.split(path)[1]

            if self._get_tst_from_file(file) != ts_type:
                logger.debug(f"ignoring file {path}: not of type {ts_type}")
                continue

            try:
                yr = ReadCmipCtm._get_year_from_nc(path)
            except Exception as ex:
                raise ValueError(f"Could not find any year in {path}: {ex}")

            clean_paths.add(path)
            if yr not in yrs:
                raise ValueError(f"The year {yr} of {path} is not in {yrs}")

            if yr in found_yrs:
                continue

            found_yrs.add(yr)

        if len(found_yrs) != len(yrs):
            raise ValueError(
                f"A different amount of years {found_yrs} were found compared to {yrs} in {filepaths}"
            )

        return list(clean_paths)

    @property
    def data_id(self) -> str | None:
        return self._data_id

    @property
    def _data_dir(self) -> str:
        """
        Directory containing netcdf files
        """
        if self._private.data_dir is None:
            raise AttributeError("data_dir needs to be set before accessing")
        return self._private.data_dir

    @_data_dir.setter
    def _data_dir(self, val: str):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
        self._private.data_dir = val
        self._private.filedata = None
        self._search_all_files()
        self._private.files = self._filepaths

    @property
    def _filename(self) -> str | None:
        """
        Name of latest netcdf file read
        """
        return self._private.filename

    @_filename.setter
    def _filename(self, val: str):
        """
        Name of netcdf file
        """
        if not isinstance(val, str):  # pragma: no cover
            raise ValueError("needs str")
        elif val == self._private.filename:
            return
        self._private.filename = val
        self._private.filedata = None

    @property
    def _filepaths(self) -> list[str]:
        """
        Paths to data file
        """
        if self._data_dir is None and self._filepaths is None:  # pragma: no cover
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        return self._private.filepaths

    @_filepaths.setter
    def _filepaths(self, value: list[str]):
        if not isinstance(value, list):  # pragma: no cover
            raise ValueError("needs to be list of strings")
        self._private.filepaths = value

    @property
    def _filedata(self) -> xr.Dataset:
        """
        Loaded netcdf file (:class:`xarray.Dataset`)
        """
        if self._private.filedata is None:
            self._open_file()
        return self._private.filedata

    @functools.cache
    def _check_files_in_data_dir(self, data_dir: str):
        """
        Check for data files in input data directory

        Parameters
        ----------
        data_dir : str
            directory to be searched.

        Raises
        ------
        FileNotFoundError
            if no EMEP files can be identified

        Returns
        -------
        list
            list of file matches

        """
        files: list[str] = [str(p) for p in pathlib.Path(data_dir).iterdir() if p.is_file()]

        matches = [
            str(p)
            for p in pathlib.Path(data_dir).iterdir()
            if self._private.file_pattern.match(p.name) is not None
        ]
        if len(matches) == 0:
            raise FileNotFoundError(
                f"No valid model files could be found in {data_dir} for any of the "
                f"supported files: {files}"
            )
        return matches

    @property
    def _ts_type(self) -> str:
        """
        Frequency of time dimension of current data file

        Raises
        ------
        AttributeError
            if :attr:`filename` is not set.

        Returns
        -------
        str
            current ts_type.

        """
        if self._private.ts_type is None:
            return self._ts_type_from_filename(self._filename)
        return self._private.ts_type

    @property
    def ts_types(self) -> list[str]:
        """
        List of available frequencies

        Raises
        ------
        AttributeError
            if :attr:`data_dir` is not set.

        Returns
        -------
        list
            list of available frequencies

        """
        if not isinstance(self._private.files, list):
            raise AttributeError("please set data_dir first")
        tsts = []
        for file in self._private.files:
            tsts.append(self._ts_type_from_filename(file))
        return list(set(tsts))

    @property
    def years_avail(self) -> list[str]:
        """
        Years available in loaded dataset
        """
        years = self._get_yrs_from_filepaths()

        years = list(np.unique(years))
        return sorted(years)

    @property
    def vars_provided(self) -> list[str]:
        """Variables provided by this dataset"""
        # return list(self.var_map) + list(self.AUX_REQUIRES)
        return list(self.var_map)

    def _open_file(self):
        """
        Open current netcdf file

        Returns
        -------
        dict(xarray.Dataset)
            Dict with years as keys and Datasets as items

        """
        fps = self._filepaths
        ds = {}
        yrs = self._get_yrs_from_filepaths()

        ts_type = self._ts_type
        fps = self._clean_filepaths(fps, yrs, ts_type)

        if ts_type == "hourly" and len(fps) > 1:
            start_date = None
            end_date = None
            for fp in fps:
                with xr.open_dataset(fp, decode_timedelta=True) as nc:
                    file_start_date = nc["time"][:].data.min()
                    file_end_date = nc["time"][:].data.max()

                start_date = min([x for x in [start_date, file_start_date] if x is not None])
                end_date = max([x for x in [end_date, file_end_date] if x is not None])

            if (end_date - start_date) / np.timedelta64(1, "h") > (366 * 24):
                raise ValueError(
                    f"ts_type {ts_type} can not be hourly when using multiple years ({start_date} - {end_date})"
                )

        logger.info(f"Opening {fps}")
        ds = xr.open_mfdataset(fps, chunks={"time": 24}, decode_timedelta=True)

        self._private.filedata = ds

        return ds

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "ReadCmipCtm"

    def has_var(self, var_name: str) -> bool:
        """Check if variable is supported

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        avail = self.vars_provided
        if var_name in avail or const.VARS[var_name].var_name_aerocom in avail:
            return True
        return False

    def _ts_type_from_filename(self, filename: str) -> str:
        """
        Get ts_type from filename

        Parameters
        ----------
        filename : str

        Raises
        ------
        ValueError
            if ts_type cannot be inferred from filename.

        Returns
        -------
        tstype : str
        """
        filename = os.path.basename(filename)
        for substr, tstype in self.FREQ_CODES.items():
            if substr in filename:
                return tstype
        raise ValueError(f"Failed to retrieve ts_type from filename {filename}")

    def _filename_from_ts_type(self, ts_type: str):
        """
        Infer file name of data based on input ts_type

        Parameters
        ----------
        ts_type : str
            desired time freq of data

        Raises
        ------
        ValueError
            On wrong ts_type.

        Returns
        -------
        fname : str
            Name of data file based on ts_type
            freq.

        """
        if ts_type not in self.REVERSE_FREQ_CODES:
            raise ValueError(f"unknown ts_type={ts_type}")
        freq = self.REVERSE_FREQ_CODES[ts_type]
        return self.FILE_FREQ_TEMPLATE.format(freq=freq)

    def _load_var(self, var_name_aerocom: str, ts_type: str):
        """
        Load variable data as :class:`xarray.DataArray`.

        This combines both, variables that can be read directly and auxiliary
        variables that are computed.

        Parameters
        ----------
        var_name_aerocom : str
            variable name
        ts_type : str
            desired frequency

        Raises
        ------
        VarNotAvailableError
            if input variable is not available

        Returns
        -------
        xarray.DataArray
            loaded data
        ProjectionInformation
            projection of variable

        """
        if var_name_aerocom in self.var_map:  # can be read
            return self._read_var_from_file(var_name_aerocom, ts_type)
        raise VarNotAvailableError(
            f"Variable {var_name_aerocom} is not supported"
        )  # pragma: no cover

    def read_var(self, var_name: str, ts_type: str | None = None, **kwargs):
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. Supported are
            "hourly", "daily", "monthly" , "yearly".

        Returns
        -------
        GriddedData
        """
        if not self.has_var(var_name):
            raise VarNotAvailableError(var_name)
        var = const.VARS[var_name]
        var_name_aerocom = var.var_name_aerocom

        if self._data_dir is None:  # pragma: no cover
            raise ValueError("data_dir must be set before reading.")
        elif self._filename is None and ts_type is None:  # pragma: no cover
            raise ValueError("please specify ts_type")
        elif ts_type is not None:
            # filename and ts_type are set. update filename if ts_type suggests
            # that current file has different resolution
            self._filename = self._filename_from_ts_type(ts_type)
        self._private.ts_type = ts_type

        ts_type = self._ts_type

        arr, proj_info = self._load_var(var_name_aerocom, ts_type)
        if arr.units in Unit._UALIASES:
            arr.attrs["units"] = Unit._UALIASES[arr.units]
        try:
            cube = arr.to_iris()
        except MemoryError as e:  # pragma: no cover
            raise NotImplementedError from e

        if ts_type == "hourly":
            cube.coord("time").convert_units("hours since 1900-01-01")
        gridded = GriddedData(
            cube,
            var_name=var_name_aerocom,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
            proj_info=proj_info,
        )

        # At this point a GriddedData object with name gridded should exist

        gridded.metadata["data_id"] = self._data_id
        gridded.metadata["from_files"] = self._filepaths

        gridded.convert_unit(get_standard_unit(var_name))
        # Remove unnecessary metadata. Better way to do this?
        for metadata in ["current_date_first", "current_date_last"]:
            if metadata in gridded.metadata.keys():
                del gridded.metadata[metadata]
        return gridded

    def _read_var_from_file(self, var_name_aerocom: str, ts_type: str):
        """
        Read variable data from file as :class:`xarray.DataArray`.

        See also :func:`_load_var`

        Parameters
        ----------
        var_name_aerocom : str
            variable name
        ts_type : str
            desired frequency

        Raises
        ------
        VarNotAvailableError
            if input variable is not available

        Returns
        -------
        xarray.DataArray
            loaded data
        ProjectionInformation
            projection of variable

        """
        emep_var = self.var_map[var_name_aerocom]

        try:
            filedata = self._filedata
            data = filedata[emep_var]
            proj_info = ProjectionInformation.from_xarray(filedata, emep_var)
        except KeyError:
            raise VarNotAvailableError(
                f"{var_name_aerocom} ({emep_var}) not available in {self._filename}"
            )
        data.attrs["long_name"] = var_name_aerocom
        data.time.attrs["long_name"] = "time"
        data.time.attrs["standard_name"] = "time"
        prefix = emep_var.split("_")[0]
        data.attrs["units"] = self._preprocess_units(data.units, prefix)
        return data, proj_info

    @staticmethod
    def _preprocess_units(units: str, prefix: str | None = None):
        """
        Update units for certain variables

        Parameters
        ----------
        units : str
            Current unit of data
        prefix : str, optional
            Variable prefix (e.g. AOD, AbsCoeff).

        Returns
        -------
        str
            updated unit (where applicable)

        """
        if units == "" and prefix == "AOD":  #
            return "1"
        elif units == "" and prefix == "AbsCoef":
            return "m-1"
        return units
