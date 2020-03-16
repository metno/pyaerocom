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
from pyaerocom.variable import emep_variable_path
from pyaerocom.griddeddata import GriddedData
from pyaerocom.tstype import TsType
from pyaerocom.helpers import seconds_in_periods

class ReadEMEP(object):
    
    
    # TODO: Unit conversion - EMEP units not specified as per time unit
    # TODO: 
    
    def __init__(self, filepath, data_id=None, var_file=None):
        
        self._filepath = filepath
        self._data_id = data_id
        self._var_file = var_file
        
        try:
            open(filepath, 'r')
            # open(var_file, 'r')
        except Exception as e:
            const.print_log.exception('File "{}" not found. Error message: {}'.format(filepath, self._filepath,
                                                       repr(e)))

        #: dictionary containing information about additionally required variables
        #: for each auxiliary variable (i.e. each variable that is not provided
        #: by the original data but computed on import)
        self.AUX_REQUIRES = {'depso4'     :   ['dryso4','wetso4']}


       #: Functions that are used to compute additional variables (i.e. one 
       #: for each variable defined in AUX_REQUIRES)
        self.AUX_FUNS = {'depso4'     :   add_cubes}
    
    
    
    def __str__(self):
        # TODO: List variables?
        raise NotImplementedError
    
    
    def read_var(self, var_name, start=None, stop=None,
                 ts_type=None, experiment=None, vert_which=None, 
                 flex_ts_type=True, prefer_longer=False, 
                 aux_vars=None, aux_fun=None, **kwargs):
        """Read EMEP data, rename to Aerocom naming and return GriddedData object"""

        var_map = self.map_aero_emep()
            
        #: Variable need processing
        if var_name in self.AUX_REQUIRES:
            temp_cubes = []
            for aux_var in self.AUX_REQUIRES[var_name]:
                temp_cubes.append(self.read_var(aux_var))
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
                data.attrs['units'] = 'mg/m2'
            gridded = GriddedData(data.to_iris(), var_name=var_name, ts_type=ts_type)
        

                
            
        # TODO: Figure out what the data_id should be for EMEP data
        # gridded.metadata['data_id'] = data_id
        gridded.time.long_name = 'time' # quickplot_map expects time long name to be time.
        gridded.metadata['data_id'] = self._data_id
        # Remove unneccessary(?) metadata. Better way to do this?
        del(gridded.metadata['current_date_first'])
        del(gridded.metadata['current_date_last'])



        # Convert mg/m^2 (implicit per day, month or year) -> kg
        if EMEP_prefix in ['WDEP', 'DDEP']:
            # mg -> kg
            gridded.to_xarray().values *= 10**-6
            # day/month/year -> s
            if TsType(ts_type) == TsType('monthly'):
                timestamps = gridded.time_stamps()
                seconds_in_month = seconds_in_periods(timestamps, ts_type)
                for i in range(len(seconds_in_month)):
                    gridded.to_xarray().isel(time=i).values /= seconds_in_month[i]
                gridded.units = 'kg m-2 s-1'


# =============================================================================
#         gridded.var_name = var_name  # TODO: check that this is working
#         # Replaced by passing var_name to GriddedData
# 
# =============================================================================
        return gridded


    def read(self, vars_to_retrieve, start=None, stop=None,
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

    def map_aero_emep(self):
        """Read variable mapping to dictionary: Aerocom -> EMEP"""
        variables = {}
        if not self._var_file:
            self._var_file = emep_variable_path()    
        with open(self._var_file, 'r') as var_file:
            for line in var_file.readlines():
                var = line.split("'")[1]
                aer_var, emep_var = var.split('=')
                variables[aer_var] = emep_var
        return variables        
    
    
if __name__ == '__main__':
    
    basepath = '/home/eirikg/Desktop/pyaerocom/data/2020_AerocomHIST/'
    
    file = '2010_GLOB1_2010met/Base_month.nc'
    var_file= basepath + 'vars_sorted.sh'
    filepath = '{}{}'.format(basepath, file)

    # from pyaerocom.units_helpers import unit_conversion_fac_custom


    reader = ReadEMEP(filepath, var_file=var_file, data_id='EMEP')
    sconcno = reader.read_var('sconcno', ts_type='monthly')

    
# =============================================================================
#     basepath = '/home/eirikg/Desktop/pyaerocom/data/'
#     file = '2020_AerocomHIST/1850_GLOB1_2010met/Base_month.nc'
#     filepath = '{}{}'.format(basepath, file)
# 
#     reader = ReadEMEP(filepath, data_id='EMEP')
#     wetso4 = reader.read_var('wetso4', ts_type='monthly')
#     from pyaerocom.io.readgridded import ReadGridded
#     control_dir = '/home/eirikg/Desktop/pyaerocom/data/2020_AerocomHIST/control'
#     control_reader = ReadGridded(data_dir=control_dir)
#     wetso4_control = control_reader.read_var('wetso4')
#     
#     coloc = pya.colocation.colocate_gridded_gridded(wetso4, wetso4_control)
# =============================================================================
