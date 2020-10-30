#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
def _load_coldata_tm5_aeronet_from_scratch(file_path):
    from xarray import open_dataarray
    from pyaerocom import ColocatedData
    arr = open_dataarray(file_path)
    if '_min_num_obs' in arr.attrs:
        info = {}
        for val in arr.attrs['_min_num_obs'].split(';')[:-1]:
            to, fr, num = val.split(',')
            if not to in info:
                info[to] = {}
            if not fr in info[to]:
                info[to][fr] = {}
            info[to][fr] = int(num)
        arr.attrs['min_num_obs'] = info
    cd = ColocatedData()
    cd.data = arr
    return cd