#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:18:21 2018

@author: jonasg
"""

from pandas import Series
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt

class MySeries(Series):
    def __init__(self, *args, **kwargs):
        #super(MySeries, self).__init__(*args, **kwargs)
        pass

if __name__=="__main__":
    plt.close("all")    
    ts = np.datetime64("2014") + np.arange(0, 100, 1).astype("timedelta64[D]")
    vals = np.arange(0,100,1)
    
    
    s = MySeries(vals, ts)
    s.plot()