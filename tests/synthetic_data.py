    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains methods to create synthetic data objects for unit testing

Created on Mon May 13 11:24:39 2019

@author: jonasg
"""
import numpy as np
from pyaerocom import StationData

def _make_station_data1():
    stat = StationData()

    d = dict(latitude = 33,
             longitude = 15,
             altitude = 300,
             dataset_name = 'test',
             PI = 'jonas gliss',
             instrument_name = 'test instr',
             station_id = 42,
             station_name = 'test station',
             ts_type =  'monthly',
             revision_date = '20190513',
             data_level=2,
             country='norway',
             data_version=2)

    stat.update(d)

    START = '2000'
    NUM_YEARS = 5
    NUM = NUM_YEARS * 12
    stat.dtime = np.datetime64(START) + np.arange(NUM).astype('timedelta64[M]')

    stat.ec550aer = np.random.random_sample(NUM) -.5
    stat.od550aer = np.ones(NUM)

    stat.var_info['ec550aer'] = {'units' : 'm-1'}
    stat.var_info['od550aer'] = {'units' : '1'}

    return stat

def _make_station_data2():
    """Create an example synthetic instance of StationData class"""
    stat = StationData()
    d = dict(latitude = 33.01,
             longitude = 15,
             altitude = 300,
             dataset_name = 'test (alt)',
             PI = 'Jonas Gliss',
             instrument_name = 'test instr',
             station_id = 42,
             station_name = 'test station',
             ts_type =  'daily',
             revision_date = '20190513',
             data_level=3,
             country='norway',
             data_version=2)

    stat.update(d)

    START = '2007'
    NUM_DAYS = 277

    stat.dtime = np.datetime64(START) + np.arange(NUM_DAYS).astype('timedelta64[D]')

    stat.ec550aer = np.random.random_sample(NUM_DAYS) -.5
    stat.od550aer = np.ones(NUM_DAYS)
    stat.conco3 = np.arange(NUM_DAYS)

    stat.var_info['ec550aer'] = {'units' : 'Mm-1'}
    stat.var_info['od550aer'] = {'units' : '1'}
    stat.var_info['conco3']  = {'units' : 'ug m-3'}

    return stat

class DataAccess:
    """Factory for loading and accessing of data objects"""
    _LOADERS = dict(station_data1 = _make_station_data1,
                    station_data2 = _make_station_data2)

    def __getitem__(self, key):
        if key in self.__dict__: # item is loaded
            return self.__dict__[key]
        data = self._LOADERS[key]()
        self.__dict__[key] = data
        return data

if __name__ == '__main__':
    acc = DataAccess()
