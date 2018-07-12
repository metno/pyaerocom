#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 09:15:11 2018

@author: jonasg
"""

import numpy as np

l = list(np.arange(10))

pop_uneven = []
for idx, num in l:
    if num%2:
        pop_uneven.append(idx)
        
uneven = []