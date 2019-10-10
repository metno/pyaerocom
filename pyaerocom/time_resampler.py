#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module containing time resampling functionality
"""
import pandas as pd
import xarray as xarr
from pyaerocom import const
from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.tstype import TsType
from pyaerocom.time_config import TS_TYPE_TO_PANDAS_FREQ
from pyaerocom.helpers import (resample_time_dataarray, 
                               resample_timeseries, isnumeric)

class TimeResampler(object):
    """Object that can be use to resample timeseries data
    
    It supports hierarchical resampling of :class:`xarray.DataArray` objects 
    and :class:`pandas.Series` objects.
    
    Hierarchical means, that resampling constraints can be applied for each 
    level, that is, if hourly data is to be resampled to monthly, it may be 
    specified to first required minimum number of hours per day, and minimum
    days per month, to create the output data.
    """
    SAMPLING_CONSTRAINTS = const.OBS_MIN_NUM_RESAMPLE
    APPLY_CONSTRAINTS = const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS
    FREQS_SUPPORTED = TS_TYPE_TO_PANDAS_FREQ
    def __init__(self, input_data=None):
        self.last_setup = None
        self._input_data = None
        self.input_data = input_data
        self.valid_base_ts_types = [x for x in const.GRID_IO.TS_TYPES if 
                                    TsType(x).mulfac==1]
    
    @property
    def input_data(self):
        """Input data object that is to be resampled"""
        return self._input_data
    
    @input_data.setter
    def input_data(self, val):
        if not isinstance(val, (pd.Series, xarr.DataArray)):
            raise ValueError('Invalid input: need Series or DataArray')
        self._input_data = val
        
    @property
    def fun(self):
        """Resamplig method (depends on input data type)"""
        if isinstance(self.input_data, pd.Series):
            return resample_timeseries
        return resample_time_dataarray
    
    def _gen_idx(self, from_ts_type, to_ts_type, min_num_obs):
        if isnumeric(min_num_obs):
            return [(to_ts_type.val, int(min_num_obs))]
        if not isinstance(min_num_obs, dict):
            raise ValueError('Invalid input for min_num_obs, need dictionary '
                             'or integer, got {}'.format(min_num_obs))
        valid = self.valid_base_ts_types
        from_mul = from_ts_type.mulfac
        if from_mul != 1:
            const.print_log.warn('Ignoring multiplication factor {} in '
                                 'data with resolution {} in resampling method'
                                 .format(from_mul, from_ts_type))
        start = valid.index(from_ts_type.base)
        stop = valid.index(to_ts_type.base) 
        
        last_from = valid[start]
        idx = []
        for i in range(start+1, stop+1):
            to = valid[i]
            if to in min_num_obs and last_from in min_num_obs[to]:
                
                min_num = min_num_obs[to][last_from]
                last_from = to
                idx.append((to, min_num))
        if len(idx) == 0 or not idx[-1][0] == to_ts_type.base:
            idx.append((to_ts_type.base, 0))
        return idx
    
    def resample(self, to_ts_type, input_data=None, from_ts_type=None, 
                 how='mean', apply_constraints=False, 
                 min_num_obs=None, **kwargs):
        """Resample input data
        
        Parameters
        ----------
        input_data : pandas.Series or xarray.DataArray
            data to be resampled
        to_ts_type : str or pyaerocom.tstype.TsType
            output resolution
        how : str
            string specifying how the data is to be aggregated, default is mean
        apply_constraints : bool, optional
            if True, hierarchical resampling is applied using input 
            `samping_constraints` (if provided) or else, using constraints 
            specified in :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`
        min_num_obs : dict or int, optinal
            integer or nested dictionary specifying minimum number of 
            observations required to resample from higher to lower frequency.
            For instance, if `input_data` is hourly and `to_ts_type` is
            monthly, you may specify something like::
                
                min_num_obs = 
                    {'monthly'  :   {'daily'  : 7}, 
                     'daily'    :   {'hourly' : 6}}
                    
            to require at least 6 hours per day and 7 days per month. Or, if 
            data is daily and output is monthly and   
        **kwargs
           additional input arguments passed to resampling method
          
        Returns
        -------
        pandas.Series or xarray.DataArray
            resampled data object
        """
        if not isinstance(to_ts_type, TsType):
            to_ts_type = TsType(to_ts_type)
        
        if not to_ts_type.val in self.FREQS_SUPPORTED:
            raise NotImplementedError('Cannot resample to input frequency '
                                      '{}. Choose from: {}'
                                      .format(to_ts_type, 
                                              self.FREQS_SUPPORTED.keys()))
        
        if input_data is not None:
            self.input_data = input_data
        if self.input_data is None:
            raise ValueError('Please provide data (Series or DataArray)')
        
        if apply_constraints is None:
            apply_constraints = self.APPLY_CONSTRAINTS
        
        if not apply_constraints:
            self.last_setup = dict(apply_constraints=False,
                                   min_num_obs=None)
            return self.fun(self.input_data, freq=to_ts_type.val, 
                            how=how, **kwargs)
        elif from_ts_type is None:
            const.print_log.warn('Cannot apply time resampling constraints, '
                                 'since input from_ts_type is None. Applying '
                                 'resampling to {} without any constraints'
                                 .format(to_ts_type))
            self.last_setup = dict(apply_constraints=False,
                                   min_num_obs=None)
            return self.fun(self.input_data, freq=to_ts_type.val, 
                            how=how, **kwargs)
        
        if isinstance(from_ts_type, str):
            from_ts_type = TsType(from_ts_type)
        
        if not isinstance(from_ts_type, TsType):
            raise ValueError('Invalid input for from_ts_type: {}. Need valid '
                             'str or TsType. Input arg from_ts_type is '
                             'required if resampling using hierarchical '
                             'constraints (arg apply_constraints) is activated'
                             .format(from_ts_type))
        
        if to_ts_type > from_ts_type:
            raise TemporalResolutionError('Cannot resample time-series from {} '
                                          'to {}'
                                          .format(from_ts_type, to_ts_type))
        elif to_ts_type == from_ts_type:
            const.logger.info('Input time frequency equals current frequency '
                              'of data, ignoring any resampling constraints')
            self.last_setup = dict(apply_constraints=False,
                                   min_num_obs=None)
            return self.fun(self.input_data, freq=to_ts_type.val, how=how, 
                            **kwargs)
            
        if min_num_obs is None:
            min_num_obs = self.SAMPLING_CONSTRAINTS
            
        _idx = self._gen_idx(from_ts_type, to_ts_type, min_num_obs)
        data = self.input_data
        for to_ts_type, mno in _idx:
            data = self.fun(data, freq=to_ts_type, how=how, 
                            min_num_obs=mno)
        self.last_setup = dict(apply_constraints=True,
                               min_num_obs=min_num_obs)   
        return data
    
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pyaerocom as pya

    plt.close('all')
    data = pya.io.ReadUngridded().read('EBASMC', 'scatc550dryaer')
    
    data.set_flags_nan()
    data = data.apply_filters(data_level=2, remove_outliers=True)
        
    stat = data.to_station_data('Bondvil*')
    
    hourly = stat.scatc550dryaer
    
    resampler = TimeResampler(hourly)
    
    monthly = resampler.resample('monthly', apply_constraints=True, 
                                from_ts_type='hourly')
    
    monthly1 = resampler.resample('monthly', apply_constraints=False)
    
    yearly = resampler.resample('yearly', apply_constraints=True, 
                                from_ts_type='hourly')
    
    yearly1 = resampler.resample('yearly', apply_constraints=False)
    
    fig, ax = plt.subplots(1,1, figsize=(18, 12))
    
    hourly.plot(style=' x', color='#e6e6e6', label='hourly (raw)', ax=ax)
    monthly.plot(style='-+b', label='monthly (C)')
    monthly1.plot(style=' xr', label='monthly (raw)')
    
    yearly.plot(style='-o', markersize=12, color='lime', label='yearly (C)')
    yearly1.plot(style=' o', markersize=8, color='red', label='yearly (raw)')
    
    ax.legend()
    
    fig, ax = plt.subplots(1,1, figsize=(12, 12))
    ax.plot(yearly, yearly1, ' x', color='lime')
    ax.set_xlabel('yearly (C)')
    ax.set_ylabel('yearly (raw)')



        
        
        
        
        
        
                
            
        
            
        
        
        
            
    