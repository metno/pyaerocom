#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:36:15 2019

@author: jonasg
"""
from pyaerocom import geodesy
import numpy.testing as npt

def test_haversine():
    npt.assert_allclose(geodesy.haversine(0, 15, 0, 16), 111.20, atol=0.1)
    
def test_is_within_radius_km():
    assert geodesy.is_within_radius_km(0, 15, 0, 16, 1000, 111.2)
    
if __name__ == '__main__':

    test_haversine()
    test_is_within_radius_km()