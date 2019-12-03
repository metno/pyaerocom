#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:03:55 2019

@author: hannas
"""

import pyaerocom as pya
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail

import numpy as np

VAR = 'od550aer'
YEAR = 2010
FREQ = 'daily'
MODEL = 'NorESM2-met2010_AP3-CTRL'
SATELITE = 'MODIS6.1aqua'

def test_filter_attributes():
    f = pya.Filter('WORLD-noMOUNTAINS-LAND')
    assert f.land_ocn == 'LAND'
    assert f.region_name == 'WORLD'
    assert f.name == 'WORLD-noMOUNTAINS-LAND'
    assert not f._region.is_htap

@lustre_unavail
def test_filter_griddeddata():
    model = pya.io.ReadGridded(data_id=SATELITE).read_var('od550aer', 
                                                          ts_type='daily', 
                                                          start = 2010)
    f1 = pya.filter.Filter('WORLD-noMOUNTAINS-LAND')
    f2 = pya.filter.Filter('WORLD-noMOUNTAINS-OCN')
    
    m_land = f1.apply(model)
    m_ocn  = f2.apply(model)
    
    #a = np.abs(np.nansum(model.cube.data.data))
    #b = np.abs(np.nansum(m_ocn.cube.data.data))
    #c = np.abs(np.nansum(m_land.cube.data.data))
    
    #print(" a = {} = b + c = {} ".format(a, b+c))
    assert np.abs(np.nanmean(m_land.cube.data.data) + 6939.1149583639135) < 0.00001
    assert np.abs(np.nanmean(m_ocn.cube.data.data) + 5160.469329580611) < 0.00001   
    
    return

@lustre_unavail
def test_filter_colocateddata():
    model = pya.io.ReadGridded(data_id=MODEL).read_var('od550aer', 
                                                       ts_type='daily', 
                                                       start = 2010)
    
    sat = pya.io.ReadGridded(data_id=SATELITE).read_var('od550aer', 
                                                        ts_type='daily', 
                                                        start = 2010)
    
    data_coloc = pya.colocation.colocate_gridded_gridded(model, 
                                                         sat, 
                                                         ts_type='monthly', 
                                                         filter_name='WORLD-noMOUNTAINS-OCN')

    assert data_coloc.data.sum().values - 111340.31777193633 < 0.001

@lustre_unavail
def test_filter_ungriddeddata():
    obs_id = 'AeronetSunV2Lev2.daily'
    obs_reader = pya.io.ReadUngridded(obs_id, 'od500aer')
    obs_data = obs_reader.read()
    
    stations = 154
    f = pya.Filter(name = 'EUROPE-noMOUNTAINS')
    data = f.apply(obs_data) 
    gg = data.to_station_data_all()
    assert len(gg['station_name']) + len(gg['failed']) == stations

if __name__ == '__main__':
    test_filter_colocateddata()