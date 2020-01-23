#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:27:28 2019

@author: jonasg
"""
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
import numpy.testing as npt
from pyaerocom.colocation import colocate_gridded_ungridded
import pytest

def _load_modis6aqua_aod_2010():
    from pyaerocom.io import ReadGridded
    return ReadGridded('MODIS6.aqua').read_var('od550aer',
                                               start=2010,
                                               ts_type='daily')

def _load_aeronet_sunv3():
    from pyaerocom.io import ReadUngridded
    return ReadUngridded().read('AeronetSunV3Lev2.daily', 'od550aer')

@lustre_unavail
@pytest.fixture(scope='module')
def modis_data():
    return _load_modis6aqua_aod_2010()

@lustre_unavail
@pytest.fixture(scope='module')
def aeronet_data():
    return _load_aeronet_sunv3()

def test_modis_data(modis_data):
    data =  modis_data
    assert data.ts_type == 'daily'
    assert str(data.start) == '2010-01-01T00:00:00.000000'
    assert str(data.stop) == '2010-12-31T23:59:59.999999'
    assert len(data.time.points) == 365
    assert data.shape == (365, 180, 360)

def test_colocate_gridded_ungridded_default(modis_data, aeronet_data):
    coldata = colocate_gridded_ungridded(modis_data, aeronet_data)
    assert coldata.ts_type == 'daily'
    
    stats = {'totnum'       : 97455.0, 
             'num_valid'    : 22173.0, 
             'refdata_mean' : 0.20148, 
             'refdata_std': 0.24190694442558214, 
             'data_mean': 0.21707663503434954, 
             'data_std': 0.2640279860471867, 
             'weighted':False,
             'rms': 0.14676859292764524, 
             'R': 0.8371045991138515, 
             'R_spearman': 0.8008437094410961, 
             'R_kendall': 0.6186103268134735, 
             'nmb': 0.0933142471394159, 
             'mnmb': 0.044064426995632636, 
             'fge': 0.4286766659859061, 
             'num_neg_data': 844, 
             'num_neg_refdata': 0, 
             'num_coords_with_data': 267, 
             'num_coords_tot': 267}
    
    stats_calc = coldata.calc_statistics()
    assert len(stats) == len(stats_calc)
    vals = []
    vals_nominal = []
    for key, val in stats_calc.items():
        assert key in stats, key
        vals.append(val)    
        vals_nominal.append(stats[key])
    npt.assert_allclose(vals, vals_nominal, rtol=TEST_RTOL)
        
    
def test_colocate_gridded_ungridded_custom(modis_data, aeronet_data):
    coldata = colocate_gridded_ungridded(
            modis_data, 
            aeronet_data, 
            ts_type='monthly',
            apply_time_resampling_constraints=True,
            colocate_time=True,
            remove_outliers=False)
    
    assert coldata.ts_type == 'monthly'
    
    stats = {'totnum': 3204.0, 
             'num_valid': 1357.0, 
             'refdata_mean': 0.20040808380164812, 
             'refdata_std': 0.18818580038766464, 
             'data_mean': 0.21129443314225607, 
             'data_std': 0.19777726159168757, 
             'weighted':False,
             'rms': 0.08594528034591596, 
             'R': 0.9035961859420195, 
             'R_spearman': 0.8441011217929901, 
             'R_kendall': 0.6733353952628113, 
             'nmb': 0.05703560589497942, 
             'mnmb': 0.036236316494641645, 
             'fge': 0.3085368320318555, 
             'num_neg_data': 16, 
             'num_neg_refdata': 0, 
             'num_coords_with_data': 255, 
             'num_coords_tot': 267}
    
    stats_calc = coldata.calc_statistics()
    assert len(stats) == len(stats_calc)
    vals = []
    vals_nominal = []
    for key, val in stats_calc.items():
        assert key in stats, key
        vals.append(val)
        vals_nominal.append(stats[key])
    npt.assert_allclose(vals, vals_nominal, rtol=TEST_RTOL)
    
if __name__ == '__main__':
    
    import pyaerocom as pya
    sat = _load_modis6aqua_aod_2010()
    obs = _load_aeronet_sunv3()
    
    test_colocate_gridded_ungridded_default(sat, obs)
    test_colocate_gridded_ungridded_custom(sat, obs)