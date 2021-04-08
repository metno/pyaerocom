#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
from pyaerocom import StationData
import numpy as np
import pandas as pd


def _load_coldata_tm5_aeronet_from_scratch(file_path):
    from xarray import open_dataarray
    from pyaerocom import ColocatedData
    arr = open_dataarray(file_path)
    if '_min_num_obs' in arr.attrs:
        info = {}
        for val in arr.attrs['_min_num_obs'].split(';')[:-1]:
            to, fr, num = val.split(',')
            if not to in info:
                info[to] = {}
            if not fr in info[to]:
                info[to][fr] = {}
            info[to][fr] = int(num)
        arr.attrs['min_num_obs'] = info
    cd = ColocatedData()
    cd.data = arr
    return cd

def create_fake_station_data(addvars, varinfo, varvals, start, stop, freq,
                              meta):
    if isinstance(addvars, str):
        addvars = [addvars]
    stat = StationData()
    stat.update(**meta)
    dtime = pd.date_range(start, stop, freq=freq).values
    stat['dtime'] = dtime
    for var in addvars:
        if var in varinfo:
            stat.var_info[var] = varinfo[var]
        if isinstance(varvals, dict):
            val = varvals[var]
        else:
            val = varvals
        stat[var] = np.ones(len(dtime)) * val
    return stat

def create_fake_stationdata_list():
    stats = [
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  10, '2010-01-01', '2010-12-31', 'd',
                                  {'awesomeness' : 10,
                                   'data_revision' : 20120101,
                                   'ts_type' : 'daily', 'latitude' : 10,
                                   'longitude' : 20, 'altitude' : 0,
                                   'station_name' : 'FakeSite'}),
        # overlaps with first one
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  20, '2010-06-01', '2011-12-31', 'd',
                                  {'awesomeness' : 12,
                                   'data_revision' : 20110101,
                                   'ts_type' : 'daily', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # monthly, but missing ts_type and wrong unit
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'mole mole-1'}},
                                  20, '2014-01-01', '2015-12-31', '3MS',
                                  {'awesomeness' : 2,
                                   'data_revision' : 20140101,
                                   'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # invalid ts_type
        create_fake_station_data('concpm10', {'concpm10': {'units' : 'ug m-3'}},
                                  20, '1850', '2020', '1000d',
                                  {'awesomeness' : 15,
                                   'data_revision' : 20130101,
                                   'ts_type' : '1000daily', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        # new variable and monthly
        create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  1, '2005', '2012', 'MS',
                                  {'awesomeness' : 42,
                                   'data_revision' : 20200101,
                                   'ts_type' : 'monthly', 'latitude' : 42.001,
                                   'longitude' : 20, 'altitude' : 0.1,
                                   'station_name' : 'FakeSite'}),

        create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  0.1, '2008', '2009', '60d',
                                  {'awesomeness' : 46,
                                   'data_revision' : 20200101,
                                   'ts_type' : '60daily', 'latitude' : 22.001,
                                   'longitude' : 10, 'altitude' : 100,
                                   'station_name' : 'FakeSite2'})
        ]

    stat_werr = create_fake_station_data('od550aer', {'od550aer': {'units' : '1'}},
                                  0.2, '2010', '2016', '10d',
                                  {'awesomeness' : 30,
                                   'data_revision' : 20200101,
                                   'ts_type' : '10daily', 'latitude' : 22.001,
                                   'longitude' : 10, 'altitude' : 100,
                                   'station_name' : 'FakeSite2'})
    stat_werr.data_err['od550aer'] = np.ones(len(stat_werr.dtime))*9999
    stats.append(stat_werr)
    return stats

if __name__ == '__main__':
    import pyaerocom as pya
    stats = create_fake_stationdata_list()

    for stat in stats:
        print(stat)
