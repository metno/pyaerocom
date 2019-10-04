#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
from pyaerocom import units_helpers as helpers

def test_unit_conversion_fac():
    assert helpers.unit_conversion_fac('m-1', '1/Mm') == 1e6
    
    
    
    
    
    
    
    
    