#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy as np
from pandas import Timestamp
from pyaerocom import ColocatedData
from pyaerocom.conftest import TESTDATADIR, CHECK_PATHS

EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])

def test_meta_access_filename():
    name = 'absc550aer_REF-EBAS-Lev3_MOD-CAM5-ATRAS_20100101_20101231_daily_WORLD-noMOUNTAINS.nc'

    meta = {'var_name': 'absc550aer',
            'ts_type': 'daily',
            'filter_name': 'WORLD-noMOUNTAINS',
            'start': Timestamp('2010-01-01 00:00:00'),
            'stop': Timestamp('2010-12-31 00:00:00'),
            'data_source': ['EBAS-Lev3', 'CAM5-ATRAS']}
    for k, v in ColocatedData.get_meta_from_filename(name).items():
        assert meta[k] == v

def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(str(EXAMPLE_FILE))
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded




if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
