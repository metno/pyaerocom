#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:27:28 2019

@author: jonasg
"""
import pytest
import numpy as np
import numpy.testing as npt

from pyaerocom.conftest import (TEST_RTOL, lustre_unavail, testdata_unavail)
from pyaerocom.colocation import colocate_gridded_ungridded
from pyaerocom.colocateddata import ColocatedData

@testdata_unavail
@pytest.mark.parametrize('addargs,ts_type,shape,obsmean,modmean',[
    (dict(), 
     'monthly', (2,12,8), 0.315930,0.275671),
    (dict(var_ref_outlier_ranges={'od550aer':[0.1,0.5]},
          var_outlier_ranges={'od550aer':[0.1,0.2]}),
     'monthly', (2,12,8), 0.227333,0.275671),
    (dict(apply_time_resampling_constraints=False), 
     'monthly', (2,12,8), 0.316924,0.275671),
    (dict(filter_name='WORLD-wMOUNTAINS'), 
     'monthly', (2,12,11), 0.269707, 0.243861),
    (dict(use_climatology_ref=True), 
     'monthly', (2,12,13), 0.302636, 0.234147)
    ])
def test_colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset, 
                                    addargs, ts_type, shape,
                                    obsmean, modmean):
    coldata = colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset, 
                                         **addargs)
    
    assert isinstance(coldata, ColocatedData)    
    assert coldata.ts_type == ts_type
    assert coldata.shape == shape 
    
    means = [np.nanmean(coldata.data.data[0]),
             np.nanmean(coldata.data.data[1])]
    
    npt.assert_allclose(means, [obsmean, modmean], rtol=TEST_RTOL)
    
@pytest.mark.skip(reason='No fixture for gridded observation data available yet')
def test_colocate_gridded_gridded(mod, obs, addargs, **kwargs):
    pass
if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
    