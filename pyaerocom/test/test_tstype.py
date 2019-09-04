#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
from pyaerocom.tstype import TsType

def test_basic_operators():
    monthly = TsType('monthly')
    yearly = TsType('yearly')
    daily = TsType('daily')
    
    assert monthly < daily
    assert monthly <= daily
    assert monthly != daily
    assert yearly < daily
    assert not (yearly == daily)
    assert monthly > yearly
    assert monthly >= yearly
    
def test_basic_operators_pandas():
    monthly = TsType('MS')
    yearly = TsType('AS')
    daily = TsType('D')
    
    assert monthly < daily
    assert monthly <= daily
    assert monthly != daily
    assert yearly < daily
    assert not (yearly == daily)
    assert monthly > yearly
    assert monthly >= yearly

if __name__=="__main__":
    test_basic_operators()
    test_basic_operators_pandas()    