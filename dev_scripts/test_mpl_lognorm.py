#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 08:49:37 2018

@author: jonasg
"""

from matplotlib.colors import LogNorm
import pyaerocom

if __name__=="__main__":
    
    data = pyaerocom.GriddedData()._init_testdata_default()
    