#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import numpy.testing as npt
import numpy as np
import os
import pytest
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3


TEST_VARS = ['od550aer', 'ang4487aer']
    
def make_dataset():
    r = ReadAeronetSunV3()
    return r.read(file_pattern='G*', 
                  vars_to_retrieve=TEST_VARS)

@lustre_unavail
@pytest.fixture(scope='session')
def aeronetsunv3lev2_subset():
    return make_dataset()

@lustre_unavail
def test_shape_ungridded(aeronetsunv3lev2_subset):
    assert aeronetsunv3lev2_subset.shape == (63170, 12)
    
@lustre_unavail
def test_meta_blocks_ungridded(aeronetsunv3lev2_subset):
    assert len(aeronetsunv3lev2_subset.metadata) == 29
    assert len(aeronetsunv3lev2_subset.unique_station_names) == 29
    
    assert aeronetsunv3lev2_subset.unique_station_names == ['GISS',
                                         'GORDO_rest',
                                         'GOT_Seaprism',
                                         'GSFC',
                                         'Gageocho_Station',
                                         'Gainesville_Airport',
                                         'Gaithersburg',
                                         'Galata_Platform',
                                         'Gandhi_College',
                                         'Gangneung_WNU',
                                         'Georgia_Tech',
                                         'Glasgow_MO',
                                         'Gloria',
                                         'Gobabeb',
                                         'Goldstone',
                                         'Gorongosa',
                                         'Gosan_SNU',
                                         'Gotland',
                                         'Gozo',
                                         'Graciosa',
                                         'Granada',
                                         'Grand_Forks',
                                         'Granite_Island',
                                         'Grizzly_Bay',
                                         'Guadeloup',
                                         'Gual_Pahari',
                                         'Guam',
                                         'Gustav_Dalen_Tower',
                                         'Gwangju_GIST']

@lustre_unavail
def test_od550aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset:
        if not 'od550aer' in stat:
            no_odcount += 1
            continue
        mean = np.mean(stat.od550aer)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(stat.od550aer))
    assert no_odcount == 5
    npt.assert_allclose(actual=[np.mean(mean_vals), 
                                np.mean(std_vals)],
                        desired=[0.209, 0.149], atol=1e-2)
    
@lustre_unavail
def test_ang4487aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset:
        if not 'ang4487aer' in stat:
            no_odcount += 1
            continue
        mean = np.mean(stat.ang4487aer)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(stat.ang4487aer))
    assert no_odcount == 1
    npt.assert_allclose(actual=[np.mean(mean_vals), 
                                np.mean(std_vals)],
                        desired=[1.202, 0.337], atol=1e-2)
    
@lustre_unavail
def test_load_berlin():
    dataset = ReadAeronetSunV3()
    files = dataset.find_in_file_list('*Berlin*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == 'Berlin_FUB.lev30'
    data = dataset.read_file(files[0],
                             vars_to_retrieve=['od550aer'])
    
    test_vars = ['od440aer',
                 'od500aer',
                 'od550aer',
                 'ang4487aer']
    assert all([x in data for x in test_vars])
    
    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])
    
    assert isinstance(data['dtime'][0], np.datetime64)
    t0 = data['dtime'][0]
    
    assert t0 == np.datetime64('2014-07-06T12:00:00')
    
    
    first_vals = [data[var][0] for var in test_vars]
    
    nominal = [0.224297, 0.178662, 0.148119, 1.967039]
    npt.assert_allclose(actual=first_vals, desired=nominal, rtol=TEST_RTOL)
    
    
    
    
if __name__=="__main__":
    
    test_load_berlin()
    aeronetsunv3lev2_subset = make_dataset()
    test_shape_ungridded(aeronetsunv3lev2_subset)