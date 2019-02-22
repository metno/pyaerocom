#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level test methods that check EBAS time series data for selected stations
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy.testing as npt
from pyaerocom.test.settings import lustre_unavail
from pyaerocom.io import ReadEbas

@pytest.fixture(scope='module')
def data_scat_jungfraujoch():
    r = ReadEbas()
    return r.read('scatc550aer', station_names='Jungfrau*')

@pytest.mark.skip
@lustre_unavail
def test_assert_msg():
    assert 42==True, 'apparently, 42 is not True, but it should be'
    
@lustre_unavail   
def test_scat_jungfraujoch(data_scat_jungfraujoch):
    
    data = data_scat_jungfraujoch
    assert 'EBASMC' in data.data_revision
    assert data.data_revision['EBASMC'] == '20190115'
    assert data.shape == (227928, 12)
    
if __name__=="__main__":
    r = ReadEbas()
    data = r.read('scatc550aer', station_names='Jungfrau*')
    
    stat = data.to_station_data('Jung*')
    stat.plot_timeseries('scatc550aer')