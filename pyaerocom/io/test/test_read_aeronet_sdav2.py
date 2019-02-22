#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import numpy.testing as npt
import numpy as np
import os
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
    
@lustre_unavail
def test_load_berlin_AeroSdaV2L2D():
    reader = ReadAeronetSdaV2()
    files = reader.find_in_file_list('*Berlin*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == '920801_180519_Berlin_FUB.ONEILL_20'

    test_vars = ['od870aer',
                 'od675aer',
                 'od667aer',
                 'od555aer',
                 'od551aer',
                 'od532aer',
                 'od531aer',
                 'od500aer_input',
                 'od490aer',
                 'od443aer',
                 'od440aer',
                 'od412aer',
                 'od380aer',
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
    assert data['dtime'][0] == np.datetime64('2014-07-06T00:00:00')
    
    vals = []
    for var in test_vars:
        
        vals.append([data[var].mean(), data[var].std()])
    
    npt.assert_allclose(vals, [[0.0671392659574468, 0.04104413045022494], 
                               [0.09650303546099291, 0.06181304333693019], 
                               [-999.0, 0.0], 
                             [-999.0, 0.0], 
                             [-999.0, 0.0], 
                             [-999.0, 0.0], 
                             [-999.0, 0.0], 
                             [0.15719042198581562, 0.09911926067054333], 
                             [-999.0, 0.0], 
                             [-999.0, 0.0], 
                             [0.1873593581560284, 0.11626762295798776], 
                             [-999.0, 0.0], 
                             [0.2310559893617021, 0.1389056396199096], 
                             [1.5027900015754372, 0.4624822418227316], 
                             [0.1338938495016503, 0.08439866119497562], 
                             [0.02333982521802314, 0.016413010680297286], 
                             [0.11055405137562464, 0.08244321868457247]], 
                        rtol=TEST_RTOL)
    
if __name__=="__main__":
    test_load_berlin_AeroSdaV2L2D()
        
    