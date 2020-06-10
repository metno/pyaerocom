#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:20:04 2020

@author: eirikg
"""

import xarray as xr
import os
import glob
import pyaerocom as pya
from pyaerocom import const, print_log, logger
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.variable import get_emep_variables
from pyaerocom.griddeddata import GriddedData
from pyaerocom.tstype import TsType
from pyaerocom.helpers import seconds_in_periods
from pyaerocom.variable import get_aliases
from pyaerocom.units_helpers import implicit_to_explicit_rates


class ReadEMEP(object):
    """
    Class for reading EMEP model output data.

    Parameters
    ----------
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    filepath : str
        Path to netcdf file.
    data_dir : str

    Attributes
    ----------
    filepath :
    data_id :
    data_dir :
    vars_provided :
    """

    # dictionary containing information about additionally required variables
    # for each auxiliary variable (i.e. each variable that is not provided
    # by the original data but computed on import)
    AUX_REQUIRES = {'depso4' : ['dryso4','wetso4'],
                         'sconcbc' : ['sconcbcf', 'sconcbcc'],
                         'sconcno3' : ['sconcno3c', 'sconcno3f'],
                         # 'sconctno3' : ['sconcno3', 'sconchno3'],
                         'sconcoa' : ['sconcoac', 'sconcoaf']}

    # Functions that are used to compute additional variables (i.e. one
    # for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'depso4' : add_cubes,
                     'sconcbc' : add_cubes,
                     'sconcno3' : add_cubes,
                     'sconctno3' : add_cubes,
                     'sconcoa' : add_cubes}


    def __init__(self, filepath=None, data_dir=None, data_id=None):
        if (filepath and data_dir):
            raise ValueError('Either filepath or data_dir should be set, not both.')

        if data_dir is not None:
            self.data_dir = data_dir
        else:
            self._data_dir = None
        if filepath is not None:
            self.filepath = filepath
        else:
            self._filepath = None
        self.data_id = data_id

    def __str__(self):
        s = 'Reader: ReadEMEP\n'
        s += "Available frequencies: {}\n".format(self.ts_types)
        s += "Available variables: {}\n".format(self.vars_provided)
        return s

    @property
    def filepath(self):
        """
        Path to netcdf file
        """
        return self._filepath

    @filepath.setter
    def filepath(self, val):
        try:
            open(val, 'r')
        except Exception as e:
            const.print_log.warning('File "{}" not found. Error message: {}'.format(val, repr(e)))
            val = None
        self._filepath = val

    @property
    def data_dir(self):
        """
        Directory containing netcdf files
        """
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val):
        if not os.path.isdir(val):
            raise FileNotFoundError('Folder "{}" not found.'.format(val))
            val = None
        self._data_dir = val

    @property
    def ts_types(self):
        return self._available_ts_types()

    def _available_ts_types(self):
        ts_types = []
        if self.data_dir:
            files = os.listdir(self.data_dir)
            for filename in files:
                ts_types.append(self._ts_type_from_filename(filename))
        elif self.filepath:
            filename = self.filepath.split('/')[-1]
            ts_types.append(self._ts_type_from_filename(filename))
        return list(set(ts_types))

    @property
    def vars_provided(self):
        """Variables provided by this dataset"""
        return self._get_vars_provided()

    def _get_vars_provided(self):
        variables = None
        data_vars = set()
        for filepath in self._get_paths():
            data = xr.open_dataset(filepath)
            data_vars.update(set(data.keys()))
        emep_vars = set(get_emep_variables().values())
        available = data_vars.intersection(emep_vars)
        inv_emep = {v: k for k, v in get_emep_variables().items()}
        avail_aero = [ inv_emep[var] for var in available]
        variables = sorted(avail_aero)
        return variables

    def _get_paths(self):
        paths = []
        if self.filepath:
            paths = [self.filepath]
        if self.data_dir:
            pattern = os.path.join(self.data_dir, 'Base_*.nc')
            paths = glob.glob(pattern)
        return paths

    @property
    def data_id(self):
        """
        Data ID of dataset
        """
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        """
        """
        if not isinstance(val, str):
            val = None
        self._data_id = val

    def read(self, vars_to_retrieve, data_id=None, start=None, stop=None,
             ts_type=None, **kwargs):

        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        data = []
        for var_name in vars_to_retrieve:
            try:
                data.append(self.read_var(var_name, start, stop, ts_type, data_id=data_id))
            except Exception as e:
                const.print_log.exception('Failed to read data of {}\n'
                            'Error message: {}'.format(self._filepath,
                                                       repr(e)))
        return tuple(data)

    def read_var(self, var_name, start=None, stop=None,
                 ts_type=None, **kwargs):
        """Read EMEP variable, rename to Aerocom naming and return GriddedData object"""

        if not ts_type:
            ts_type = self._infer_ts_type()
        filepath = self._find_filepath(ts_type)
        gridded = self._load_gridded(var_name, filepath, ts_type)
        return gridded

    def _infer_ts_type(self):
        ts_type = None
        if self.data_dir:
            raise ValueError('ts_type needed when reading from a directory.')
        if self.filepath:
            const.print_log.warning('No ts_type, inferring from filename...')
            ts_type = self._ts_type_from_filename(self.filepath.split('/')[-1].split('.')[0])
            if not ts_type:
                raise ValueError('ts_type could not be inferred')
        return ts_type

    def _find_filepath(self, ts_type):
        if self.data_dir:
            filepath = self._filepath_from_data_dir(ts_type)
        elif self.filepath:
            filepath = self.filepath
        else:
            raise ValueError('Filepath or data_dir must be set before reading variable.')
        return filepath

    def _filepath_from_data_dir(self, ts_type):
        if ts_type == 'monthly':
            filename = 'Base_month.nc'
        elif ts_type == 'daily':
            filename = 'Base_day.nc'
        elif ts_type == 'yearly':
            filename = 'Base_fullrun.nc'
        else:
            raise ValueError('ts_type not recognized.')
        filepath = os.path.join(self.data_dir, filename)
        return filepath


    def _load_gridded(self, var_name, filepath, ts_type):
        if var_name in self.AUX_REQUIRES:
            return self._load_gridded_aux(var_name, filepath, ts_type)
        else:
            return self._load_gridded_standard(var_name, filepath, ts_type)

    def _load_gridded_standard(self, var_name, filepath, ts_type):
        try:
            emep_var = get_emep_variables()[var_name]
            EMEP_prefix = emep_var.split('_')[0]
        except KeyError as e:
            raise VarNotAvailableError('Variable {} not in EMEP mapping.'.format(var_name))
        data = xr.open_dataset(filepath)[emep_var]
        data = self._standardize_dataarray_metadata(data, var_name, filepath, EMEP_prefix)
        cube = data.to_iris()
        gridded = GriddedData(cube, var_name=var_name, ts_type=ts_type, convert_unit_on_init=False)
        if EMEP_prefix in ['WDEP', 'DDEP']:
            gridded = implicit_to_explicit_rates(gridded, ts_type)
        return gridded

    def _load_gridded_aux(self, var_name, filepath, ts_type):
        temp_cubes = []
        for aux_var in self.AUX_REQUIRES[var_name]:
            temp_cubes.append(self.read_var(aux_var, ts_type=ts_type))
        aux_func = self.AUX_FUNS[var_name]
        cube = aux_func(*temp_cubes)
        gridded = GriddedData(cube, var_name=var_name, ts_type=ts_type, computed=True)
        return gridded

    def _standardize_dataarray_metadata(self, data, var_name, filepath, EMEP_prefix):
        data.attrs['data_id'] = self.data_id
        data.attrs['from_files'] = filepath
        try:
            data.time.attrs['long_name'] = 'time'
            data.time.attrs['standard_name'] = 'time'
            data.attrs['units'] = self._preprocess_units(data.units, EMEP_prefix)
        except AttributeError as e:
            const.print_log.warning('Data has no time dimension.')
        for metadata in ['current_date_first', 'current_date_last']:
            if metadata in data.attrs.keys():
                del(data.attrs[metadata])
        return data

    @staticmethod
    def _preprocess_units(units, prefix=None):
        new_unit = units
        if units == '' and prefix == 'AOD': #
            new_unit = '1'
        elif units == 'mgS/m2' or units == 'mgN/m2':
            raise NotImplementedError('Species specific units are not implemented.')
            new_unit = units
        return new_unit

    @staticmethod
    def _ts_type_from_filename(filename):
        ts_type = None
        filename = filename.lower()
        filename = os.path.splitext(filename)[0]
        if filename == 'base_day':
            ts_type = 'daily'
        elif filename == 'base_month':
            ts_type = 'monthly'
        elif filename == 'base_fullrun':
            ts_type = 'yearly'
        return ts_type

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
        avail = self.vars_provided
        if var_name in avail:
            return True
        try:
            var = const.VARS[var_name]
        except VariableDefinitionError as e:
            const.print_log.warn(repr(e))
            return False

        for alias in var.aliases:
            if alias in avail:
                return True
        return False


if __name__ == '__main__':

    basepath = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_AerocomHIST/'
    file = '2010_GLOB1_2010met/Base_month.nc' # 2010 emissions with 2010 meteorology
    filepath = '{}{}'.format(basepath, file)

    reader = ReadEMEP(filepath, data_id='EMEP')
    depso4 = reader.read_var('depso4', ts_type='monthly')
    wetso4 = reader.read_var('wetso4', ts_type='monthly')
