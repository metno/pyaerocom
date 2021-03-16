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
from pyaerocom.io.aux_read_cubes import add_cubes, subtract_cubes
from pyaerocom.variable import get_emep_variables
from pyaerocom.griddeddata import GriddedData
from pyaerocom.units_helpers import implicit_to_explicit_rates

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
    data_dir : str
        Base directory of EMEP data, containing one or more netcdf files
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
    AUX_FUNS = {'depso4' : add_cubes,
                'concbc' : add_cubes,
                'concno3' : add_cubes,
                'conctno3' : add_cubes,
                'concoa' : add_cubes,
                'concpmgt25': subtract_cubes
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

            if data_id is None:
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

    def compute_var(self, var_name_aerocom, ts_type):
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
        if not var_name_aerocom in self.AUX_REQUIRES:
            raise AttributeError(
                f'{var_name_aerocom} cannot be computed, only '
                f'{list(self.AUX_REQUIRES)}')
        temp_cubes = []
        req = self.AUX_REQUIRES[var_name_aerocom]
        aux_func = self.AUX_FUNS[var_name_aerocom]
        const.print_log.info(
                f'computing {var_name_aerocom} from {req} using {aux_func}'
                )
        for aux_var in self.AUX_REQUIRES[var_name_aerocom]:
            temp_cubes.append(self.read_var(aux_var, ts_type=ts_type))

        cube = aux_func(*temp_cubes)
        return GriddedData(cube, var_name=var_name_aerocom,
                           ts_type=ts_type, computed=True)

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
        var_name_aerocom = const.VARS[var_name].var_name_aerocom

        if self.data_dir is None:
            raise ValueError('data_dir must be set before reading.')
        elif self.filename is None and ts_type is None:
            raise ValueError('please specify ts_type')
        elif ts_type is not None:
            #filename and ts_type are set. update filename if ts_type suggests
            #that current file has different resolution
            self.filename = self.filename_from_ts_type(ts_type)

        ts_type = self.ts_type
        if var_name_aerocom in self.AUX_REQUIRES:
            gridded = self.compute_var(var_name_aerocom, ts_type)
        else:
            gridded = self._gridded_from_filedata(var_name_aerocom, ts_type)

        # At this point a GriddedData object with name gridded should exist

        gridded.metadata['data_id'] = self.data_id
        gridded.metadata['from_files'] = self.filepath

        # Remove unneccessary metadata. Better way to do this?
        for metadata in ['current_date_first', 'current_date_last']:
            if metadata in gridded.metadata.keys():
                del(gridded.metadata[metadata])
        return gridded

    def _gridded_from_filedata(self, var_name_aerocom, ts_type):
        emep_var = self.var_map[var_name_aerocom]

        prefix = emep_var.split('_')[0]
        try:
            data = self.filedata[emep_var]
        except KeyError:
            raise VarNotAvailableError(
                f'{var_name_aerocom} ({emep_var}) not available in {self.filename}')
        data.attrs['long_name'] = var_name_aerocom
        data.time.attrs['long_name'] = 'time'
        data.time.attrs['standard_name'] = 'time'
        data.attrs['units'] = self.preprocess_units(data.units, prefix)
        cube = data.to_iris()
        if ts_type == 'hourly':
            cube.coord('time').convert_units('hours since 1900-01-01')
        gridded = GriddedData(cube, var_name=var_name_aerocom,
                              ts_type=ts_type, check_unit=False,
                              convert_unit_on_init=False)

        if prefix in ['WDEP', 'DDEP']:
            implicit_to_explicit_rates(gridded, ts_type)
        return gridded

    @staticmethod
    def preprocess_units(units, prefix=None):
        new_unit = units
        if units == '' and prefix == 'AOD': #
            new_unit = '1'
        elif units == '' and prefix == 'AbsCoef':
            new_unit = 'm-1'
            new_unit = units
        elif units == 'mgS/m2' or units == 'mgN/m2':
            raise NotImplementedError('Species specific units are not implemented.')
        return new_unit

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
