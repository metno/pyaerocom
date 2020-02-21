#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:03:55 2019

@author: hannas
"""
import pytest
import numpy as np

from pyaerocom.filter import Filter
from pyaerocom.conftest import lustre_unavail, testdata_unavail

def test_Filter_init():
    assert Filter('EUROPE').name == 'EUROPE-wMOUNTAINS'
    assert Filter('noMOUNTAINS-OCN-NAMERICA').name == 'NAMERICA-noMOUNTAINS-OCN'
    
def test_filter_attributes():
    f = Filter('WORLD-noMOUNTAINS-LAND')
    assert f.land_ocn == 'LAND'
    assert f.region_name == 'WORLD'
    assert f.name == 'WORLD-noMOUNTAINS-LAND'
    assert not f.region.is_htap
    

@testdata_unavail
@pytest.mark.parametrize('filter_name, mean',[
    ('EUROPE-noMOUNTAINS-LAND', 0.16616775),
    ('EUROPE-noMOUNTAINS-OCN', 0.1314668),
    ('EUROPE', 0.13605888)
    ])
def test_filter_griddeddata(data_tm5, filter_name, mean):
    
    model = data_tm5.copy()

    f = Filter(filter_name) # europe only land

    subset = f.apply(model)
    np.testing.assert_allclose(np.nanmean(subset.cube.data), mean)
    
@lustre_unavail
def test_filter_ungriddeddata(aeronetsunv3lev2_subset):
    
    obs_data = aeronetsunv3lev2_subset
    
    f1 = Filter(name = 'NAMERICA-noMOUNTAINS')
    f2 = Filter(name = 'NAMERICA-noMOUNTAINS-OCN')
    f3 = Filter(name = 'NAMERICA-noMOUNTAINS-LAND')

    #gg = data.to_station_data_all()
    assert len(f1.apply(obs_data).unique_station_names) == 2
    try:
        f2.apply(obs_data).unique_station_names
    except Exception as e:
        from pyaerocom.exceptions import DataExtractionError
        assert isinstance(e, DataExtractionError)
    assert len(f3(obs_data).unique_station_names) == 2
    
    
@lustre_unavail
def test_filter_colocateddata():
    pass
# =============================================================================
#     data_coloc = pya.colocation.colocate_gridded_gridded(model, 
#                                                          sat, 
#                                                          ts_type='monthly', 
#                                                          filter_name='WORLD-noMOUNTAINS-OCN')
# 
#     assert data_coloc.data.sum().values - 111340.31777193633 < 0.001
# =============================================================================

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)