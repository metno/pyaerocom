# from collections.abc import Callable
import logging
import os
import pathlib

import iris
import numpy as np
import pandas as pd
import xarray as xr
from iris.util import equalise_attributes

from pyaerocom import const, GriddedData
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.io.gridded_reader import GriddedReader
from pyaerocom.units.helpers import get_standard_unit

# from pyaerocom.units.units import Unit
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

    FILEMASK = "*_*_*_*_*_*_*.nc"

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
        self._files = sorted(self._files)
        return self._files

    def get_file_info(self):
        # get some info out of a file
        # time coverage and time resolution for now
        _years = []
        _vars = []
        _ts_types = []
        for _file in sorted(self._files):
            logger.info(f"Fetching file info for file {_file}...")
            self._last_file_data = xr.open_dataset(_file, decode_timedelta=True)
            self._file_info[_file] = {}
            self._file_info[_file]["time_cover"] = [
                self._last_file_data["time"].data.min(),
                self._last_file_data["time"].data.max(),
            ]
            self._file_info[_file]["years"] = np.unique(
                self._last_file_data[self.TIME_NAME].data.astype("datetime64[Y]").astype(int)
                + 1970
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
                self._last_file_data[self.TIME_NAME].data
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
        _start = None
        _stop = None
        # start and stop can either be a valid pandas.Timestamp or a string that pandas.Timestamp understands
        if "start" in kwargs:
            if isinstance(kwargs["start"], pd.Timestamp):
                _start = kwargs["start"]
            elif isinstance(kwargs["start"], str):
                try:
                    _start = pd.Timestamp(kwargs["start"])
                except ValueError:
                    logging.error(
                        f"Start time {kwargs['start']} is not valid. Using the entire file instead."
                    )
            else:
                logging.info(
                    f"Start time argument {kwargs['start']} given, but is not a valid type. Using the entire file instead."
                )

        if "stop" in kwargs:
            if isinstance(kwargs["stop"], pd.Timestamp):
                _stop = kwargs["stop"]
            elif isinstance(kwargs["stop"], str):
                try:
                    _stop = pd.Timestamp(kwargs["stop"])
                except ValueError:
                    logging.error(
                        f"Start time {kwargs['stop']} is not valid. Using the entire file instead."
                    )
            else:
                logging.info(
                    f"Stop time argument {kwargs['stop']} given, but is not a valid type. Using the entire file instead."
                )

        # create an iris.Constraint if the user gave a start and a stop date for reading
        date_range = None
        if _start is not None and _stop is not None:
            date_range = iris.Constraint(time=lambda cell: _start <= cell.point <= _stop)
        elif _start is not None:
            date_range = iris.Constraint(time=lambda cell: _start <= cell.point)
        elif _stop is not None:
            date_range = iris.Constraint(time=lambda cell: cell.point <= _stop)

        self.get_file_list()
        self.get_file_info()
        if not self.has_var(var_name):
            raise VarNotAvailableError(var_name)
        var = const.VARS[var_name]
        var_name_aerocom = var.var_name_aerocom
        #
        if self._data_dir is None:  # pragma: no cover
            raise ValueError("data_dir must be set before reading.")

        # determine which files to read
        _files_to_read = []
        for _file in self._file_info:
            if var_name != self._file_info[_file]["variable"]:
                logging.info(f"Variable {var_name} not available for {_file}")
                continue
            else:
                logging.info(f"adding file{_file} to list of files to read...")
                _files_to_read.append(_file)

        cubelist = iris.load(
            _files_to_read,
            var_name,
        )
        # extract the interesting dates
        if date_range is not None:
            cubelist = cubelist.extract(date_range)

        if len(cubelist) > 1:
            # GriddedData can handle only a single cube, not a CubeList
            equalise_attributes(cubelist)
            cube = cubelist.concatenate_cube()
        else:
            cube = cubelist[0]
        gridded = GriddedData(
            cube,
            var_name=var_name_aerocom,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
        )
        # add some more metadata
        _last_rev = self._file_info[_files_to_read[-1]]["realization"]
        gridded.metadata["data_id"] = self._data_id
        gridded.metadata["from_files"] = _files_to_read
        gridded.metadata["data_revision"] = _last_rev
        # not sure if this is needed
        gridded.convert_unit(get_standard_unit(var_name))
        return gridded
