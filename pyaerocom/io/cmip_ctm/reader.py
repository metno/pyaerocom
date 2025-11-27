# from collections.abc import Callable
import logging
import os
import pathlib

import iris
import iris.cube
import iris.time
import numpy as np
import pandas as pd
import xarray as xr
from cf_units import Unit
from iris.util import equalise_attributes

from pyaerocom import const, GriddedData
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
from .model_variables import cmip_variables, cmip_aux_info, cmip_aliases

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
        self.aux_info = cmip_aux_info()
        self.cmip_aliases = cmip_aliases()
        # will contain info about what variables to read from files
        self.read_info = {}

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
        # some info on how to read data
        self._var_info = {}
        self.get_file_list()
        self.get_file_info()
        # dictionary with temporary data for computed variables
        self._temp_data = iris.cube.CubeList()
        # because iris uses standard_names for the variable naming, we need a mapping between aerocom and
        # standard names
        self._temp_var_mapping = {}
        self._model_vars_read = []
        self._model_vars_computed = []
        # will store the time base iris.Contraint of the data set
        self.date_range = None

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

    def read_var(
        self,
        var_name: str,
        ts_type: str | None = None,
        for_computation_flag: bool = False,
        **kwargs,
    ):
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. Supported are
            "hourly", "daily", "monthly" , "yearly".
        for_computation_flag : bool
            flag to indicate if the data used for computation of another variable only
            Will prevent the creation of a GriddedData object at the end

        Returns
        -------
        GriddedData
        """
        # this method is used recursively...
        if var_name not in self._var_info:
            self._var_info[var_name] = {}
            self._var_info[var_name]["to_read"] = []
            self._var_info[var_name]["to_compute"] = []

        if self.date_range is None:
            _start = None
            _stop = None
            # start and stop can either be a valid pandas.Timestamp or a string that pandas.Timestamp understands
            if "start" in kwargs:
                if isinstance(kwargs["start"], pd.Timestamp):
                    _start = kwargs["start"]
                elif isinstance(kwargs["start"], int):
                    _start = iris.time.PartialDateTime(f"{kwargs['start']}-01-01")

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
                elif isinstance(kwargs["stop"], int):
                    _stop = pd.Timestamp(f"{kwargs['stop']}-01-01")
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
            if _start is not None and _stop is not None:
                self.date_range = iris.Constraint(time=lambda cell: _start <= cell.point <= _stop)
            elif _start is not None:
                self.date_range = iris.Constraint(time=lambda cell: _start <= cell.point)
            elif _stop is not None:
                self.date_range = iris.Constraint(time=lambda cell: cell.point <= _stop)

        # test if var can be directly read
        if not self.has_var(var_name):
            # check for alias
            if var_name not in self.cmip_aliases:
                # additional_vars_needed = self.check_var_computable(var_name)
                pass
            # raise VarNotAvailableError(var_name)
        var = const.VARS[var_name]
        var_name_aerocom = var.var_name_aerocom
        #
        if self._data_dir is None:  # pragma: no cover
            raise ValueError("data_dir must be set before reading.")

        # determine which files to read
        _files_to_read = []
        for _file in self._file_info:
            if var_name != self._file_info[_file]["variable"]:
                # logging.info(f"Variable {var_name} not available for {_file}")
                continue
            else:
                logging.info(f"adding file{_file} to list of files to read...")
                _files_to_read.append(_file)

        if len(_files_to_read) == 0:
            # the pyaerocom variable can't be read directly; check if it can be computed
            # and read the necessary temporary data if possible
            # needs_computation_flag = self.check_and_read_aux_vars(var_name)
            aux_vars = self.check_and_read_aux_vars(var_name)
            # if for_computation_flag and len(self._temp_data.keys()) > 0:
            if not for_computation_flag and len(aux_vars) > 0:
                # calculate computed variable
                pass
                assert True
                # concatenate all data into single cube
                # perform the calculation

        else:
            cubelist = iris.load(
                _files_to_read,
                var_name,
            )
            # extract the interesting dates
            if isinstance(self.date_range, iris.Constraint):
                # some hacking for noleap calendars
                try:
                    cubelist = cubelist.extract(self.date_range)
                except TypeError:
                    logger.info(
                        "Info: forcing leap year calendar to non leap year model data. Necessary date corrections are still missing at this point."
                    )
                    tcoord = cubelist[0].coord("time")

                    tcoord.units = Unit(tcoord.units.origin, calendar="gregorian")
                    cubelist = cubelist.extract(self.date_range)

            if len(cubelist) > 1:
                # GriddedData can handle only a single cube, not a CubeList
                equalise_attributes(cubelist)
                cube = cubelist.concatenate_cube()
            else:
                cube = cubelist[0]

        if not for_computation_flag and len(_files_to_read) > 0:
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
        else:
            return cube

    def check_and_read_aux_vars(self, var_name: str):
        # check if a given variable can be computed from the found data files
        # and read the data into self.read_info
        logger.info(f"checking if var {var_name} is computable")
        if var_name in self.aux_info:
            # formula for variable computation is defined
            # check if the necessary variables are available
            logger.info(
                f"need var(s) {','.join(self.aux_info[var_name]['aux_vars'])} for computation of var {var_name}"
            )
            for _var_needed in self.aux_info[var_name]["aux_vars"]:
                logger.info(f"working on var {_var_needed} ")

                if _var_needed in self._vars and _var_needed not in self._model_vars_read:
                    logger.info(f"found var {_var_needed} in data dir")
                    self._temp_data.append(self.read_var(_var_needed, for_computation_flag=True))
                    self._temp_var_mapping[_var_needed] = self._temp_data[-1].name()
                    self._model_vars_read.append(_var_needed)
                    # self._var_info[var_name]["to_read"] = _var_needed
                    continue
                compute_vars = self.check_and_read_aux_vars(_var_needed)
                if len(compute_vars) > 0:
                    logger.info(f"found var {_var_needed} as computable using vars {compute_vars}")
                    # self._var_info["vars_to_read"]["to_compute"] = compute_vars
                    for _compute_var in compute_vars:
                        if self.aux_info[_var_needed]["how"] == "surface layer":
                            # We work on the last element of the cube list
                            z_coordinate_name = self._temp_data[-1].dim_coords[1].name()
                            p_max = max(self._temp_data[-1].dim_coords[1].points)
                            constraint = iris.Constraint(
                                coord_values={z_coordinate_name: lambda cell: cell == p_max}
                            )
                            self._temp_data.append(self._temp_data[-1].extract(constraint))
                        else:
                            raise NotImplementedError(
                                'only implemented the "surface_layer" how method for now'
                            )

                    continue
                alias_needed = self.check_aliases_available(_var_needed)
                if alias_needed:
                    logger.info(f"found var {_var_needed} as alias {alias_needed}")
                    self.read_var(alias_needed, for_computation_flag=True)
                    continue
                else:
                    logging.info(
                        f"missing variable {_var_needed} in provided model data directory and var is not computable"
                    )
                    return []
        else:
            logging.info(f"var {var_name} is not computable")
            return []

        return self.aux_info[var_name]["aux_vars"]

    def check_aliases_available(self, var_name: str):
        logger.info(f"checking if alias for var {var_name} is available in dataset...")
        if var_name in self.cmip_aliases:
            logger.info(f"alias for var {var_name} is {self.cmip_aliases[var_name]['alias']}...")
            if self.cmip_aliases[var_name]["alias"] in self._vars:
                logger.info(
                    f"var {self.cmip_aliases[var_name]['alias']} is available in dataset..."
                )
                return self.cmip_aliases[var_name]["alias"]
            else:
                logger.info(
                    f"var {self.cmip_aliases[var_name]['alias']} is NOT available in dataset..."
                )
                return False
        else:
            logger.info(f"no alias for var {var_name} defined.")
            return False
