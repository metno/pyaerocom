#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:20:04 2020

@author: eirikg
"""

import xarray as xr
import numpy as np
import sys
import os
import glob

import pyaerocom as pya
from pyaerocom import const, print_log, logger
from pyaerocom.exceptions import VarNotAvailableError, VariableDefinitionError
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.variable import get_emep_variables
from pyaerocom.griddeddata import GriddedData
from pyaerocom.tstype import TsType
from pyaerocom.helpers import seconds_in_periods
from pyaerocom.variable import get_aliases
from pyaerocom.units_helpers import implicit_to_explicit_rates




class ReadMscwCtm(object):
    """
    Class for reading model output from the EMEP MSC-W chemical transport model.

    Parameters
    ----------
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    filepath : str
        Path to netcdf file.
    data_dir : str, optional
        Base directory of EMEP data, containing one or more netcdf files

    Attributes
    ----------
    filepath : str
        Path to netcdf file
    data_id : str
        ID of model
    data_dir : str
        Base directory of EMEP data, containing one or more netcdf files
    vars_provided : str
        Variables that are available to read in filepath or data_dir
    ts_types : str
        Available temporal resolution in filepath or data_dir
    years_avail : str
        Years available for reading
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


    def __init__(self, filepath=None, data_id=None, data_dir=None):

        # if (filepath and data_dir):
        #     raise ValueError('Either filepath or data_dir should be set, not both.')

        if data_dir is not None:
            self.data_dir = data_dir
        else:
            self._data_dir = None
        if filepath is not None:
            self.filepath = filepath
        else:
            self._filepath = None
        self.data_id = data_id


    @property
    def filepath(self):
        """
        Path to netcdf file
        """
        return self._filepath


    @property
    def data_dir(self):
        """
        Directory containing netcdf files
        """
        return self._data_dir


    @filepath.setter
    def filepath(self, val):
        if not os.path.isfile(val):
            raise FileNotFoundError('Filepath {} not found.'.format(val))
        self._filepath = val
        self._data_dir = None


    @data_dir.setter
    def data_dir(self, val):
        if not os.path.isdir(val):
            raise FileNotFoundError('Folder "{}" not found.'.format(val))
        self._data_dir = val
        self._filepath = None


    @property
    def ts_types(self):
        return self._get_ts_types()


    @property
    def years_avail(self):
        """
        Years available in dataset
        """
        try:
            paths = self._get_paths()
            data = xr.open_dataset(paths[0])
            years = data.time.dt.year.values
            years = list(np.unique(years))
            return sorted(years)
        except Exception as e:
            return []


    @property
    def vars_provided(self):
        """Variables provided by this dataset"""
        return self._get_vars_provided()


    def _get_ts_types(self):
        ts_types = []
        if self.data_dir is not None:
            files = self._get_paths()
            for path in files:
                filename = path.split('/')[-1]
                ts_types.append(ts_type_from_filename(filename))
        elif self.filepath is not None:
            filename = self.filepath.split('/')[-1]
            ts_types.append(ts_type_from_filename(filename))
        return list(set(ts_types))

    def _get_paths(self):
        paths = []
        if self.filepath is not None:
            paths = [self.filepath]
        if self.data_dir is not None:
            pattern = os.path.join(self.data_dir, 'Base_*.nc')
            paths = glob.glob(pattern)
        return paths

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

    def __repr__(self):
            return self.__str__()

    def __str__(self):
        s = 'Reader: ReadMscwCtm\n'
        s += "Available frequencies: {}\n".format(self.ts_types)
        s += "Available variables: {}\n".format(self.vars_provided)
        return s


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
            const.print_log.warn(repr(e))
            return False
        #
        # if self.check_compute_var(var_name):
        #     return True
        #
        for alias in var.aliases:
            if alias in avail:
                return True
        #
        # if var.is_alias and var.var_name_aerocom in avail:
        #     return True

        return False


    def read_var(self, var_name, ts_type=None, **kwargs):
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. ("hourly", "daily", "monthly" , "yearly")

        Returns
        -------
        GriddedData
        """

        if self.filepath is None and self.data_dir is None:
            raise ValueError('filepath or data_dir must be set before reading.')
        elif self.data_dir is not None and ts_type is None:
            raise ValueError('ts_type must be set when reading from directory.')
        var_map = get_emep_variables()

        aliases = get_aliases(var_name)
        if len(aliases) == 1 and aliases[0] in var_map:
            var_name = aliases[0]

        # Find path to file based on ts_type
        filepath = ''
        if self.data_dir is not None:
            filename = ''
            if ts_type == 'monthly':
                filename = 'Base_month.nc'
            elif ts_type == 'hourly':
                filename = 'Base_hour.nc'
            elif ts_type == 'daily':
                filename = 'Base_day.nc'
            elif ts_type == 'yearly':
                filename = 'Base_fullrun.nc'
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.isfile(filepath):
                raise FileNotFoundError('Could not find file: {}'.format(filepath))
        elif self.filepath is not None:
            filepath = self.filepath
            if ts_type is None:
                ts_type = ts_type_from_filename(os.path.split(filepath)[-1])

        if var_name in self.AUX_REQUIRES:
            temp_cubes = []
            for aux_var in self.AUX_REQUIRES[var_name]:
                temp_cubes.append(self.read_var(aux_var, ts_type=ts_type))
            aux_func = self.AUX_FUNS[var_name]
            cube = aux_func(*temp_cubes)
            gridded = GriddedData(cube, var_name=var_name, ts_type=ts_type, computed=True)
        else:
            try:
                emep_var = var_map[var_name]
            except KeyError:
                raise VarNotAvailableError('Variable {} not in EMEP mapping.'.format(var_name))
            EMEP_prefix = emep_var.split('_')[0]
            data = xr.open_dataset(filepath)[emep_var]
            data.attrs['long_name'] = var_name
            data.time.attrs['long_name'] = 'time'
            data.time.attrs['standard_name'] = 'time'
            data.attrs['units'] = self.preprocess_units(data.units, EMEP_prefix)
            cube = data.to_iris()
            if ts_type == 'hourly':
                cube.coord('time').convert_units('hours since 1900-01-01')
            gridded = GriddedData(cube, var_name=var_name, ts_type=ts_type, convert_unit_on_init=False)

            if EMEP_prefix in ['WDEP', 'DDEP']:
                implicit_to_explicit_rates(gridded, ts_type)

        # At this point a GriddedData object with name gridded should exist

        gridded.metadata['data_id'] = self.data_id
        gridded.metadata['from_files'] = filepath # ReadGridded cannot concatenate several years of data if this is missing

        # Remove unneccessary metadata. Better way to do this?
        for metadata in ['current_date_first', 'current_date_last']:
            if metadata in gridded.metadata.keys():
                del(gridded.metadata[metadata])
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


def ts_type_from_filename(filename):
    ts_type = None
    filename = filename.lower()
    filename = os.path.splitext(filename)[0]
    if filename == 'base_day':
        ts_type = 'daily'
    elif filename == 'base_hour':
        ts_type = 'hourly'
    elif filename == 'base_month':
        ts_type = 'monthly'
    elif filename == 'base_fullrun':
        ts_type = 'yearly'
    return ts_type


class ReadEMEP(ReadMscwCtm):
    """Old name of :class:`ReadMscwCtm`."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("You are using a deprecated name ReadEMEP for class ReadMscwCtm")




if __name__ == '__main__':

    basepath = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_AerocomHIST/'
    file = '2010_GLOB1_2010met/Base_month.nc' # 2010 emissions with 2010 meteorology
    filepath = '{}{}'.format(basepath, file)

    reader = ReadMscwCtm(filepath, data_id='EMEP')
    # Read variable that uses AUX_FUNS
    depso4 = reader.read_var('wetsox', ts_type='monthly')
    # Read variable that uses unit conversions
    wetso4 = reader.read_var('wetso4', ts_type='monthly')
