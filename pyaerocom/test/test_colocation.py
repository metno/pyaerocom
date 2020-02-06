#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:27:28 2019

@author: jonasg
"""
import pytest
import numpy as np
import numpy.testing as npt

from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.colocation import colocate_gridded_ungridded
from pyaerocom.io.test.test_read_aeronet_sunv3 import aeronetsunv3lev2_subset
from pyaerocom.test.test_griddeddata import data_tm5

@lustre_unavail
def test_colocate_gridded_ungridded_default(data_tm5, aeronetsunv3lev2_subset):
    coldata = colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset)
    assert coldata.ts_type == 'monthly'
    
    stats = {'totnum': 48.0, 'num_valid': 15.0, 
             'refdata_mean': 0.09317085075736015, 
             'refdata_std': 0.0418982083785594, 
             'data_mean': 0.10662878553072612, 
             'data_std': 0.04734850235431848, 
             'weighted': False, 
             'rms': 0.026635879341186646, 
             'R': 0.8743210058158878, 
             'R_spearman': 0.8785714285714284, 
             'R_kendall': 0.7333333333333334, 
             'nmb': 0.14444361797676125, 
             'mnmb': 0.12380017801579468, 
             'fge': 0.23771937356434453, 
             'num_neg_data': 0, 
             'num_neg_refdata': 0, 
             'num_coords_with_data': 3, 
             'num_coords_tot': 4}
    
    stats_calc = coldata.calc_statistics()
    assert len(stats) == len(stats_calc)
    vals = []
    vals_nominal = []
    for key, val in stats_calc.items():
        assert key in stats, key
        vals.append(val)    
        vals_nominal.append(stats[key])
    npt.assert_allclose(vals, vals_nominal, rtol=TEST_RTOL)
        
 
@lustre_unavail
def test_colocate_gridded_ungridded_custom(data_tm5, aeronetsunv3lev2_subset):
    coldata = colocate_gridded_ungridded(
            data_tm5, 
            aeronetsunv3lev2_subset,
            ts_type='yearly',
            use_climatology_ref=True,
            apply_time_resampling_constraints=True,
            colocate_time=True,
            remove_outliers=False)
    
    assert coldata.ts_type == 'yearly'
    assert coldata.shape == (2, 1, 6)
    
    stats = {'totnum': 6.0, 'num_valid': 4.0, 'refdata_mean': 0.14714656748980037, 
             'refdata_std': 0.05836215522825422, 'data_mean': 0.13612345532913292, 
             'data_std': 0.03900864539522903, 'weighted': False, 
             'rms': 0.05254246921514237, 'R': 0.5026321577103197, 
             'R_spearman': 0.39999999999999997, 'R_kendall': 0.3333333333333334, 
             'nmb': -0.07491246550098105, 'mnmb': -0.03453627649127072, 
             'fge': 0.24068195719824653, 'num_neg_data': 0, 
             'num_neg_refdata': 0, 'num_coords_with_data': 4, 'num_coords_tot': 6}
    
    stats_calc = coldata.calc_statistics(min_num_valid=4)
    assert len(stats) == len(stats_calc)
    vals = []
    vals_nominal = []
    for key, val in stats_calc.items():
        assert key in stats, key
        vals.append(val)
        vals_nominal.append(stats[key])
    npt.assert_allclose(vals, vals_nominal, rtol=TEST_RTOL)
    
if __name__ == '__main__':
    
    pytest.main(['./test_colocation.py'])
    