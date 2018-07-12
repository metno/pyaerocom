#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:03:57 2018

@author: jonasg
"""

import numpy as np

### PART 1
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
    

### PART 2
class NonExtendableArray:
    CHUNKSIZE=200
    LEN = 10
    def __init__(self):
        self.arr = np.empty(self.LEN)
    
    def set_tryexcept(self, idx, value):
        try:
            self.arr[idx] = value
        except IndexError:
            self.add_chunk()
            self.arr[idx] = value
            
    def set_checksize(self, idx, value):
        if idx >= self.LEN:
            self.add_chunk()
        self.arr[idx] = value

    def add_chunk(self):
        chunk = np.empty(self.CHUNKSIZE)*np.nan
        self.arr = np.append(self.arr, chunk)
        self.LEN += self.CHUNKSIZE

def test_tryexcept(endnum=1000):
    a = NonExtendableArray()    
    for k in range(1000):
        a.set_tryexcept(k, 42)
    return a

def test_checksize(endnum=1000):
    a = NonExtendableArray()    
    for k in range(1000):
        a.set_checksize(k, 42)
    return a
        
a = test_tryexcept()
a1 = test_checksize()