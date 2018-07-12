#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:03:57 2018

@author: jonasg
"""

import numpy as np

class ExtendableArray:
    CHUNKSIZE=20
    ROWNO=100
    COLNO = 10
    def __init__(self):
        self.arr = np.empty([self.ROWNO, self.COLNO])
        self.index = 0
    
    def _add_chunk(self):
        chunk = np.empty([self.CHUNKSIZE, self.COLNO])*np.nan
        self.arr = np.append(self.arr, chunk, axis=0)
        self.ROWNO += self.CHUNKSIZE
        print("adding chunk, new array size ({})".format(self.arr.shape))
        
    def __setitem__(self, key, val):
        if self.index >= self.ROWNO:
            self._add_chunk()
        self.arr[key] = val
        self.index += 1
        
arr = ExtendableArray()

for k in range(121):
    arr[k] = np.ones(10)*k
        