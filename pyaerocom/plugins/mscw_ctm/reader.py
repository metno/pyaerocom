import glob
import logging
import os
import re
import warnings

import numpy as np
import xarray as xr

from pyaerocom import const
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.griddeddata import GriddedData
from pyaerocom.units_helpers import UALIASES

from .additional_variables import (
    add_dataarrays,
    calc_concNhno3,
    calc_concNnh3,
    calc_concNnh4,
    calc_concNno,
    calc_concNno2,
    calc_concNno3pm10,
    calc_concNno3pm25,
    calc_concno3pm10,
    calc_concno3pm25,
    calc_concNtnh,
    calc_concso4t,
    calc_concSso2,
    calc_concsspm25,
    calc_conNtnh_emep,
    calc_conNtno3,
    calc_conNtno3_emep,
    calc_vmrno2,
    calc_vmro3,
    calc_vmrox,
    calc_vmrox_from_conc,
    identity,
    subtract_dataarrays,
    update_EC_units,
)
from .model_variables import emep_variables

logger = logging.getLogger(__name__)


class ReadMscwCtm:
    """
    Class for reading model output from the EMEP MSC-W chemical transport model.

    Parameters
    ----------
    filepath : str
        Path to netcdf file.
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    data_dir : str, optional
        Base directory of EMEP data, containing one or more netcdf files

    Attributes
    ----------
    data_id : str
        ID of model
    filename : str
        name of data file to be read.
    """

    # dictionary containing information about additionally required variables
    # for each auxiliary variable (i.e. each variable that is not provided
    # by the original data but computed on import)
    AUX_REQUIRES = {
        "depso4": ["dryso4", "wetso4"],
        "depoxs": ["dryoxs", "wetoxs"],
        "depoxn": ["dryoxn", "wetoxn"],
        "deprdn": ["dryrdn", "wetrdn"],
        "concbc": ["concbcf", "concbcc"],
        "concno3": ["concno3c", "concno3f"],
        "concoa": ["concoac", "concoaf"],
        "concpmgt25": ["concpm10", "concpm25"],
        "concNhno3": ["conchno3"],
        "concNnh3": ["concnh3"],
        "concNnh4": ["concnh4"],
        "concNno3pm10": ["concno3f", "concno3c"],
        "concNno3pm25": ["concno3f", "concno3c"],
        "concno3pm10": ["concno3f", "concno3c"],
        "concno3pm25": ["concno3f", "concno3c"],
        "concsspm25": ["concssf", "concssc"],
        "concsspm10": ["concssf", "concssc"],
        # "vmrox": ["concno2", "vmro3"],
        "vmrox": ["concno2", "conco3"],
        "vmrno2": ["concno2"],
        "concNtno3": ["concoxn"],
        "concNtnh": ["concrdn"],
        # "concNtno3": ["conchno3", "concno3f", "concno3c"],
        # "concNtnh": ["concnh3", "concnh4"],
        "concecpm25": ["concecFine"],
        "concecpm10": ["concecFine", "concecCoarse"],
        "concCecpm10": ["concecpm10"],
        "concCecpm25": ["concecpm25"],
        "concCocpm25": ["concCocFine"],
        "concCocpm10": ["concCocFine", "concCocCoarse"],
        "concso4t": ["concso4", "concss"],
        "concNno": ["concno"],
        "concNno2": ["concno2"],
        "concSso2": ["concso2"],
        "vmro3": ["conco3"],
    }

    # Functions that are used to compute additional variables (i.e. one
    # for each variable defined in AUX_REQUIRES)
    # NOTE: these methods are supposed to work for xarray.DataArray instances
    # not iris.cube.Cube instance
    AUX_FUNS = {
        "depso4": add_dataarrays,
        "depoxs": add_dataarrays,
        "depoxn": add_dataarrays,
        "deprdn": add_dataarrays,
        "concbc": add_dataarrays,
        "concno3": add_dataarrays,
        "concoa": add_dataarrays,
        "concpmgt25": subtract_dataarrays,
        "concNhno3": calc_concNhno3,
        "concNnh3": calc_concNnh3,
        "concNnh4": calc_concNnh4,
        "concNno3pm10": calc_concNno3pm10,
        "concNno3pm25": calc_concNno3pm25,
        "concno3pm10": calc_concno3pm10,
        "concno3pm25": calc_concno3pm25,
        "concsspm25": calc_concsspm25,
        "concsspm10": add_dataarrays,
        # "vmrox": calc_vmrox,
        "vmrox": calc_vmrox_from_conc,
        "vmrno2": calc_vmrno2,
        "concNtno3": calc_conNtno3_emep,
        "concNtnh": calc_conNtnh_emep,
        # "concNtno3": calc_conNtno3,
        # "concNtnh": calc_concNtnh,
        "concecpm25": identity,
        "concecpm10": add_dataarrays,
        "concCecpm25": update_EC_units,
        "concCecpm10": update_EC_units,
        "concCocpm25": identity,
        "concCocpm10": add_dataarrays,
        "concso4t": calc_concso4t,
        "concNno": calc_concNno,
        "concNno2": calc_concNno2,
        "concSso2": calc_concSso2,
        "vmro3": calc_vmro3,
    }

    #: supported filename masks, placeholder is for frequencies
    FILE_MASKS = ["Base_*.nc"]

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

    DEFAULT_FILE_NAME = "Base_day.nc"

    def __init__(self, data_id=None, data_dir=None):
        self._data_dir = None
        # opened dataset (for performance boost), will be reset if data_dir is
        # changed
        self._filename = None
        self._filedata = None
        self._filepaths = None
        self._filepath = None

        self._file_mask = self.FILE_MASKS[0]
        self._files = None

        self.var_map = emep_variables()

        if data_dir is not None:
            if not isinstance(data_dir, str) or not os.path.exists(data_dir):
                raise FileNotFoundError(f"{data_dir}")

            self.data_dir = data_dir

        self.data_id = data_id

        self.filename = self.DEFAULT_FILE_NAME

    def search_all_files(self):
        namelist = self._get_namelist_from_folder()
        self.filepaths = self._get_files_from_namelist(namelist)

    def _get_files_from_namelist(self, namelist):
        files = []
        for d in namelist:
            mask, f = self._check_files_in_data_dir(d)
            files += f

        return files

    def _get_namelist_from_folder(self):
        """
        Finds all the subfolders where a emep file for one year might be.

        Note
        -------
        Checks only current level for folders. Should be able
        to search deeper.

        The only qualification of being a valid subfolder is whether or not
        the subfolder has contains a number >= 2000. There are no check if there
        are any emep files in the folder

        Returns
        -------
        List
         List of the names of the subfolder

        """
        dd = self.data_dir

        dirs = glob.glob(dd + "/*/")
        namelist = []
        yrs = []

        for d in dirs:
            if re.match(r".*20\d\d.*", d) is None:
                continue
            yrs.append(d.split("/")[-1])

            namelist.append(d)

        if len(namelist) == 0:
            namelist = [dd]
        else:
            namelist = [d for _, d in sorted(zip(yrs, namelist))]
        return list(set(namelist))

    def _get_yrs_from_filepaths(self):
        fps = self.filepaths
        yrs = []
        for fp in fps:
            try:
                yr = re.search(r".*(20\d\d).*", fp).group(1)
            except:  # pragma: no cover
                raise ValueError(f"Could not find any year in {fp}")

            yrs.append(yr)

        return sorted(list(set(yrs)))

    def _get_tst_from_file(self, file):
        # tst = re.search("Base_(.*).nc", file).group(1)
        mask = self._file_mask.replace("*", "(.*)")
        tst = re.search(mask, file).group(1)

        if "LF_" in tst:
            return None

        if tst not in list(self.FREQ_CODES):
            raise ValueError(f"The ts_type {tst} is not supported")

        return self.FREQ_CODES[tst]

    def _clean_filepaths(self, filepaths, yrs, ts_type):
        clean_paths = []
        found_yrs = []

        yrs = [int(yr) for yr in yrs]
        for path in filepaths:
            ddir, file = os.path.split(path)

            if self._get_tst_from_file(file) != ts_type:
                continue

            yrs_dir = ddir.split(os.sep)[-1]
            try:
                yr = re.search(r".*(20\d\d).*", yrs_dir).group(1)
            except:  # pragma: no cover
                raise ValueError(f"Could not find any year in {yrs_dir}")

            if int(yr) not in yrs:
                raise ValueError(f"The year {yr} is not in {yrs}")

            if int(yr) in found_yrs:
                raise ValueError(f"The year {yr} is already found: {found_yrs}")

            found_yrs.append(int(yr))

            clean_paths.append(path)

        if len(found_yrs) != len(yrs):
            raise ValueError(
                f"A different amount of years {found_yrs} were found compared tp {yrs}"
            )

        return [d for _, d in sorted(zip(found_yrs, clean_paths))]

    @property
    def data_dir(self):
        """
        Directory containing netcdf files
        """
        if self._data_dir is None:
            raise AttributeError(f"data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
        self._file_mask = self.FILE_MASKS[0]
        self._data_dir = val
        self._filedata = None
        self.search_all_files()
        self._files = self.filepaths

    @property
    def filename(self):
        """
        Name of netcdf file
        """
        return self._filename

    @filename.setter
    def filename(self, val):
        """
        Name of netcdf file
        """
        if not isinstance(val, str):  # pragma: no cover
            raise ValueError("needs str")
        elif val == self._filename:
            return
        self._filename = val
        self._filedata = None

    @property
    def filepath(self):
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # pragma: no cover
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        if not isinstance(value, str):
            raise TypeError("needs to be a string")

        self._filepath = value
        ddir, fname = os.path.split(value)
        self.data_dir = ddir
        self.filename = fname

    @property
    def filepaths(self):
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # pragma: no cover
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        return self._filepaths

    @filepaths.setter
    def filepaths(self, value):
        if not isinstance(value, list):  # pragma: no cover
            raise ValueError("needs to be list of strings")
        self._filepaths = value

    @property
    def filedata(self):
        """
        Loaded netcdf file (:class:`xarray.Dataset`)
        """
        if self._filedata is None:
            self.open_file()
        return self._filedata

    def _check_files_in_data_dir(self, data_dir):
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
        str
            file mask used (is identified automatically based on
            :attr:`FILE_MASKS`)
        list
            list of file matches

        """

        for fmask in self.FILE_MASKS:
            matches = glob.glob(f"{data_dir}/{fmask}")
            if len(matches) > 0:
                return fmask, matches
        raise FileNotFoundError(
            f"No valid model files could be found in {data_dir} for any of the "
            f"supported file masks: {self.FILE_MASKS}"
        )

    @property
    def ts_type(self):
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
        return self.ts_type_from_filename(self.filename)

    @property
    def ts_types(self):
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
        if not isinstance(self._files, list):
            raise AttributeError("please set data_dir first")
        tsts = []
        for file in self._files:
            tsts.append(self.ts_type_from_filename(file))
        return list(set(tsts))

    @property
    def years_avail(self):
        """
        Years available in loaded dataset
        """
        data = self.filepaths
        years = self._get_yrs_from_filepaths()

        years = list(np.unique(years))
        return sorted(years)

    @property
    def vars_provided(self):
        """Variables provided by this dataset"""
        return list(self.var_map) + list(self.AUX_REQUIRES)

    def open_file(self):
        """
        Open current netcdf file

        Returns
        -------
        dict(xarray.Dataset)
            Dict with years as keys and Datasets as items

        """
        fps = self.filepaths
        ds = {}

        yrs = self._get_yrs_from_filepaths()

        ts_type = self.ts_type_from_filename(self.filename)
        fps = self._clean_filepaths(fps, yrs, ts_type)
        if len(fps) > 1 and ts_type == "hourly":
            raise ValueError(f"ts_type {ts_type} can not be hourly when using multiple years")
        logger.info(f"Opening {fps}")
        ds = xr.open_mfdataset(fps)

        self._filedata = ds

        return ds

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "ReadMscwCtm"

    def has_var(self, var_name):
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

    def ts_type_from_filename(self, filename):
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

    def filename_from_ts_type(self, ts_type):
        """
        Infer file name of data based on input ts_type

        Parameters
        ----------
        ts_type : str
            desired time freq of data

        Raises
        ------
        ValueError
            If no file could be inferred.

        Returns
        -------
        fname : str
            Name of data file inferred based on current file mask and input
            freq.

        """
        mask = self._file_mask
        for substr, tst in self.FREQ_CODES.items():
            if tst == ts_type:
                fname = mask.replace("*", substr)
                return fname
        raise ValueError(f"failed to infer filename from input ts_type={ts_type}")

    def _compute_var(self, var_name_aerocom, ts_type):
        """Compute auxiliary variable

        Like :func:`read_var` but for auxiliary variables
        (cf. AUX_REQUIRES)

        Parameters
        ----------
        var_name : str
            variable that are supposed to be read
        ts_type : str
            string specifying temporal resolution.

        Returns
        -------
        GriddedData
            loaded data object
        """

        temp_arrs = []
        req = self.AUX_REQUIRES[var_name_aerocom]
        aux_func = self.AUX_FUNS[var_name_aerocom]
        logger.info(f"computing {var_name_aerocom} from {req} using {aux_func}")
        for aux_var in self.AUX_REQUIRES[var_name_aerocom]:
            arr = self._load_var(aux_var, ts_type)
            temp_arrs.append(arr)

        return aux_func(*temp_arrs)

    def _load_var(self, var_name_aerocom, ts_type):
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

        """
        if var_name_aerocom in self.var_map:  # can be read
            return self._read_var_from_file(var_name_aerocom, ts_type)
        elif var_name_aerocom in self.AUX_REQUIRES:
            return self._compute_var(var_name_aerocom, ts_type)
        raise VarNotAvailableError(
            f"Variable {var_name_aerocom} is not supported"
        )  # pragma: no cover

    def read_var(self, var_name, ts_type=None, **kwargs):
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

        if self.data_dir is None:  # pragma: no cover
            raise ValueError("data_dir must be set before reading.")
        elif self.filename is None and ts_type is None:  # pragma: no cover
            raise ValueError("please specify ts_type")
        elif ts_type is not None:
            # filename and ts_type are set. update filename if ts_type suggests
            # that current file has different resolution
            self.filename = self.filename_from_ts_type(ts_type)

        ts_type = self.ts_type

        arr = self._load_var(var_name_aerocom, ts_type)
        if arr.units in UALIASES:
            arr.attrs["units"] = UALIASES[arr.units]
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
        )

        #!obsolete
        # if var.is_deposition:
        #    implicit_to_explicit_rates(gridded, ts_type)

        # At this point a GriddedData object with name gridded should exist

        gridded.metadata["data_id"] = self.data_id
        gridded.metadata["from_files"] = self.filepaths

        # Remove unneccessary metadata. Better way to do this?
        for metadata in ["current_date_first", "current_date_last"]:
            if metadata in gridded.metadata.keys():
                del gridded.metadata[metadata]
        return gridded

    def _read_var_from_file(self, var_name_aerocom, ts_type):
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

        """
        emep_var = self.var_map[var_name_aerocom]

        try:
            filedata = self.filedata
            data = filedata[emep_var]

        except KeyError:
            raise VarNotAvailableError(
                f"{var_name_aerocom} ({emep_var}) not available in {self.filename}"
            )
        data.attrs["long_name"] = var_name_aerocom
        data.time.attrs["long_name"] = "time"
        data.time.attrs["standard_name"] = "time"
        prefix = emep_var.split("_")[0]
        data.attrs["units"] = self.preprocess_units(data.units, prefix)
        return data

    @staticmethod
    def preprocess_units(units, prefix):
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


class ReadEMEP(ReadMscwCtm):
    """Old name of :class:`ReadMscwCtm`."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "You are using a deprecated name ReadEMEP for class ReadMscwCtm, "
            "please use ReadMscwCtm instead",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
