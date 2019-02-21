#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy.testing as npt
from pyaerocom import UngriddedData, const


def test_init_shape():
    npt.assert_array_equal(UngriddedData().shape, (10000, 12))
    
    d1 = UngriddedData(num_points=2, add_cols=['bla', 'blub'])
    npt.assert_array_equal(d1.shape, (2, 14))
    
    d1.add_chunk(1112)
    
    npt.assert_array_equal(d1.shape, (1114, 14))


    
if __name__=="__main__":
    test_init_shape()
    