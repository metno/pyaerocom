import fnmatch
import logging
import os
import warnings
from glob import glob
from pathlib import Path

import iris
import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import const
from pyaerocom.exceptions import (
    DataCoverageError,
    DataQueryError,
    DataSourceError,
    FileConventionError,
    TemporalResolutionError,
    VariableDefinitionError,
    VarNotAvailableError,
)
from pyaerocom.griddeddata import GriddedData
from pyaerocom.units.datetime import get_highest_resolution, sort_ts_types, to_pandas_timestamp
from pyaerocom.helpers import isnumeric
from pyaerocom.io import AerocomBrowser
from pyaerocom.io.aux_components_fun import (
    calc_concNhno3_from_vmr,
    calc_concNnh3_from_vmr,
    calc_concNnh4,
    calc_concNno3pm10,
    calc_concNno3pm25,
    calc_concno3pm10,
    calc_concno3pm25,
    calc_concNtnh,
    calc_concNtno3,
    calc_sspm25,
)
from pyaerocom.io.aux_read_cubes import (
    add_cubes,
    compute_angstrom_coeff_cubes,
    divide_cubes,
    mmr_from_vmr,
    multiply_cubes,
    subtract_cubes,
)
from pyaerocom.io.file_conventions import FileConventionRead
from pyaerocom.io.gridded_reader import GriddedReader
from pyaerocom.io.helpers import add_file_to_log
from pyaerocom.io.iris_io import concatenate_iris_cubes, load_cubes_custom
from pyaerocom.metastandards import AerocomDataID
from pyaerocom.units.datetime import TsType
from pyaerocom.variable import Variable

logger = logging.getLogger(__name__)


