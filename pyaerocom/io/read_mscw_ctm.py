#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:20:04 2020

@author: eirikg
"""

import xarray as xr
import numpy as np
import os
import glob

from pyaerocom import const
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.variable import get_emep_variables
from pyaerocom.griddeddata import GriddedData
from pyaerocom.units_helpers import implicit_to_explicit_rates

def add_dataarrays(*arrs):
    """
    Add a bunch of :class:`xarray.DataArray` instances

    Parameters
    ----------
    *arrs
        input arrays (instances of :class:`xarray.DataArray` with same shape)

    Returns
    -------
    xarray.DataArray
        Added array

    """
    if not len(arrs) > 1:
        raise ValueError('Need at least 2 input arrays to add')
    result = arrs[0]
    for arr in arrs[1:]:
        result += arr
    return result

def subtract_dataarrays(*arrs):
    """
    Subtract a bunch of :class:`xarray.DataArray` instances from an array

    Parameters
    ----------
    *arrs
        input arrays (instances of :class:`xarray.DataArray` with same shape).
        Subtraction is performed with respect to the first input array.


    Returns
    -------
    xarray.DataArray
        Diff array (all additional ones are subtracted from first array)

    """
    if not len(arrs) > 1:
        raise ValueError('Need at least 2 input arrays to add')
    result = arrs[0]
    for arr in arrs[1:]:
        result -= arr
    return result

class ReadMscwCtm(object):
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
    AUX_REQUIRES = {'depso4' : ['dryso4','wetso4'],
                    'concbc' : ['concbcf', 'concbcc'],
                    'concno3' : ['concno3c', 'concno3f'],
                    'concoa' : ['concoac', 'concoaf'],
                    'concpmgt25': ['concpm10', 'concpm25']}

    # Functions that are used to compute additional variables (i.e. one
    # for each variable defined in AUX_REQUIRES)
    # NOTE: these methods are supposed to work for xarray.DataArray instances
    # not iris.cube.Cube instance
    AUX_FUNS = {'depso4' : add_dataarrays,
                'concbc' : add_dataarrays,
                'concno3' : add_dataarrays,
                'conctno3' : add_dataarrays,
                'concoa' : add_dataarrays,
                'concpmgt25': subtract_dataarrays,
                }

    #: supported filename masks, placeholder is for frequencies
    FILE_MASKS = ['Base_*.nc']

    #: frequencies encoded in filenames
    FREQ_CODES = {
        'hour'    : 'hourly',
        'day'     : 'daily',
        'month'   : 'monthly',
        'fullrun' : 'yearly',

    }

    DEFAULT_FILE_NAME = 'Base_day.nc'

    def __init__(self, filepath=None, data_id=None, data_dir=None):
        self._data_dir = None
        # opened dataset (for performance boost), will be reset if data_dir is
        # changed
        self._filename = None
        self._filedata = None

        self._file_mask = None
        self._files = None

        self.var_map = get_emep_variables()

        data_dir, filename, data_id = self._eval_input(filepath, data_id,
                                                       data_dir)
        self.data_id = data_id
        if data_dir is not None:
            self.data_dir = data_dir

        if filename is None:
            filename = self.DEFAULT_FILE_NAME

        self.filename = filename

    def _eval_input(self, filepath, data_id, data_dir):
        """
        Evaluate input (helper method for __init__)

        Note, this method does not change the associated class attributes, it
        just does some sanity checking on what the user inputs.

        Parameters
        ----------
        filepath : str, optional
            path to file to be read
        data_id : str, optional
            ID of dataset
        data_dir : str, optional
            directory containing EMEP data files

        Raises
        ------
        FileNotFoundError
            if any of input data_dir or filepath are provided but do not exist
        ValueError
            if any of input data_dir or filepath are provided but are not
            a directory or file, respectively.

        Returns
        -------
        tuple
            3-element tuple containing (potentially updated / inferred values of):

                - `data_dir`
                - `filename`
                - `data_id`

        """
        filename = None
        if filepath is not None:
            if not isinstance(filepath, str) or not os.path.exists(filepath):
                raise FileNotFoundError(f'{filepath}')
            if os.path.isdir(filepath):
                raise ValueError(f'{filepath} is a directory, please use data_dir')
            data_dir,filename = os.path.split(filepath)

        if data_dir is not None:
            if not isinstance(data_dir, str) or not os.path.exists(data_dir):
                raise FileNotFoundError(f'{data_dir}')
            if not os.path.isdir(data_dir):
                raise ValueError(f'{data_dir} is not a directory')
        if data_id is None and data_dir is not None:
            data_id = data_dir.split(os.sep)[-1]
        return (data_dir,filename,data_id)

    @property
    def data_dir(self):
        """
        Directory containing netcdf files
        """
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val):
        if not os.path.isdir(val):
            raise FileNotFoundError(val)
        mask, filelist = self._check_files_in_data_dir(val)
        self._file_mask = mask
        self._files = filelist
        self._data_dir = val
        self._filedata = None

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
        if not isinstance(val, str):
            raise ValueError('need str')
        elif val == self._filename:
            return
        self._filename = val
        self._filedata = None

    @property
    def filepath(self):
        """
        Path to data file
        """
        if self.data_dir is None:
            raise AttributeError('need data_dir to be set in data')
        return os.path.join(self.data_dir, self.filename)

    @filepath.setter
    def filepath(self, value):
        ddir, fname = os.path.split(value)
        self.data_dir = ddir
        self.filename = fname

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
            matches = glob.glob(f'{data_dir}/{fmask}')
            if len(matches) > 0:
                return fmask, matches
        raise FileNotFoundError(
            f'No valid model files could be found in {data_dir} for any of the '
            f'supported file masks: {self.FILE_MASKS}')

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
            raise AttributeError('please set data_dir first')
        tsts = []
        for file in self._files:
            tsts.append(self.ts_type_from_filename(file))
        return tsts

    @property
    def years_avail(self):
        """
        Years available in loaded dataset
        """
        data = self.filedata
        years = data.time.dt.year.values
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
        xarray.Dataset

        """
        fp = self.filepath
        const.print_log.info(f'Opening {fp}')

        ds = xr.open_dataset(fp)
        self._filedata = ds
        return ds

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'ReadMscwCtm'


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
        raise ValueError(f'Failed to retrieve ts_type from filename {filename}')

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
                fname = mask.replace('*', substr)
                return fname
        raise ValueError('failed to infer filename from input ts_type={ts_type}')

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
        const.print_log.info(
                f'computing {var_name_aerocom} from {req} using {aux_func}'
                )
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
        if var_name_aerocom in self.var_map: #can be read
            return self._read_var_from_file(var_name_aerocom, ts_type)
        elif var_name_aerocom in self.AUX_REQUIRES:
            return self._compute_var(var_name_aerocom, ts_type)
        raise VarNotAvailableError('Variable {var_name} is not supported')

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

        if self.data_dir is None:
            raise ValueError('data_dir must be set before reading.')
        elif self.filename is None and ts_type is None:
            raise ValueError('please specify ts_type')
        elif ts_type is not None:
            #filename and ts_type are set. update filename if ts_type suggests
            #that current file has different resolution
            self.filename = self.filename_from_ts_type(ts_type)

        ts_type = self.ts_type

        arr = self._load_var(var_name_aerocom, ts_type)
        try:
            cube = arr.to_iris()
        except MemoryError as e:
            raise NotImplementedError(f'BAAAM: {e}')

        if ts_type == 'hourly':
            cube.coord('time').convert_units('hours since 1900-01-01')
        gridded = GriddedData(cube, var_name=var_name_aerocom,
                              ts_type=ts_type, check_unit=False,
                              convert_unit_on_init=False)

        if var.is_deposition:
            implicit_to_explicit_rates(gridded, ts_type)

        # At this point a GriddedData object with name gridded should exist

        gridded.metadata['data_id'] = self.data_id
        gridded.metadata['from_files'] = self.filepath

        # Remove unneccessary metadata. Better way to do this?
        for metadata in ['current_date_first', 'current_date_last']:
            if metadata in gridded.metadata.keys():
                del(gridded.metadata[metadata])
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
            data = self.filedata[emep_var]
        except KeyError:
            raise VarNotAvailableError(
                f'{var_name_aerocom} ({emep_var}) not available in {self.filename}')
        data.attrs['long_name'] = var_name_aerocom
        data.time.attrs['long_name'] = 'time'
        data.time.attrs['standard_name'] = 'time'
        prefix = emep_var.split('_')[0]
        data.attrs['units'] = self.preprocess_units(data.units, prefix)
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
        if units == '' and prefix == 'AOD': #
            return '1'
        elif units == '' and prefix == 'AbsCoef':
            return 'm-1'

class ReadEMEP(ReadMscwCtm):
    """Old name of :class:`ReadMscwCtm`."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("You are using a deprecated name ReadEMEP for class ReadMscwCtm")




if __name__ == '__main__': # pragma: no cover

    EMEP_DIR = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_REPORTING/EMEP01_rv4_35_2018_emepCRef2_XtraOut/'

    fname = 'Base_month.nc'

    fp = EMEP_DIR + fname

    reader = ReadMscwCtm(data_dir=EMEP_DIR)#+'Base_month.nc')


    # Read variable that uses AUX_FUNS
    data = reader.read_var('concno3', ts_type='daily')
