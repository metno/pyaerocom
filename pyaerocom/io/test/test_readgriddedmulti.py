#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

# TODO: Docstrings
import pytest
import numpy.testing as npt
import numpy as np
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.io.readgridded import ReadGriddedMulti

MODELS = ["AATSR_SU_v4.3", "CAM5.3-Oslo_CTRL2016", 
          'ECHAM6-SALSA_AP3-CTRL2015']
TEST_VARS = ["od550aer", "od550dust"]

@lustre_unavail
@pytest.fixture(scope='module')
def dataset():
    return ReadGriddedMulti(MODELS, '2010','2011')

@lustre_unavail    
def test_info_available(dataset):    
    ids_nominal = MODELS
    vars_nominal = [['abs550aer', 'ang4487aer', 'od550aer', 'od550dust', 
                    'od550erraer', 'od550gt1aer', 'od550lt1aer'],
                    ['abs550aer', 'deltaz3d', 'humidity3d', 'od440aer', 
                     'od550aer', 'od550aer3d', 'od550aerh2o', 'od550dryaer', 
                     'od550dust', 'od550lt1aer', 'od870aer'],
                    ['depbc', 'depdust', 'depoa', 'depso4', 'depss', 'emibc', 
                     'emidms', 'emidust', 'emiso2', 'emiso4', 'emiss', 'emivoc', 
                     'emivoct', 'loadbc', 'loaddust', 'loadoa', 'loadso4', 
                     'loadss', 'od550aer', 'od550bc', 'od550dust', 'od550oa', 
                     'od550so4', 'od550ss', 'sconcbc', 'sconcdust', 'sconcoa', 
                     'sconcso4', 'sconcss']]
    years_nominal = [[2010, 2011, 2012],
                     [2010],
                     [2010]]
    
    for i, model in enumerate(MODELS):
        d = dataset[model]
        assert d.name == ids_nominal[i]
        npt.assert_array_equal(d.vars, vars_nominal[i])
        npt.assert_array_equal(d.years, years_nominal[i])

@lustre_unavail        
def test_read_vars(dataset):
    result = dataset.read(TEST_VARS, ts_type="daily",
                          flex_ts_type=False)
    
    npt.assert_array_equal([2,2,0], [len(x.data) for x in result.values()])
    dataset["ECHAM6-SALSA_AP3-CTRL2015"].read(TEST_VARS, ts_type="monthly")
    
    npt.assert_array_equal([2,2,2], [len(x.data) for x in dataset.results.values()])

@lustre_unavail                
def test_data_available(dataset):
    npt.assert_array_equal(MODELS, [k for k in dataset.results.keys()])
    arr = []
    for model, result in dataset.results.items():
        for species, data in result.data.items():
            row = []
            row.extend(data.shape)
            row.append(data[0].mean())
            row.append(data[0].std())
            arr.append(row)
    arr = np.asarray(arr)
    nominal = np.asarray([[3.66000000e+02, 1.80000000e+02, 3.60000000e+02, 
                           1.18452743e-01, 1.02940924e-01],
                          [3.66000000e+02, 1.80000000e+02, 3.60000000e+02, 
                           1.95622779e-02, 3.41552608e-02],
                          [3.65000000e+02, 1.92000000e+02, 2.88000000e+02, 
                           9.24114585e-02, 1.36086926e-01],
                          [3.65000000e+02, 1.92000000e+02, 2.88000000e+02, 
                           1.65812690e-02, 7.40822107e-02],
                          [1.20000000e+01, 9.60000000e+01, 1.92000000e+02, 
                           1.34139806e-01, 1.07606672e-01],
                          [1.20000000e+01, 9.60000000e+01, 1.92000000e+02, 
                           5.48036816e-03, 1.74955484e-02]])
    npt.assert_allclose(actual=arr, desired=nominal, rtol=TEST_RTOL)
    
    
if __name__=="__main__":
    d = dataset()
    test_info_available(d)
    test_read_vars(d)
    arr= test_data_available(d)