class ReadGridded(GriddedReader):
    """Class for reading gridded files using AeroCom file conventions

    Attributes
    ----------
    data_id : str
        string ID for model or obsdata network (see e.g. Aerocom interface map
        plots lower left corner)
    data : GriddedData
        imported data object
    data_dir : str
        directory containing result files for this model
    start : pandas.Timestamp
        start time for data import
    stop : pandas.Timestamp
        stop time for data import
    file_convention : FileConventionRead
        class specifying details of the file naming convention for the model
    files : list
        list containing all filenames that were found.
        Filled, e.g. in :func:`ReadGridded.get_model_files`
    from_files : list
        List of all netCDF files that were used to concatenate the current
        data cube (i.e. that can be based on certain matching settings such as
        var_name or time interval).
    ts_types : list
        list of all sampling frequencies (e.g. hourly, daily, monthly) that
        were inferred from filenames (based on Aerocom file naming convention)
        of all files that were found
    vars : list
        list containing all variable names (e.g. od550aer) that were inferred
        from filenames based on Aerocom model file naming convention
    years : list
        list of available years as inferred from the filenames in the data
        directory.

    Parameters
    ----------
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    data_dir : str, optional
        directory containing data files. If provided, only this directory is
        considered for data files, else the input `data_id` is used to search
        for the corresponding directory.
    file_convention : str
        string ID specifying the file convention of this model (cf.
        installation file `file_conventions.ini <https://github.com/metno/
        pyaerocom/blob/master/pyaerocom/data/file_conventions.ini>`__)
    init : bool
        if True, the model directory is searched (:func:`search_data_dir`) on
        instantiation and if it is found, all valid files for this model are
        searched using :func:`search_all_files`.

    """

    CONSTRAINT_OPERATORS = {
        "==": np.equal,
        "!=": np.not_equal,
        "<": np.less,
        "<=": np.less_equal,
        ">": np.greater,
        ">=": np.greater_equal,
    }

    AUX_REQUIRES = {
        "ang4487aer": ("od440aer", "od870aer"),
        "angabs4487aer": ("abs440aer", "abs870aer"),
        "od550gt1aer": ("od550aer", "od550lt1aer"),
        "wetoa": ("wetpoa", "wetsoa"),
        "dryoa": ("drypoa", "drysoa"),
        "conc*": ("mmr*", "rho"),
        "sc550dryaer": ("ec550dryaer", "ac550dryaer"),
        "mmr*": ("vmr*",),
        "rho": ("ts", "ps"),
        "concox": ("concno2", "conco3"),
        "vmrox": ("vmrno2", "vmro3"),
        "fmf550aer": ("od550lt1aer", "od550aer"),
        "concno3": ("concno3c", "concno3f"),
        "concprcpoxn": ("wetoxn", "pr"),
        "concprcpoxs": ("wetoxs", "pr"),
        "concprcprdn": ("wetrdn", "pr"),
        "concsspm10": ("concss25", "concsscoarse"),
        "concsspm25": ("concss25", "concsscoarse"),
        "concno3pm10": ("concno3f", "concno3c"),
        "concno3pm25": ("concno3f", "concno3c"),
        "concNno3pm10": ("concno3f", "concno3c"),
        "concNno3pm25": ("concno3f", "concno3c"),
        "concNhno3": ("vmrhno3",),
        "concNtno3": ("concno3f", "concno3c", "vmrhno3"),
        "concNnh3": ("vmrnh3",),
        "concNnh4": ("concnh4",),
        "concNtnh": ("concnh4", "vmrnh3"),
    }

    AUX_ALT_VARS = {
        "od440aer": ["od443aer"],
        "od870aer": ["od865aer"],
        "ac550dryaer": ["ac550aer"],
    }

    AUX_FUNS = {
        "ang4487aer": compute_angstrom_coeff_cubes,
        "angabs4487aer": compute_angstrom_coeff_cubes,
        "od550gt1aer": subtract_cubes,
        "wetoa": add_cubes,
        "dryoa": add_cubes,
        "sc550dryaer": subtract_cubes,
        "conc*": multiply_cubes,
        "mmr*": mmr_from_vmr,
        "concox": add_cubes,
        "vmrox": add_cubes,
        "fmf550aer": divide_cubes,
        "concno3": add_cubes,
        "concsspm10": add_cubes,
        "concsspm25": calc_sspm25,
        "concno3pm10": calc_concno3pm10,
        "concno3pm25": calc_concno3pm25,
        "concNno3pm10": calc_concNno3pm10,
        "concNno3pm25": calc_concNno3pm25,
        "concNhno3": calc_concNhno3_from_vmr,
        "concNtno3": calc_concNtno3,
        "concNnh3": calc_concNnh3_from_vmr,
        "concNnh4": calc_concNnh4,
        "concNtnh": calc_concNtnh,
        # 'mec550*'      :    divide_cubes,
        # 'tau*'         :    lifetime_from_load_and_dep
    }

    #: Additional arguments passed to computation methods for auxiliary data
    #: This is optional and defined per-variable like in AUX_FUNS
    AUX_ADD_ARGS = {
        "concprcpoxn": dict(
            ts_type="daily", prlim=0.1e-3, prlim_units="m d-1", prlim_set_under=np.nan
        ),
        "concprcpoxs": dict(
            ts_type="daily", prlim=0.1e-3, prlim_units="m d-1", prlim_set_under=np.nan
        ),
        "concprcprdn": dict(
            ts_type="daily", prlim=0.1e-3, prlim_units="m d-1", prlim_set_under=np.nan
        ),
    }

    _data_dir = ""

    VERT_ALT = {"Surface": "ModelLevel"}

    def __init__(self, data_id=None, data_dir=None, file_convention="aerocom3"):
        self._data_dir = None

        #: data_id of gridded dataset
        self._data_id = data_id

        # file naming convention. Default is aerocom3 file convention, change
        # using self.file_convention.import_default("aerocom2"). Is
        # automatically updated in class ReadGridded
        self.file_convention = FileConventionRead(file_convention)

        self.file_info = None

        #: List of unique Aerocom variable names that were identified from
        #: the filenames in the data directory
        self._vars_2d = []
        self._vars_3d = []

        #: This object can be used to
        self.browser = AerocomBrowser()

        # these can be filled using method add_aux_compute and they will not
        # affect global settings of the reader class
        self._aux_requires = {}
        self._aux_funs = {}

        #: quick access to variables that can be computed (will be filled and
        #: handles automatically)
        self._aux_avail = {}

        self.ignore_vert_code = False
        if data_dir is not None:
            self.data_dir = data_dir
        elif data_id:
            self.search_data_dir()
        if self.data_dir is not None:
            try:
                self.search_all_files()
            except DataCoverageError as e:
                logger.warning(repr(e))

    @property
    def data_id(self) -> str:
        """
        Data ID of dataset
        """
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        if val is None:
            val = ""
        if not isinstance(val, str):
            raise ValueError("Invalid input for data_id, need str")
        self._data_id = val

    @property
    def data_dir(self) -> str:
        """
        Directory where data files are located
        """
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val):
        if isinstance(val, Path):
            val = str(val)
        if not isinstance(val, str) or not os.path.isdir(val):
            raise FileNotFoundError(f"Input data directory {val} does not exist")
        self._data_dir = val
        self.reinit()

    @property
    def years_avail(self) -> list:
        """
        Years available in dataset
        """
        if self.file_info is None:
            self.search_all_files()
        return sorted(self.file_info.year.unique())

    @property
    def experiments(self) -> list:
        """
        List of all experiments that are available in this dataset
        """
        if self.file_info is None:
            self.search_all_files()
        return sorted(self.file_info.experiment.unique())

    @property
    def files(self) -> list:
        """
        List of data files
        """
        if self.file_info is None:
            self.search_all_files()
        return [os.path.join(self.data_dir, x) for x in sorted(self.file_info.filename.values)]

    @property
    def ts_types(self):
        """Available frequencies"""
        return self.file_info.ts_type.unique()

    @property
    def vars_filename(self):
        return sorted(self._vars_2d + self._vars_3d)

    @property
    def vars(self):
        from pyaerocom.exceptions import DeprecationError

        raise DeprecationError(
            "Attribute vars is deprecated in ReadGridded. Please use vars_filename instead"
        )

    @property
    def vars_provided(self):
        """Variables provided by this dataset"""
        return self._get_vars_provided()

    @property
    def file_type(self):
        """File type of data files"""
        return const.GRID_IO.FILE_TYPE

    @property
    def TS_TYPES(self):
        """List with valid filename encryptions specifying temporal resolution

        Update 7.11.2019: not in use anymore due to improved handling of
        all possible frequencies now using TsType class.
        """
        return const.GRID_IO.TS_TYPES

    @property
    def start(self):
        """First available year in the dataset (inferred from filenames)

        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily
        given that data from this year is available for all variables in
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years_avail) == 0:
            raise AttributeError(
                "No information about available years accessible"
                "please run method search_all_files first"
            )
        yr = sorted(self.years_avail)[0]
        if yr == 9999:
            yr = 2222
        return to_pandas_timestamp(yr)

    @property
    def stop(self):
        """Last available year in the dataset (inferred from filenames)

        Note
        ----
        This is not variable or ts_type specific, so it is not necessarily
        given that data from this year is available for all variables in
        :attr:`vars` or all frequencies liste in :attr:`ts_types`
        """
        if len(self.years_avail) == 0:
            raise AttributeError(
                "No information about available years accessible"
                "please run method search_all_files first"
            )
        years = sorted(self.years_avail)
        year = years[-1]

        if year == 9999:
            logger.warning(
                "Data contains climatology. Will be ignored as stop time, using last year"
            )
            if len(years) == 1:
                year = 2222
            else:
                year = years[-2]

        return to_pandas_timestamp(f"{year}-12-31 23:59:59")

    def reinit(self):
        """Reinit everything that is loaded specific to data_dir"""
        self.file_info = None
        self._vars_2d = []
        self._vars_3d = []

    def _get_vars_provided(self):
        """(Private method) get all variables provided"""
        _vars = []
        _vars.extend(self.vars_filename)

        for aux_var in self.AUX_REQUIRES:
            if "*" in aux_var:
                continue
            if aux_var not in _vars and self.check_compute_var(aux_var):
                _vars.append(aux_var)
        for aux_var in self._aux_requires:
            if "*" in aux_var:
                continue
            if aux_var not in _vars and self.check_compute_var(aux_var):
                _vars.append(aux_var)

        # also add standard names of 3D variables if not already in list
        for var in self._vars_3d:
            var = var.lower().replace("3d", "")
            if var not in _vars:
                _vars.append(var)
        return _vars

    def _check_aux_compute_access(self, var_name):
        """Check if input var_name can be computed

        Note
        ----
        Does not check variable families (e.g. conc*) which is done via
        :func:`_check_var_match_pattern`. Only checks entries in
        :attr:`AUX_REQUIRES` and :attr:`aux_requires`.

        Parameters
        ----------
        var_name : str
            input variable name that is supposed to be checked

        Returns
        -------
        bool
            True, if variable can be computed, else False
        """
        if var_name in self._aux_requires and var_name in self._aux_funs:
            vars_req = self._aux_requires[var_name]
            fun = self._aux_funs[var_name]
        elif var_name in self.AUX_REQUIRES and var_name in self.AUX_FUNS:
            vars_req = self.AUX_REQUIRES[var_name]
            fun = self.AUX_FUNS[var_name]
        else:
            return False
        vars_to_read = []
        for i, var in enumerate(vars_req):
            try:
                # the variable might be updated in _check_var_avail
                vars_to_read.append(self._check_var_avail(var))
            except (VarNotAvailableError, VariableDefinitionError):
                return False
        if not len(vars_to_read) == len(vars_req):
            return False
        self._aux_avail[var_name] = (vars_to_read, fun)
        return True

    def _check_var_match_pattern(self, var_name):
        """Check if input variable can be accessed via auxiliary variable family

        E.g. if var_name is concpm10 and mmrpm10 and rho are available

        Parameters
        ----------
        var_name : str
            variable that is supposed to be read

        Returns
        -------
        bool
            True if variable can be read, else False
        """
        vars_found = []
        for pattern in self.registered_var_patterns:
            if fnmatch.fnmatch(var_name, pattern):
                vars_required = self.AUX_REQUIRES[pattern]
                for addvar in vars_required:
                    if "*" not in addvar:
                        vars_found.append(addvar)
                    else:
                        _addvar = var_name
                        spl1 = pattern.split("*")
                        spl2 = addvar.split("*")
                        if len(spl1) != len(spl2):
                            raise AttributeError(
                                "variable patterns in "
                                "AUX_REQUIRES and corresponding "
                                "values (with * in name) need "
                                "to have the same number of "
                                "wildcard delimiters"
                            )
                        for i, substr in enumerate(spl1):
                            if bool(substr):
                                _addvar = _addvar.replace(substr, spl2[i])
                        vars_found.append(_addvar)

                if len(vars_found) == len(vars_required):
                    all_ok = True
                    vars_to_read = []
                    for var in vars_found:
                        try:
                            vars_to_read.append(self._check_var_avail(var))
                        except (VarNotAvailableError, VariableDefinitionError):
                            all_ok = False
                            break

                    if all_ok:
                        fun = self.AUX_FUNS[pattern]
                        self.add_aux_compute(var_name, vars_required=vars_to_read, fun=fun)
                        self._aux_avail[var_name] = (vars_to_read, fun)
                        return True
        return False

    def _get_aux_vars_and_fun(self, var_to_compute):
        """Helper that searches auxiliary variables for computation of input var

        Parameters
        ----------
        var_to_compute : str
            one of the auxiliary variables that is supported by this interface
            (cf. :attr:`AUX_REQUIRES`)

        Raises
        ------
        VarNotAvailableError
            if one of the required variables for computation is not available
            in the data

        Returns
        -------
        list
            list of variables that are used as input for computation method
            of input variable
        callable
            function that is used to compute input variable
        """
        if var_to_compute not in self._aux_avail:
            if not self.check_compute_var(var_to_compute):
                raise VarNotAvailableError(f"Variable {var_to_compute} cannot be computed")
        return self._aux_avail[var_to_compute]

    def check_compute_var(self, var_name):
        """Check if variable name belongs to family that can be computed

        For instance, if input var_name is `concdust` this method will check
        :attr:`AUX_REQUIRES` to see if there is a variable family pattern
        (`conc*`) defined that specifies how to compute these variables. If
        a match is found, the required variables and computation method is
        added via :func:`add_aux_compute`.

        Parameters
        -----------
        var_name : str
            variable name to be checked

        Returns
        -------
        bool
            True if match is found, else False
        """

        if "*" in var_name:
            raise VariableDefinitionError(f"Invalid variable name {var_name}. Must not contain *")
        if var_name in self._aux_avail:
            return True
        elif self._check_aux_compute_access(var_name):
            return True
        return self._check_var_match_pattern(var_name)

    def _check_var_avail(self, var):
        if var in self.vars_filename:
            return var

        if var in self.AUX_ALT_VARS:
            for alt_var in self.AUX_ALT_VARS[var]:
                if alt_var in self.vars_filename:
                    return alt_var

        v = const.VARS[var]

        for alias in v.aliases:
            if alias in self.vars_filename:
                return alias
        raise VarNotAvailableError(f"Var {var} is not available in data...")

    def has_var(self, var_name):
        """Check if variable is available

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        # vars_provided includes variables that can be read and variables that
        # can be computed. It does not consider variable families that may be
        # able to be computed or alias matches
        avail = self.vars_provided
        if var_name in avail:
            return True
        try:
            var = const.VARS[var_name]
        except VariableDefinitionError as e:
            logger.warning(repr(e))
            return False

        if self.check_compute_var(var_name):
            return True

        for alias in var.aliases:
            if alias in avail:
                return True

        if var.is_alias and var.var_name_aerocom in avail:
            return True

        return False

    def _get_years_to_load(self, start=None, stop=None):
        """Array containing year numbers that are supposed to be loaded

        Returns
        -------
        ndarray
            all years to be loaded
        """
        start_provided = False
        if start is None:
            start = self.start
            if start.year == 2222:
                return np.array([9999])
        else:
            start_provided = True
            if isinstance(start, int) and start == 9999:
                return np.array([9999])
            start = to_pandas_timestamp(start)

        if stop is None:
            if start_provided:
                stop = to_pandas_timestamp(start)
            else:
                stop = self.stop
        else:
            stop = to_pandas_timestamp(stop)
            stop -= np.timedelta64(
                1, "s"
            )  # subtract one second to end up at the end of previous year
        if const.MIN_YEAR > start.year:
            logger.warning(
                f"First available year {start} of data {self.data_id} is smaller "
                f"than supported first year {const.MIN_YEAR}."
            )
            start = const.MIN_YEAR
        if const.MAX_YEAR < stop.year:
            raise ValueError(
                f"Last available year {stop} of data {self.data_id} is larger "
                f"than supported last year {const.MAX_YEAR}."
            )
            stop = const.MAX_YEAR

        if start and stop:
            return np.arange(start.year, stop.year + 1, 1)

        if not self.years_avail:
            raise AttributeError(
                "No information available for available "
                "years. Please run method "
                "search_all_files first"
            )
        return np.array(self.years_avail)

    def search_data_dir(self):
        """Search data directory based on model ID

        Wrapper for method :func:`search_data_dir_aerocom`

        Returns
        -------
        str
            data directory

        Raises
        ------
        IOError
            if directory cannot be found
        """
        _dir = self.browser.find_data_dir(self.data_id)
        self.data_dir = _dir
        return _dir

    @staticmethod
    def _eval_data_id(data_id):
        """
        Extract meta information from data_id

        Parameters
        ----------
        data_id : str
            string specifying model and other relevant information. In the
            best case following AeroCom Phase III conventions, that is,
            following the template specified in :class:`AerocomDataID`.

        Returns
        -------
        vals : list
            list containing successfully extracted information from data_id
        """

        vals = AerocomDataID(data_id).values
        return vals

    def _update_file_convention(self, files):
        """Update current file convention based on input files

        Loops over all files in input list and as updates the file convention
        based on the first file in list that matches one of the registered
        conventions.

        Updates class :attr:`file_convention`

        Raises
        ------
        FileNotFoundError
            if none of the input files matches a registered convention.
        """
        for file in files:
            try:
                self.file_convention.from_file(os.path.basename(file))
                return
            except Exception:
                pass

        raise FileNotFoundError(
            f"None of the available files in {self.data_dir} matches a "
            f"registered pyaerocom file convention"
        )

    def _evaluate_fileinfo(self, files):
        result = []
        _vars_temp = []
        _vars_temp_3d = []

        for _file in files:
            # TODO: resolve this in a more general way...
            if "ModelLevelAtStations" in _file:
                logger.info(f"Ignoring file {_file}")
                continue
            try:
                info = self.file_convention.get_info_from_file(_file)
                if not self.data_id:
                    self.data_id = info["data_id"]
                var_name = info["var_name"]
                _is_3d = False
                if is_3d(var_name):
                    _vars_temp_3d.append(var_name)
                    _is_3d = True
                else:
                    _vars_temp.append(var_name)

                if not TsType.valid(info["ts_type"]):  # in self.TS_TYPES:
                    raise TemporalResolutionError(f"Invalid frequency {info['ts_type']}")

                (model, meteo, experiment, pert) = self._eval_data_id(info["data_id"])
                result.append(
                    [
                        var_name,
                        info["year"],
                        info["ts_type"],
                        info["vert_code"],
                        self.data_id,
                        model,
                        meteo,
                        experiment,
                        pert,
                        info["is_at_stations"],
                        _is_3d,
                        os.path.basename(_file),
                    ]
                )

            except (FileConventionError, DataSourceError, TemporalResolutionError) as e:
                msg = f"Failed to import file\n{_file}\nModel: {self.data_id}\nError: {e}"
                logger.warning(msg)
                if const.WRITE_FILEIO_ERR_LOG:
                    add_file_to_log(_file, msg)

        if len(_vars_temp + _vars_temp_3d) == 0:
            raise AttributeError("Failed to extract information from filenames")

        self._vars_2d = sorted(set(_vars_temp))
        self._vars_3d = sorted(set(_vars_temp_3d))
        return result

    def _fileinfo_to_dataframe(self, result):
        header = [
            "var_name",
            "year",
            "ts_type",
            "vert_code",
            "data_id",
            "name",
            "meteo",
            "experiment",
            "perturbation",
            "is_at_stations",
            "3D",
            "filename",
        ]

        df = pd.DataFrame(result, columns=header)
        df.sort_values(
            [
                "var_name",
                "year",
                "ts_type",
                "data_id",
                "name",
                "meteo",
                "experiment",
                "perturbation",
                "is_at_stations",
                "3D",
            ],
            inplace=True,
        )

        uv = df.vert_code.unique()
        if len(uv) == 1 and uv[0] == "":
            self.ignore_vert_code = True
        return df

    def search_all_files(self, update_file_convention=True):
        """Search all valid model files for this model

        This method browses the data directory and finds all valid files, that
        is, file that are named according to one of the aerocom file naming
        conventions. The file list is stored in :attr:`files`.

        Note
        ----
        It is presumed, that naming conventions of files in
        the data directory are not mixed but all correspond to either of the
        conventions defined in

        Parameters
        ----------
        update_file_convention : bool
            if True, the first file in `data_dir` is used to identify the
            file naming convention (cf. :class:`FileConventionRead`)

        Raises
        ------
        DataCoverageError
            if no valid files could be found
        """
        if self.data_dir is None:
            raise AttributeError("please set data_dir first")

        # get all files with correct ending
        files = glob(f"{self.data_dir}/*{self.file_type}")
        if len(files) == 0:
            logger.warning(
                f"No files of type {self.file_type} could be found in current "
                f"data directory (data_dir={os.path.abspath(self.data_dir)}"
            )
            return

        if update_file_convention:
            # Check if the found file has a naming according the aerocom conventions
            # and set the convention for all files (maybe this need to be
            # updated in case there can be more than one file naming convention
            # within one model directory)
            try:
                self._update_file_convention(files)
            except FileNotFoundError as e:
                logger.warning(repr(e))
                return

        result = self._evaluate_fileinfo(files)
        df = self._fileinfo_to_dataframe(result)
        self.file_info = df

        if len(df) == 0:
            raise DataCoverageError(f"No valid files could be found for {self.data_id}")

    def filter_files(
        self,
        var_name=None,
        ts_type=None,
        start=None,
        stop=None,
        experiment=None,
        vert_which=None,
        is_at_stations=False,
        df=None,
    ):
        """Filter file database

        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        ts_type : str
            string specifying temporal resolution (choose from
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised
            of the available resolutions is used
        start : Timestamp or str, optional
            start time of data import
        stop : Timestamp or str, optional
            stop time of data import
        experiment : str
            name of experiment (only relevant if this dataset contains more
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that
            match the query.

        """
        if df is None:
            df = self.file_info

        yrs = self._get_years_to_load(start, stop)
        year_cond = df.year.isin(yrs)

        if var_name is None:
            var_cond = df.var_name.isin(df.var_name.values)
        else:
            var_cond = df.var_name == var_name
        if vert_which is None:
            vert_cond = df.vert_code.isin(df.vert_code.values)
        else:
            vert_cond = df.vert_code == vert_which
        if ts_type is None:
            freq_cond = df.ts_type.isin(df.ts_type.values)
        else:
            freq_cond = df.ts_type == ts_type
        if experiment is None:
            exp_cond = df.experiment.isin(df.experiment.values)
        else:
            exp_cond = df.experiment == experiment

        return df.loc[
            (var_cond)
            & (year_cond)
            & (freq_cond)
            & (exp_cond)
            & (vert_cond)
            & (df.is_at_stations == is_at_stations)
        ]

    def _infer_ts_type(self, df, ts_type, flex_ts_type, prefer_longer):
        ts_types = df.ts_type.unique()

        if len(ts_types) == 1:
            # only one frequency available
            if flex_ts_type or ts_type is None or ts_types[0] == ts_type:
                # all good
                return ts_types[0]
            raise DataCoverageError(f"No files could be found for ts_type {ts_type}")
        highest_avail = get_highest_resolution(*ts_types)
        # there is more than one frequency available -> decision making
        # gets more complicated
        if not flex_ts_type:
            if ts_type is None:
                return highest_avail
            elif ts_type in ts_types:
                return ts_type
            raise DataCoverageError("Failed to infer ts_type")

        # ts_type is flexible
        if ts_type is None:
            # initiate with highest available
            ts_type = highest_avail

        if not prefer_longer:
            return ts_type

        # ts_type is flexible and user prefers the longer period over
        # higher resolution
        ts_type = ts_types[0]
        subset = self.filter_files(ts_type=ts_type, df=df)
        for _ts_type in ts_types[1:]:
            _subset = self.filter_files(ts_type=_ts_type, df=df)
            if len(_subset) > len(subset):
                subset = _subset
                ts_type = _ts_type
        return ts_type

    def filter_query(
        self,
        var_name,
        ts_type=None,
        start=None,
        stop=None,
        experiment=None,
        vert_which=None,
        is_at_stations=False,
        flex_ts_type=True,
        prefer_longer=False,
    ):
        """Filter files for read query based on input specs

        Parameters
        ----------

        Returns
        -------
        DataFrame
            dataframe containing filtered dataset
        """
        if var_name not in self.file_info.var_name.values:
            raise DataCoverageError(
                f"Variable {var_name} is not available in dataset {self.data_id}"
            )

        subset = self.filter_files(
            var_name=var_name,
            ts_type=None,  # disregard ts_type in 1. iteration
            start=start,
            stop=stop,
            experiment=experiment,
            vert_which=vert_which,
            is_at_stations=is_at_stations,
        )
        if len(subset) == 0:
            if vert_which in self.VERT_ALT:
                vc = self.VERT_ALT[vert_which]
                logger.warning(
                    f"No files could be found for var {var_name} and "
                    f"vert_which {vert_which} in {self.data_id}. "
                    f"Trying to find alternative options"
                )
                return self.filter_query(
                    var_name,
                    ts_type,
                    start,
                    stop,
                    experiment,
                    vert_which=vc,
                    is_at_stations=is_at_stations,
                    flex_ts_type=flex_ts_type,
                    prefer_longer=prefer_longer,
                )
            raise DataCoverageError("No files could be found")
        ts_type = self._infer_ts_type(subset, ts_type, flex_ts_type, prefer_longer)
        subset = self.filter_files(ts_type=ts_type, start=start, stop=stop, df=subset)
        if len(subset) == len(subset.year.unique()):
            return subset

        # File request could not be resolved such that every year only occurs
        # once
        msg = ""
        exps = subset.experiment.unique()
        verts = subset.vert_code.unique()

        if len(exps) > 1:
            msg += f"Found multiple experiments. Choose from: {exps}"
        if len(verts) > 1:
            dvc = const.VARS[var_name].get_default_vert_code()
            if dvc is not None and dvc in verts:
                return self.filter_query(
                    var_name,
                    ts_type,
                    start,
                    stop,
                    experiment,
                    vert_which=dvc,
                    is_at_stations=is_at_stations,
                    flex_ts_type=flex_ts_type,
                    prefer_longer=prefer_longer,
                )

            if msg:
                msg += "; "
            msg += f"Found multiple vertical codes. Choose from: {verts}"
        raise DataQueryError(
            f"Failed to uniquely identify data files for input query. Reason: {msg}"
        )

    def get_files(
        self,
        var_name,
        ts_type=None,
        start=None,
        stop=None,
        experiment=None,
        vert_which=None,
        is_at_stations=False,
        flex_ts_type=True,
        prefer_longer=False,
    ):
        """Get data files based on input specs"""
        subset = self.filter_query(
            var_name,
            ts_type,
            start,
            stop,
            experiment,
            vert_which,
            is_at_stations,
            flex_ts_type,
            prefer_longer,
        )

        return self._generate_file_paths(subset)

    def _generate_file_paths(self, df=None):
        if df is None:
            df = self.file_info
        return sorted(os.path.join(self.data_dir, x) for x in df.filename.values)

    def get_var_info_from_files(self) -> dict:
        """Creates dictionary that contains variable specific meta information

        Returns
        -------
        dict
            dictionary where keys are available variables and values (for each
            variable) contain information about available ts_types, years, etc.
        """
        result = {}
        for file in self.files:
            finfo = self.file_convention.get_info_from_file(file)
            var_name = finfo["var_name"]
            if var_name not in result:
                result[var_name] = var_info = {}
                for key in finfo:
                    if key != "var_name":
                        var_info[key] = []
            else:
                var_info = result[var_name]
            for key, val in finfo.items():
                if key == "var_name":
                    continue
                if val is not None and val not in var_info[key]:
                    var_info[key].append(val)
        # now check auxiliary variables
        for var_to_compute in self.AUX_REQUIRES:
            if var_to_compute in result:
                continue
            try:
                vars_to_read = self._get_aux_vars_and_fun(var_to_compute)[0]
            except VarNotAvailableError:
                pass
            except VariableDefinitionError:
                pass
            else:
                # init result info dict for aux variable
                result[var_to_compute] = var_info = {}
                first = result[vars_to_read[0]]
                # init with results from first required variable
                var_info.update(**first)
                if len(vars_to_read) > 1:
                    for info_other in vars_to_read[1:]:
                        other = result[info_other]
                        for key, info in var_info.items():
                            # compute match with other variable
                            var_info[key] = list(np.intersect1d(info, other[key]))
                var_info["aux_vars"] = vars_to_read

        return result

    def update(self, **kwargs):
        """Update one or more valid parameters

        Parameters
        ----------
        **kwargs
            keyword args that will be used to update (overwrite) valid class
            attributes such as `data, data_dir, files`
        """
        for k, v in kwargs.items():
            if k in self.__dict__:
                logger.info(
                    f"Updating {k} in ModelImportResult for model {self.data_id}. New value: {v}"
                )
                self.__dict__[k] = v
            else:
                logger.info(f"Ignoring key {k} in ModelImportResult.update()")

    def concatenate_cubes(self, cubes):
        """Concatenate list of cubes into one cube

        Parameters
        ----------
        CubeList
            list of individual cubes

        Returns
        -------
        Cube
            Single cube that contains concatenated cubes from input list

        Raises
        ------
        iris.exceptions.ConcatenateError
            if concatenation of all cubes failed
        """
        return concatenate_iris_cubes(cubes, error_on_mismatch=True)

    def compute_var(
        self,
        var_name,
        start=None,
        stop=None,
        ts_type=None,
        experiment=None,
        vert_which=None,
        flex_ts_type=True,
        prefer_longer=False,
        vars_to_read=None,
        aux_fun=None,
        try_convert_units=True,
        aux_add_args=None,
        rename_var=None,
        **kwargs,
    ):
        """Compute auxiliary variable

        Like :func:`read_var` but for auxiliary variables
        (cf. AUX_REQUIRES)

        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        start : Timestamp or str, optional
            start time of data import (if valid input, then the current
            :attr:`start` will be overwritten)
        stop : Timestamp or str, optional
            stop time of data import
        ts_type : str
            string specifying temporal resolution (choose from
            hourly, 3hourly, daily, monthly). If None, prioritised
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more
            than one experiment)
        vert_which : str
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel)
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that
            match the query.
        try_convert_units : bool
            if True, units of GriddedData objects are attempted to be converted
            to AeroCom default. This applies both to the GriddedData objects
            being read for computation as well as the variable computed from
            the forme objects. This is, for instance, useful when computing
            concentration in precipitation from wet deposition and precipitation
            amount.
        rename_var : str
            if this is set, the `var_name` attribute of the output
            `GriddedData` object will be updated accordingly.
        **kwargs
            additional keyword args passed to :func:`_load_var`

        Returns
        -------
        GriddedData
            loaded data object
        """
        if vars_to_read is not None:
            self.add_aux_compute(var_name, vars_to_read, aux_fun)
        vars_to_read, aux_fun = self._get_aux_vars_and_fun(var_name)
        if aux_add_args is None:
            aux_add_args = {}
        data = []
        # all variables that are required need to be in the same temporal
        # resolution
        try:
            ts_type = self.find_common_ts_type(
                vars_to_read,
                start,
                stop,
                ts_type,
                experiment,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
            )
        except DataCoverageError:
            if vert_which not in self.VERT_ALT:
                raise
            vert_which = self.VERT_ALT[vert_which]

            ts_type = self.find_common_ts_type(
                vars_to_read,
                start,
                stop,
                ts_type,
                experiment,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
            )
        for var in vars_to_read:
            aux_data = self._load_var(
                var_name=var,
                ts_type=ts_type,
                start=start,
                stop=stop,
                experiment=experiment,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
                prefer_longer=prefer_longer,
                try_convert_units=try_convert_units,
                rename_var=None,
                **kwargs,
            )
            data.append(aux_data)

        if var_name in self.AUX_ADD_ARGS:
            for key, val in self.AUX_ADD_ARGS[var_name].items():
                if key not in aux_add_args:
                    aux_add_args[key] = val

        if len(aux_add_args) > 0:
            cube = aux_fun(*data, **aux_add_args)
        else:
            cube = aux_fun(*data)

        cube.var_name = var_name

        data = GriddedData(
            cube,
            data_id=self.data_id,
            computed=True,
            convert_unit_on_init=try_convert_units,
            **kwargs,
        )

        data.reader = self
        if rename_var is not None:
            data.var_name = rename_var
        return data

    def find_common_ts_type(
        self,
        vars_to_read,
        start=None,
        stop=None,
        ts_type=None,
        experiment=None,
        vert_which=None,
        flex_ts_type=True,
    ):
        """Find common ts_type for list of variables to be read

        Parameters
        ----------
        vars_to_read : list
            list of variables that is supposed to be read
        start : Timestamp or str, optional
            start time of data import (if valid input, then the current
            start will be overwritten)
        stop : Timestamp or str, optional
            stop time of data import (if valid input, then the current
            :attr:`start` will be overwritten)
        ts_type : str
            string specifying temporal resolution (choose from
            hourly, 3hourly, daily, monthly). If None, prioritised
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more
            than one experiment)
        vert_which : str
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel)
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case
            the input ts_type is not available for this variable

        Returns
        -------
        str
            common ts_type for input variable

        Raises
        ------
        DataCoverageError
            if no match can be found
        """
        if isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]

        common = self.filter_files(
            var_name=vars_to_read[0],
            start=start,
            stop=stop,
            experiment=experiment,
            vert_which=vert_which,
        ).ts_type.unique()
        if len(common) == 0:
            raise DataCoverageError(
                f"Could not find any file matches for query and variable {vars_to_read[0]}"
            )
        for var in vars_to_read[1:]:
            _tt = self.filter_files(
                var_name=var, start=start, stop=stop, experiment=experiment, vert_which=vert_which
            )
            common = np.intersect1d(common, _tt.ts_type.unique())

        if len(common) == 0:
            raise DataCoverageError(f"Could not find common ts_type for variables {vars_to_read}")
        elif len(common) == 1:
            if ts_type is None or flex_ts_type:
                return common[0]
            elif ts_type == common[0]:
                return ts_type
            raise DataCoverageError(
                f"Could not find files with ts_type={ts_type} for all input variables: {vars_to_read}"
            )
        if ts_type is not None:
            if ts_type in common:
                return ts_type

        if not flex_ts_type:
            raise DataCoverageError(
                f"Could not find files with ts_type={ts_type} for "
                f"all input variables: {vars_to_read}"
            )

        # NOTE: Changed by jgliss on 7.11.2019 for more flexibility
        # common_sorted = [x for x in const.GRID_IO.TS_TYPES if x in common]
        common_sorted = sort_ts_types(common)
        return common_sorted[0]

    def add_aux_compute(self, var_name, vars_required, fun):
        """Register new variable to be computed

        Parameters
        ----------
        var_name : str
            variable name to be computed
        vars_required : list
            list of variables to read, that are required to compute `var_name`
        fun : callable
            function that takes a list of `GriddedData` objects as input and
            that are read using variable names specified by `vars_required`.
        """
        if isinstance(vars_required, str):
            vars_required = [vars_required]
        if not isinstance(vars_required, list):
            raise ValueError(
                f"Invalid input for vars_required. Need str or list. Got: {vars_required}"
            )
        elif not callable(fun):
            raise ValueError("Invalid input for fun. Input is not a callable object")
        self._aux_requires[var_name] = vars_required
        self._aux_funs[var_name] = fun
        if not self._check_aux_compute_access(var_name):
            raise DataCoverageError(
                f"Failed to confirm access to auxiliary variable {var_name} from {vars_required}"
            )

    @property
    def registered_var_patterns(self):
        """
        List of string patterns for computation of variables

        The information is extracted from :attr:`AUX_REQUIRES`

        Returns
        -------
        list
            list of variable patterns

        """
        return [x for x in self.AUX_REQUIRES if "*" in x]

    def _get_var_to_read(self, var_name: str) -> str:
        """
        Get variable to read

        The logical order of inferring the variable to read is:

            1. Check if input variable name as is, is available in filename
            2. If not, check if an old version of that name is available
            3. If not, check if an alias name of input name is available
            4. If not, check if input variable is an alias and if AeroCom \
                variable name is available instead (e.g. input od550csaer \
                not available, but od550aer is available)

        Parameters
        ----------
        var_name : str
            name of variable that is supposed to be read

        Raises
        ------
        VarNotAvailableError
            if no match can be found
        VariableDefinitionError
            if input variable is not defined

        Returns
        -------
        str
            name of variable match found
        """

        if var_name in self.vars_filename:
            return var_name

        # e.g. user asks for od550aer but files contain only 3d var od5503daer
        # if not var_to_read in self.vars_filename:
        for var in self._vars_3d:
            if Variable(var).var_name == var_name:
                return var

        # get instance of Variable class
        var = const.VARS[var_name]

        # If the input variable has aliases, check if one of these aliases is
        # provided in the dataset
        for alias in var.aliases:
            if alias in self.vars_filename:
                logger.info(f"Did not find {var_name} field but {alias}. Using the latter instead")
                return alias

        # Finally, if still no match could be found, check if input variable
        # is an alias and see if the corresponding AeroCom variable name is
        # available in dataset
        if var.is_alias and var.var_name_aerocom in self.vars_filename:
            return var.var_name_aerocom

        raise VarNotAvailableError(f"Variable {var_name} could not be found")

    def _eval_vert_which_and_ts_type(self, var_name, vert_which, ts_type):
        if all(x == "" for x in self.file_info.vert_code.values):
            logger.info(
                f"Deactivating file search by vertical code for {self.data_id}, "
                f"since filenames do not include information about vertical code "
                f"(probably AeroCom 2 convention)"
            )
            vert_which = None

        if isinstance(vert_which, dict):
            try:
                vert_which = vert_which[var_name]
            except Exception:
                logger.info(
                    f"Setting vert_which to None, since input dict {vert_which} "
                    f"does not contain input variable {var_name}"
                )
                vert_which = None

        if isinstance(ts_type, dict):
            try:
                ts_type = ts_type[var_name]
            except Exception:
                logger.info(
                    f"Setting ts_type to None, since input dict {ts_type} "
                    f"does not contain specification variable to read {var_name}"
                )
                ts_type = None
        return vert_which, ts_type

    # TODO: add from_vars input arg for computation and corresponding method
    def read_var(
        self,
        var_name,
        start=None,
        stop=None,
        ts_type=None,
        experiment=None,
        vert_which=None,
        flex_ts_type=True,
        prefer_longer=False,
        aux_vars=None,
        aux_fun=None,
        constraints=None,
        try_convert_units=True,
        rename_var=None,
        **kwargs,
    ):
        """Read model data for a specific variable

        This method searches all valid files for a given variable and for a
        provided temporal resolution (e.g. *daily, monthly*), optionally
        within a certain time window, that may be specified on class
        instantiation or using the corresponding input parameters provided in
        this method.

        The individual NetCDF files for a given temporal period are loaded as
        instances of the :class:`iris.Cube` object and appended to an instance
        of the :class:`iris.cube.CubeList` object. The latter is then used to
        concatenate the individual cubes in time into a single instance of the
        :class:`pyaerocom.GriddedData` class. In order to ensure that this
        works, several things need to be ensured, which are listed in the
        following and which may be controlled within the global settings for
        NetCDF import using the attribute :attr:`GRID_IO` (instance of
        :class:`OnLoad`) in the default instance of the
        :class:`pyaerocom.config.Config` object accessible via
        ``pyaerocom.const``.

        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        start : Timestamp or str, optional
            start time of data import
        stop : Timestamp or str, optional
            stop time of data import
        ts_type : str
            string specifying temporal resolution (choose from
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that
            match the query.
        aux_vars : list
            only relevant if `var_name` is not available for reading but needs
            to be computed: list of variables that are required to compute
            `var_name`
        aux_fun : callable
            only relevant if `var_name` is not available for reading but needs
            to be computed: custom method for computation (cf.
            :func:`add_aux_compute` for details)
        constraints : list, optional
            list of reading constraints (dict type). See
            :func:`check_constraint_valid` and :func:`apply_read_constraint`
            for details related to format of the individual constraints.
        try_convert_units : bool
            if True, then the unit of the variable data is checked against
            AeroCom default unit for that variable and if it deviates, it is
            attempted to be converted to the AeroCom default unit. Default is
            True.
        rename_var : str
            if this is set, the `var_name` attribute of the output
            `GriddedData` object will be updated accordingly.
        **kwargs
            additional keyword args parsed to :func:`_load_var`

        Returns
        -------
        GriddedData
            loaded data object

        Raises
        ------
        AttributeError
            if none of the ts_types identified from file names is valid
        VarNotAvailableError
            if specified ts_type is not supported
        """
        # user has provided input that specified how the input variable
        # is supposed to be computed. In this case, the variable will be
        # computed even if it is directly available in a file, i.e. it
        # could be read.
        if aux_vars is not None:
            self.add_aux_compute(var_name, aux_vars, aux_fun)

        vert_which, ts_type = self._eval_vert_which_and_ts_type(var_name, vert_which, ts_type)
        data = self._try_read_var(
            var_name,
            start,
            stop,
            ts_type,
            experiment,
            vert_which,
            flex_ts_type,
            prefer_longer,
            try_convert_units=try_convert_units,
            rename_var=rename_var,
            **kwargs,
        )

        if constraints is not None:
            if isinstance(constraints, dict):
                constraints = [constraints]
            for constraint in constraints:
                data = self.apply_read_constraint(
                    data,
                    constraint,
                    start=start,
                    stop=stop,
                    ts_type=ts_type,
                    experiment=experiment,
                    vert_which=vert_which,
                    flex_ts_type=flex_ts_type,
                    prefer_longer=prefer_longer,
                    **kwargs,
                )
        return data

    def check_constraint_valid(self, constraint):
        """
        Check if reading constraint is valid

        Parameters
        ----------
        constraint : dict
            reading constraint. Requires at lest entries for following keys:
            - operator (str): for valid operators see :attr:`CONSTRAINT_OPERATORS`
            - filter_val (float): value against which data is evaluated wrt to \
                operator

        Raises
        ------
        ValueError
            If constraint is invalid

        Returns
        -------
        None.

        """
        if not isinstance(constraint, dict):
            raise ValueError("Read constraint needs to be dict")
        elif "operator" not in constraint:
            raise ValueError(
                f"Constraint requires specification of operator. "
                f"Valid operators: {self.CONSTRAINT_OPERATORS}"
            )
        elif constraint["operator"] not in self.CONSTRAINT_OPERATORS:
            raise ValueError(
                f"Invalid constraint operator. Choose from: {self.CONSTRAINT_OPERATORS}"
            )
        elif "filter_val" not in constraint:
            raise ValueError("constraint needs specification of filter_val")
        elif not isnumeric(constraint["filter_val"]):
            raise ValueError("Need numerical filter value")

    def apply_read_constraint(self, data, constraint, **kwargs):
        """
        Filter a `GriddeData` object by value in another variable

        Note
        ----
        BETA version, that was hacked down in a rush to be able to apply
        AOD>0.1 threshold when reading AE.


        Parameters
        ----------
        data : GriddedData
            data object to which constraint is applied
        constraint : dict
            dictionary defining read constraint (see
            :func:`check_constraint_valid` for minimum requirement). If
            constraint contains key var_name (not mandatory), then the
            corresponding variable is attempted to be read and is used to
            evaluate constraint and the corresponding boolean mask is then
            applied to input `data`. Wherever this mask is True (i.e. constraint
            is met), the current value in input `data` will be replaced with
            `numpy.ma.masked` or, if specified, with entry `new_val` in input
            constraint dict.
        **kwargs : TYPE
            reading arguments in case additional variable data needs to be
            loaded, to determine filter mask (i.e. if `var_name` is specified
            in input constraint). Parse to :func:`read_var`.

        Raises
        ------
        ValueError
            If constraint is invalid (cf. :func:`check_constraint_valid` for
            details).

        Returns
        -------
        GriddedData
            modified data objects (all grid-points that met constraint
            are replaced with either `numpy.ma.masked` or with a
            value that can be specified via key `new_val` in input constraint).

        """
        self.check_constraint_valid(constraint)
        if "new_val" in constraint:
            new_val = constraint["new_val"]
        else:
            new_val = np.nan

        operator_fun = self.CONSTRAINT_OPERATORS[constraint["operator"]]

        if "var_name" in constraint:
            other_data = self.read_var(constraint["var_name"], **kwargs)
        else:
            other_data = data

        if not other_data.shape == data.shape:
            raise ValueError("Failed to apply filter. Shape mismatch")

        other_arr = other_data.to_xarray()
        arr = data.to_xarray()
        if not other_arr.dims == arr.dims:
            from pyaerocom.exceptions import DataDimensionError

            raise DataDimensionError("Mismatch in dimensions")
        for dim in arr.dims:
            same_vals = (arr[dim].values == other_arr[dim].values).all()
            if not same_vals:
                if dim == "time":
                    other_arr[dim] = arr[dim]
                else:
                    raise ValueError()

        # select all grid points where conition is fulfilled
        mask = operator_fun(other_arr, constraint["filter_val"])

        # set values to new_val where condition is fulfilled
        filtered = xr.where(mask, new_val, arr)

        # overwrite data in cube with the filtered data
        outcube = filtered.to_iris()
        outcube.var_name = data.var_name
        outcube.units = data.units
        outcube.attributes = data.cube.attributes
        outcube_dims = outcube.dim_coords
        for i, name in enumerate(data.dimcoord_names):
            _name = outcube_dims[i].name()
            outcube.remove_coord(_name)
            outcube.add_dim_coord(data.cube.coord(name), i)
        data.cube = outcube
        return data

    def _try_read_var(
        self,
        var_name,
        start,
        stop,
        ts_type,
        experiment,
        vert_which,
        flex_ts_type,
        prefer_longer,
        try_convert_units,
        rename_var,
        **kwargs,
    ):
        """Helper method used in :func:`read_var`

        See :func:`read_var` for description of input arguments.
        """
        if var_name in self._aux_requires and self.check_compute_var(var_name):
            return self.compute_var(
                var_name=var_name,
                start=start,
                stop=stop,
                ts_type=ts_type,
                experiment=experiment,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
                prefer_longer=prefer_longer,
                try_convert_units=try_convert_units,
                rename_var=rename_var,
                **kwargs,
            )

        try:
            var_to_read = self._get_var_to_read(var_name)
            return self._load_var(
                var_name=var_to_read,
                ts_type=ts_type,
                start=start,
                stop=stop,
                experiment=experiment,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
                prefer_longer=prefer_longer,
                try_convert_units=try_convert_units,
                rename_var=rename_var,
                **kwargs,
            )

        except VarNotAvailableError:
            if self.check_compute_var(var_name):
                return self.compute_var(
                    var_name=var_name,
                    start=start,
                    stop=stop,
                    ts_type=ts_type,
                    experiment=experiment,
                    vert_which=vert_which,
                    flex_ts_type=flex_ts_type,
                    prefer_longer=prefer_longer,
                    try_convert_units=try_convert_units,
                    rename_var=rename_var,
                    **kwargs,
                )
        # this input variable was explicitly set to be computed, in which
        # case reading of that variable is ignored even if a file exists for
        # that
        raise VarNotAvailableError(
            f"Error: variable {var_name} not available in files and can also not be computed."
        )

    def read(
        self,
        vars_to_retrieve=None,
        start=None,
        stop=None,
        ts_type=None,
        experiment=None,
        vert_which=None,
        flex_ts_type=True,
        prefer_longer=False,
        require_all_vars_avail=False,
        **kwargs,
    ):
        """Read all variables that could be found

        Reads all variables that are available (i.e. in :attr:`vars_filename`)

        Parameters
        ----------
        vars_to_retrieve : list or str, optional
            variables that are supposed to be read. If None, all variables
            that are available are read.
        start : Timestamp or str, optional
            start time of data import
        stop : Timestamp or str, optional
            stop time of data import
        ts_type : str, optional
            string specifying temporal resolution (choose from
            "hourly", "3hourly", "daily", "monthly"). If None, prioritised
            of the available resolutions is used
        experiment : str
            name of experiment (only relevant if this dataset contains more
            than one experiment)
        vert_which : str or dict, optional
            valid AeroCom vertical info string encoded in name (e.g. Column,
            ModelLevel) or dictionary containing var_name as key and vertical
            coded string as value, accordingly
        flex_ts_type : bool
            if True and if applicable, then another ts_type is used in case
            the input ts_type is not available for this variable
        prefer_longer : bool
            if True and applicable, the ts_type resulting in the longer time
            coverage will be preferred over other possible frequencies that
            match the query.
        require_all_vars_avail : bool
            if True, it is strictly required that all input variables are
            available.
        **kwargs
            optional and support for deprecated input args

        Returns
        -------
        tuple
            loaded data objects (type :class:`GriddedData`)

        Raises
        ------
        IOError
            if input variable names is not list or string
        VarNotAvailableError
            1. if ``require_all_vars_avail=True`` and one or more of the
            desired variables is not available in this class
            2. if ``require_all_vars_avail=True`` and if none of the input
            variables is available in this object
        """
        if vars_to_retrieve is None and "var_names" in kwargs:
            warnings.warn(
                "Input arg var_names is deprecated. Please use vars_to_retrieve instead",
                DeprecationWarning,
                stacklevel=2,
            )
            vars_to_retrieve = kwargs["var_names"]
        if vars_to_retrieve is None:
            vars_to_retrieve = self.vars_filename
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        elif not isinstance(vars_to_retrieve, list):
            raise OSError(
                f"Invalid input for vars_to_retrieve {vars_to_retrieve}. "
                f"Need string or list of strings specifying var_names to load. "
                f"You may also leave it empty (None) in which case all "
                f"available variables are loaded"
            )
        if require_all_vars_avail:
            if not all([var in self.vars_provided for var in vars_to_retrieve]):
                raise VarNotAvailableError(
                    f"One or more of the specified vars ({vars_to_retrieve}) "
                    f"is not available in {self.data_id} database. "
                    f"Available vars: {self.vars_provided}"
                )
        var_names = list(np.intersect1d(self.vars_provided, vars_to_retrieve))
        if len(var_names) == 0:
            raise VarNotAvailableError(
                f"None of the desired variables is available in {self.data_id}"
            )
        data = []
        for var in var_names:
            try:
                data.append(
                    self.read_var(
                        var_name=var,
                        start=start,
                        stop=stop,
                        ts_type=ts_type,
                        experiment=experiment,
                        vert_which=vert_which,
                        flex_ts_type=flex_ts_type,
                        prefer_longer=prefer_longer,
                    )
                )
            except (VarNotAvailableError, DataCoverageError) as e:
                logger.warning(repr(e))
        return tuple(data)

    def _load_files(self, files, var_name, perform_fmt_checks=None):
        """Load list of files containing variable to read into Cube instances

        Parameters
        ----------
        files : list
            list of netcdf file
        var_name : str
            name of variable to read
        perform_fmt_checks : bool
            if True, the loaded data is checked for consistency with
            AeroCom default requirements.

        Returns
        -------
        CubeList
            list of loaded Cube instances
        list
            list containing corresponding filenames of loaded cubes
        """
        cubes, loaded_files = load_cubes_custom(
            files=files,
            var_name=var_name,
            file_convention=self.file_convention,
            perform_fmt_checks=perform_fmt_checks,
        )

        if len(loaded_files) == 0:
            raise OSError(f"None of the input files could be loaded in {self.data_id}")

        # self.loaded_cubes[var_name] = cubes
        return (cubes, loaded_files)

    def _get_meta_df(self, subset):
        """Extract relevant meta information from file_info dataframe

        Parameters
        ----------
        subset : pd.DataFrame
            subset of, or :attr:`file_info`

        Raises
        ------
        DataQueryError
            if more than one time frequency is available in the dataframe

        Returns
        -------

        """
        meta = {}
        # check additional metadata
        ts_types = subset.ts_type.unique()

        # sanity check
        if len(ts_types) > 1:
            raise DataQueryError("Fatal: subset contains more than one ts_type")
        meta["ts_type"] = ts_types[0]

        mets = subset.meteo.unique()
        meta["meteo"] = mets[0] if len(mets) == 1 else list(mets)

        exps = subset.experiment.unique()
        meta["experiment"] = exps[0] if len(exps) == 1 else list(exps)

        perts = subset.perturbation.unique()
        meta["perturbation"] = perts[0] if len(perts) == 1 else list(perts)

        vertcodes = subset.vert_code.unique()
        meta["vert_code"] = vertcodes[0] if len(vertcodes) == 1 else list(vertcodes)

        return meta

    def _load_var(
        self,
        var_name,
        ts_type,
        start,
        stop,
        experiment,
        vert_which,
        flex_ts_type,
        prefer_longer,
        try_convert_units,
        rename_var,
        **kwargs,
    ):
        """Find files corresponding to input specs and load into GriddedData

        Note
        ----
        See :func:`read_var` for I/O info.
        """
        if self.ignore_vert_code:
            vert_which = None
        subset = self.filter_query(
            var_name,
            ts_type,
            start,
            stop,
            experiment,
            vert_which,
            is_at_stations=False,
            flex_ts_type=flex_ts_type,
            prefer_longer=prefer_longer,
        )
        if len(subset) == 0:
            raise DataQueryError("Could not find file match for query")

        match_files = self._generate_file_paths(subset)
        (cube_list, from_files) = self._load_files(match_files, var_name, **kwargs)
        is_concat = False
        if len(cube_list) > 1:
            try:
                cube = self.concatenate_cubes(cube_list)
                is_concat = True
            except iris.exceptions.ConcatenateError as e:
                raise NotImplementedError(
                    f"Failed to concatenate cubes: {cube_list}\nError: {repr(e)}"
                )
        else:
            cube = cube_list[0]

        meta = self._get_meta_df(subset)
        data = GriddedData(
            input=cube,
            from_files=from_files,
            data_id=self.data_id,
            concatenated=is_concat,
            convert_unit_on_init=try_convert_units,
            **meta,
        )
        # crop cube in time (if applicable)
        if isinstance(start, int) and start != 9999:
            try:
                data = self._check_crop_time(data, start, stop)
            except Exception:
                logger.exception(
                    f"Failed to crop time dimension in {data} (start: {start}, stop: {stop})"
                )
        if rename_var is not None:
            data.var_name = rename_var
        data.reader = self
        return data

    def _check_crop_time(self, data, start, stop):
        crop_time = False
        crop_time_range = [self.start, self.stop]
        if start is not None:
            crop_time = True
            crop_time_range[0] = to_pandas_timestamp(start)
        if stop is not None:
            crop_time = True
            crop_time_range[1] = to_pandas_timestamp(stop)
        if crop_time:
            logger.info("Applying temporal cropping of result cube")
            data = data.crop(time_range=crop_time_range)
        return data

    def _check_ts_type(self, ts_type):
        """Check and, if applicable, update ts_type

        Returns
        -------
        str
            valid ts_type

        Raises
        ------
        ValueError

        """
        if ts_type is None:
            if len(self.ts_types) == 0:
                raise AttributeError(
                    "Apparently no files with a valid ts_type "
                    "entry in their filename could be found"
                )

            ts_type = self.ts_types[0]
        if not TsType.valid(ts_type):
            raise ValueError(f"Invalid input for ts_type: {ts_type}")
        return ts_type

    def __getitem__(self, var_name):
        """Try access import result for one of the models

        Parameters
        ----------
        var_name : str
            string specifying variable that is supposed to be extracted

        Returns
        -------
        GriddedData
            the corresponding read class for this model

        Raises
        -------
        ValueError
            if results for ``var_name`` are not available
        """
        if var_name not in self.data:
            return self.read_var(var_name)
        # return self.data[var_name]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        head = f"Pyaerocom {type(self).__name__}"
        s = (
            f"\n{head}\n{len(head) * '-'}\n"
            f"Data ID: {self.data_id}\n"
            f"Data directory: {self.data_dir}\n"
            f"Available experiments: {self.experiments}\n"
            f"Available years: {self.years_avail}\n"
            f"Available frequencies {self.ts_types}\n"
            f"Available variables: {self.vars_provided}\n"
        )
        return s.rstrip()

    ### DEPRECATED STUFF
    @property
    def name(self):
        """Deprecated name of attribute data_id"""
        warnings.warn("Please use data_id", DeprecationWarning, stacklevel=2)
        return self.data_id


def is_3d(var_name: str) -> bool:
    return "3d" in var_name.lower()
