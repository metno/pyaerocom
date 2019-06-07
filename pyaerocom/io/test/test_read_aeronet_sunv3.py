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
    assert aeronetsunv3lev2_subset.shape == (60950, 12)
    
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
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.2160,
                                0.1905,
                                0.1863,
                                0.1338,
                                0.1195,
                                0.6229,
                                0.2806,
                                0.1398,
                                0.0963,
                                0.1005,
                                0.0557,
                                0.2787,
                                0.3630,
                                0.1337,
                                0.1626,
                                0.1172,
                                0.1377,
                                0.1215,
                                0.1928,
                                0.1542,
                                0.6151,
                                0.0862,
                                0.0874,
                                0.4165], atol=1e-4)
    npt.assert_allclose(actual=std_vals,
                        desired=[0.2193,
                                0.0258,
                                0.1893,
                                0.0263,
                                0.0769,
                                0.3546,
                                0.2296,
                                0.1016,
                                0.0929,
                                0.1129,
                                0.0403,
                                0.2046,
                                0.2612,
                                0.1186,
                                0.1531,
                                0.0595,
                                0.1033,
                                0.2190,
                                0.1457,
                                0.1392,
                                0.2820,
                                0.0442,
                                0.0525,
                                0.3158], atol=1e-4)
    
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
    npt.assert_allclose(actual=mean_vals,
                        desired=[1.7335,
1.5850,
0.9833,
1.6073,
1.1624,
1.7254,
1.2122,
1.4659,
1.0885,
1.2963,
1.5055,
0.9200,
1.5132,
1.0421,
0.9933,
1.4937,
1.1399,
1.3020,
0.8579,
0.7132,
1.0919,
1.3674,
1.6204,
0.3195,
0.8972,
0.4446,
1.3451,
1.2527], atol=1e-4)
    npt.assert_allclose(actual=std_vals,
                        desired=[0.4569,
0.1823,
0.3688,
0.2934,
0.3098,
0.1209,
0.3129,
0.3415,
0.3388,
0.2566,
0.3059,
0.4227,
0.3322,
0.4465,
0.3190,
0.3830,
0.3317,
0.3894,
0.5120,
0.3539,
0.4207,
0.3339,
0.2269,
0.3255,
0.4177,
0.3155,
0.3509,
0.2815], atol=1e-4)
    
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
    [print('{:.4f},'.format(x)) for x in mean_vals]
    print()
    [print('{:.4f},'.format(x)) for x in std_vals]