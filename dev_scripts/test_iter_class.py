#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:49:27 2018

@author: jonasg
"""
import numpy as np

class Series(object):
    def __init__(self, low, high, num):
        
        self.data = np.linspace(low, high, num)
        self.index = 0
        self.num = num
    
    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.num:
            self.index=0
            raise StopIteration()
        else:
            self.index += 1
            return self.data[self.index-1]
        
    def __getitem__(self, index):
        return self.data[index]
    
s = Series(100, 150, 30)    
#print(list(n_list))

for item in s:
    print(item)
print(s.index)