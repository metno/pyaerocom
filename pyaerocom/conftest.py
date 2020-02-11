#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
import pytest
from pyaerocom.test.settings import lustre_unavail
from pyaerocom import GriddedData
from pyaerocom.io import ReadAasEtal
from pyaerocom.io import ReadAeronetSunV3
from pyaerocom.io import ReadEbas

MODELFILE = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/TM5_AP3-CTRL2016/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc'
TEST_VARS = ['od550aer', 'ang4487aer']
### fixtures

# Example GriddedData object (TM5 model)
@lustre_unavail
@pytest.fixture(scope='session')
def data_tm5():
    data = GriddedData(MODELFILE)
    return data



@lustre_unavail
@pytest.fixture(scope='session')
def aasetal_data():
    reader = ReadAasEtal()
    # that's quite time consuming, so keep it for possible usage in other 
    # tests
    return reader.read()  # read all variables


@lustre_unavail
@pytest.fixture(scope='session')
def aeronetsunv3lev2_subset():
    r = ReadAeronetSunV3()
    #return r.read(vars_to_retrieve=TEST_VARS)
    return r.read(file_pattern='Tu*', 
                  vars_to_retrieve=TEST_VARS)


@pytest.fixture(scope='module')
def data_scat_jungfraujoch():
    r = ReadEbas()
    return r.read('scatc550aer', station_names='Jungfrau*')