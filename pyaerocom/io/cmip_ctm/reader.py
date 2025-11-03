# from collections.abc import Callable
import logging
import os
import pathlib

import iris
import numpy as np
import xarray as xr

from pyaerocom import const, GriddedData
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.io.gridded_reader import GriddedReader

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

# import warnings

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
    # FILE_FREQ_TEMPLATE = "*.nc"

    #: frequencies encoded in filenames
    # FREQ_CODES = {
    #     "hour": "hourly",
    #     "day": "daily",
    #     "month": "monthly",
    #     "fullrun": "yearly",
    # }

    # REVERSE_FREQ_CODES = {
    #     "hourly": "hour",
    #     "daily": "day",
    #     "monthly": "month",
    #     "yearly": "fullrun",
    # }

    # DEFAULT_FILE_NAME = "Base_day.nc"

    #: pattern for 4-digit years for 19XX and 20XX used for trend subdirectories
    # YEAR_PATTERN = r".*((?:19|20)\d\d).*"
    FILEMASK = "*_*_*_*_*_*_*.nc"

    # class _PrivateFields:
    #     filename: str | None = None
    #     filedata: xr.Dataset | None = None
    #     filepaths: list[str] | None = None
    #     files: list[str] | None = None
    #     data_dir: str | None = None
    #     file_pattern: re.Pattern
    #     ts_type: str | None = None
    #
    TIME_NAME = "time"

    # max allowed time step sizes (we allow for 10% error)
    TD_MAX_HOURLY = np.timedelta64(66, "m")
    TD_MAX_DAILY = np.timedelta64(1584, "m")
    TD_MAX_MONTHLY = np.timedelta64(52272, "m")

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | None = None,
        *,
        file_pattern: str | None = FILEMASK,
        **kwargs,
    ):
        # opened dataset (for performance boost), will be reset if data_dir is
        # changed
        # self._private = self._PrivateFields()

        self.var_map = cmip_variables()

        if data_dir is not None:
            if not isinstance(data_dir, str) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")

            self._data_dir = data_dir

        self._data_id = data_id
        self.file_pattern = file_pattern
        self._filename = None
        self._file_info = {}
        self._files = []
        self._tstypes = []
        self._years = []
        self._vars = []
        # self._last_file_data = None
        # self._private.filename = self.DEFAULT_FILE_NAME

    def get_file_list(self):
        # search for nc files recursively
        logger.info("Fetching CMIP data files recursively. This might take a while...")
        searchpath = pathlib.Path(self.data_dir)
        for _file in searchpath.rglob(self.file_pattern):
            if _file.is_file():
                self._files.append(str(_file))
        logger.info(
            f"Found {len(self._files)} sonde like data files in directory {self.data_dir}."
        )
        return self._files

    def get_file_info(self):
        # get some info out of a file
        # time coverage and time resolution for now
        for _file in self._files:
            logger.info(f"Fetching file info for file {_file}...")
            self._last_file_data = xr.open_dataset(_file, decode_timedelta=True)
            self._file_info[_file] = {}
            _years = []
            _vars = []
            _ts_types = []
            self._file_info[_file]["time_cover"] = [
                self._last_file_data["time"].data.min(),
                self._last_file_data["time"].data.max(),
            ]
            self._file_info[_file]["years"] = np.unique(
                self._last_file_data["time"].data.astype("datetime64[Y]").astype(int) + 1970
            )
            _years.extend(self._file_info[_file]["years"])
            _dummy = os.path.basename(_file).split("_")
            (
                self._file_info[_file]["variable"],
                self._file_info[_file]["source_type"],
                self._file_info[_file]["source_id"],
                self._file_info[_file]["experiment"],
                self._file_info[_file]["realization"],
                self._file_info[_file]["grid"],
            ) = _dummy[:6]
            self._file_info[_file]["tstype"] = self._get_time_resolution(
                self._last_file_data["time"].data
            )
            _vars.append(self._file_info[_file]["variable"])
            _ts_types.append(self._file_info[_file]["tstype"])

        self._last_file_data.close()
        self._years.extend(list(set(_years)))
        self._vars.extend(list(set(_vars)))
        self._tstypes.extend(list(set(_ts_types)))
        return self._file_info

    def _get_time_resolution(self, times) -> str:
        # determine the time resolution between time steps
        timedelta = times[1] - times[0]
        tstype = "yearly"
        if self.TD_MAX_MONTHLY > timedelta:
            tstype = "monthly"
        if self.TD_MAX_DAILY > timedelta:
            tstype = "daily"
        if self.TD_MAX_HOURLY > timedelta:
            tstype = "hourly"
        return tstype

    @property
    def data_id(self) -> str | None:
        return self._data_id

    @data_id.setter
    def data_id(self, val: str):
        self._data_id = val

    @property
    def data_dir(self) -> str:
        """
        Directory containing netcdf files
        """
        if self._data_dir is None:
            raise AttributeError("data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val: str):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
        self._data_dir = val
        self.filedata = None

    #
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
        return list(set(self._tstypes))

    @property
    def years_avail(self) -> list[str]:
        """
        Years available in loaded dataset
        """
        return list(set(self._years))

    @property
    def vars_provided(self) -> list[str]:
        """Variables provided by this dataset"""
        return list(set(self._vars))

    #
    # def _open_file(self):
    #     """
    #     Open current netcdf file
    #
    #     Returns
    #     -------
    #     dict(xarray.Dataset)
    #         Dict with years as keys and Datasets as items
    #
    #     """
    #     fps = self._filepaths
    #     ds = {}
    #     yrs = self._get_yrs_from_filepaths()
    #
    #     ts_type = self._ts_type
    #     fps = self._clean_filepaths(fps, yrs, ts_type)
    #
    #     if ts_type == "hourly" and len(fps) > 1:
    #         start_date = None
    #         end_date = None
    #         for fp in fps:
    #             with xr.open_dataset(fp, decode_timedelta=True) as nc:
    #                 file_start_date = nc["time"][:].data.min()
    #                 file_end_date = nc["time"][:].data.max()
    #
    #             start_date = min([x for x in [start_date, file_start_date] if x is not None])
    #             end_date = max([x for x in [end_date, file_end_date] if x is not None])
    #
    #         if (end_date - start_date) / np.timedelta64(1, "h") > (366 * 24):
    #             raise ValueError(
    #                 f"ts_type {ts_type} can not be hourly when using multiple years ({start_date} - {end_date})"
    #             )
    #
    #     logger.info(f"Opening {fps}")
    #     ds = xr.open_mfdataset(fps, chunks={"time": 24}, decode_timedelta=True)
    #
    #     self._private.filedata = ds
    #
    #     return ds
    #
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
        pass
        if "start" in kwargs:
            pass
        if "stop" in kwargs:
            pass

        self.get_file_list()
        self.get_file_info()
        if not self.has_var(var_name):
            raise VarNotAvailableError(var_name)
        var = const.VARS[var_name]
        var_name_aerocom = var.var_name_aerocom
        #
        if self._data_dir is None:  # pragma: no cover
            raise ValueError("data_dir must be set before reading.")

        for _file in self._file_info:
            if var_name != self._file_info[_file]["variable"]:
                logging.info(f"Variable {var_name} not available for {_file}")
                continue
            else:
                logging.info(f"opening file{_file}...")
                # _file_data = xr.open_dataset(_file, decode_timedelta=True)
                cube = iris.load_cube(_file, var_name)

            # try:
            #     cube = _file_data.to_iris()
            # except MemoryError as e:  # pragma: no cover
            #     raise NotImplementedError from e
        #
        # if ts_type == "hourly":
        #     cube.coord("time").convert_units("hours since 1900-01-01")
        gridded = GriddedData(
            cube,
            var_name=var_name_aerocom,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
        )
        #
        # # At this point a GriddedData object with name gridded should exist
        #
        gridded.metadata["data_id"] = self._data_id
        # gridded.metadata["from_files"] = self._filepaths
        #
        # gridded.convert_unit(get_standard_unit(var_name))
        # Remove unnecessary metadata. Better way to do this?
        # for metadata in ["current_date_first", "current_date_last"]:
        #     if metadata in gridded.metadata.keys():
        #         del gridded.metadata[metadata]
        return gridded

    # @staticmethod
    # def _preprocess_units(units: str, prefix: str | None = None):
    #     """
    #     Update units for certain variables
    #
    #     Parameters
    #     ----------
    #     units : str
    #         Current unit of data
    #     prefix : str, optional
    #         Variable prefix (e.g. AOD, AbsCoeff).
    #
    #     Returns
    #     -------
    #     str
    #         updated unit (where applicable)
    #
    #     """
    #     if units == "" and prefix == "AOD":  #
    #         return "1"
    #     elif units == "" and prefix == "AbsCoef":
    #         return "m-1"
    #     return units
