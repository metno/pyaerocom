#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:20:04 2020

@author: eirikg
"""

import xarray as xr
import sys
import pyaerocom as pya
from pyaerocom import const, print_log, logger
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.variable import get_emep_variables
from pyaerocom.griddeddata import GriddedData
from pyaerocom.tstype import TsType
from pyaerocom.helpers import seconds_in_periods


class ReadEMEP(object):
    
    
    def __init__(self, filepath, data_id=None, var_file=None):
        """
        var_file: path
            Use alternative EMEP -> Aerocom variable mapping.
        """
        
        self._filepath = filepath
        self._data_id = data_id
        self._var_file = var_file
        
        try:
            open(filepath, 'r')
        except Exception as e:
            const.print_log.exception('File "{}" not found. Error message: {}'.format(filepath, self._filepath,
                                                       repr(e)))

        # dictionary containing information about additionally required variables
        # for each auxiliary variable (i.e. each variable that is not provided
        # by the original data but computed on import)
        self.AUX_REQUIRES = {'depso4' : ['dryso4','wetso4'],
                             'sconcbc' : ['sconcbcf', 'sconcbcc'],
                             'sconcno3' : ['sconcno3c', 'sconcno3f'],
                             'sconctno3' : ['sconcno3', 'sconchno3']}


       # Functions that are used to compute additional variables (i.e. one 
       # for each variable defined in AUX_REQUIRES)
        self.AUX_FUNS = {'depso4' : add_cubes,
                         'sconcbc' : add_cubes,
                         'sconcno3' : add_cubes,
                         'sconctno3' : add_cubes}
    
    
    
    def __str__(self):
        # TODO: List variables?
        raise NotImplementedError
    
    
    def read_var(self, var_name, start=None, stop=None,
                 ts_type=None, experiment=None, vert_which=None, 
                 flex_ts_type=True, prefer_longer=False, 
                 aux_vars=None, aux_fun=None, **kwargs):
        """Read EMEP variable, rename to Aerocom naming and return GriddedData object"""

        var_map = get_emep_variables()
            
        if var_name in self.AUX_REQUIRES:
            temp_cubes = []
            for aux_var in self.AUX_REQUIRES[var_name]:
                temp_cubes.append(self.read_var(aux_var, ts_type=ts_type))
            aux_func = self.AUX_FUNS[var_name]
            cube = aux_func(*temp_cubes)
            # cube.var_name = var_name
            gridded = GriddedData(cube, var_name=var_name, ts_type=ts_type, computed=True)
        else:
            try:
                emep_var = var_map[var_name]
            except KeyError as e:
                const.print_log.exception('Variable {} not in EMEP mapping.'.format(var_name))
                sys.exit(1)
                
            EMEP_prefix = emep_var.split('_')[0]
            
            data = xr.open_dataset(self._filepath)[emep_var]
            
            
            data.attrs['long_name'] = var_name
            
            if (EMEP_prefix in ['WDEP', 'DDEP']) and emep_var != 'WDEP_PREC':
                # Get rid of units (S, N f.e.) that cannot be handled with CF units
                data.attrs['units'] = 'ug/m2' # Very hardcoded. Is this always true?
            gridded = GriddedData(data.to_iris(), var_name=var_name, ts_type=ts_type)
        
            # Convert mg/m^2 (implicit per day, month or year) -> kg
            if EMEP_prefix in ['WDEP', 'DDEP']:
                # TODO: This is duplicated. Need better flow.
                gridded.time.long_name = 'time' # quickplot_map expects time long name to be time.
                gridded.time.standard_name = 'time'
                gridded._update_coord_info()
                self.implicit_to_explicit_rates(gridded, ts_type)

        
        # At this point a GriddedData object with name gridded should exist
                
        gridded.time.long_name = 'time' # quickplot_map expects time long name to be time.
        gridded.time.standard_name = 'time'
        gridded._update_coord_info()
        gridded.metadata['data_id'] = self._data_id
        # Remove unneccessary(?) metadata. Better way to do this?

        try:
            del(gridded.metadata['current_date_first'])
            del(gridded.metadata['current_date_last'])
            # ReadGridded cannot concatenate several years of data if this is missing
            gridded.metadata['from_files'] = self._filepath 
        except KeyError as e:
            const.print_log.exception('Metadata not available: {}'.format(repr(e)))

        return gridded


    def implicit_to_explicit_rates(self, gridded, ts_type):
        """
        Convert implicit daily, monthly or yearly rates to per second.
        And set units to 'kg m-2 s-1'.
        """

        gridded.to_xarray().values *= 10**-6  # ug -> kg
        timestamps = gridded.time_stamps()
        seconds_factor = seconds_in_periods(timestamps, ts_type)
        for i in range(len(seconds_factor)):
            gridded.to_xarray().isel(time=i).values /= seconds_factor[i]
        gridded.units = 'kg m-2 s-1'
        

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
    
    
if __name__ == '__main__':
    
    basepath = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_AerocomHIST/'
    file = '2010_GLOB1_2010met/Base_month.nc' # 2010 emissions with 2010 meteorology
    var_file= basepath + 'vars_sorted.sh'
    filepath = '{}{}'.format(basepath, file)

    # Create reader using 
    reader = ReadEMEP(filepath, data_id='EMEP')
    # Read variable that uses AUX_FUNS
    depso4 = reader.read_var('depso4', ts_type='monthly')
    # Read variable that uses unit conversions
    wetso4 = reader.read_var('wetso4', ts_type='monthly')
