#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import numpy.testing as npt
import numpy as np
import os
from pyaerocom.conftest import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
    
@lustre_unavail
def test_load_berlin_AeroSdaV2L2D():
    reader = ReadAeronetSdaV3()
    files = reader.find_in_file_list('*Berlin*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == 'Berlin_FUB.lev30', files[0]

    test_vars = ['od500gt1aer',
                 'od500lt1aer',
                 'od500aer',
                 'ang4487aer',
                 'od550aer',
                 'od550gt1aer',
                 'od550lt1aer']
    
    data = reader.read_file(files[0],
                            vars_to_retrieve=test_vars)                
    
    assert all([x in data for x in test_vars])
    
    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])
    
    assert isinstance(data['dtime'][0], np.datetime64)
    assert data['dtime'][0] == np.datetime64('2014-07-06T12:00:00'), data['dtime'][0]
    
    vals = []
    # test first 100 values (this ensures that data updates do not destroy
    # this test, since they should add new measurements at the end of the 
    # period in most cases)
    for var in test_vars:
        
        vals.append(np.nanmean(data[var][:100]))
    print(vals)
    npt.assert_allclose(vals, 
                        [0.03778931, 0.15039492, 0.18818413, 1.3409827399999998, 
                         0.1649781239550986, 0.033531405280829374, 
                         0.13144680608533071], 
                        rtol=TEST_RTOL)
    
if __name__=="__main__":
    test_load_berlin_AeroSdaV2L2D()    
    