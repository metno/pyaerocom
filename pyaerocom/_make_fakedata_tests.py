#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 09:03:59 2021

@author: jonasg
"""
import pytest, os
import numpy as np
import pandas as pd
import xarray as xr

TS_TYPE_FREQ = dict(
    monthly = 'MS',

    )
def check_create_modeloutdir(model_id, modoutbase):
    outdir = os.path.join(modoutbase, model_id, 'renamed')
    if not os.path.exists(outdir):
        os.makedirs(outdir, exist_ok=True)
    return outdir


def create_timedim(start, end, freq):
    return pd.date_range(start=start, end=end, freq=freq)

outbase = os.path.join(os.path.expanduser('~'), 'MyPyaerocom/data/fakedata/')

if not os.path.exists(outbase):
    raise FileNotFoundError()

modoutbase = os.path.join(outbase, 'modeldata')
obsoutbase = os.path.join(outbase, 'obsdata')

if not os.path.exists(modoutbase):
    os.mkdir(modoutbase)

if not os.path.exists(obsoutbase):
    os.mkdir(obsoutbase)

### 3monthly modeldataset of AOD

MODEL_ID = 'FAKEDATA-met2018_TEST-ONE'
OUTDIR = check_create_modeloutdir(MODEL_ID, modoutbase)

ts_type = 'monthly'
start = '2018-01-01 00:00'
stop = '2018-12-31 23:59:59'

var_name = 'od550aer'
var_units = '1'
vert_code = 'Column'
lat0, lat1, latres = 30, 60, 5
lon0, lon1, lonres = -10, 20, 4

time = create_timedim(start=start,
                      end=stop,
                      freq=TS_TYPE_FREQ[ts_type])

lats = np.arange(lat0, lat1, latres)
lons = np.arange(lon0, lon1, lonres)

numlons, numlats, numtime = len(lons), len(lats), len(time)

data = np.ones((numtime, numlats, numlons))

arr = xr.DataArray(data, dims=['time','lat','lon'],coords=[time, lats, lons])
arr.lat.attrs.update(dict(
    var_name='lat',
    standard_name='latitude',
    circular=False,
    units='degrees'
    ))


raise Exception

latdim.arrs.update(dict(

    ))


londim = iris.coords.DimCoord(lons, var_name='lon',
                              standard_name='longitude',
                              circular=False,
                              units='degrees')

timedim = iris.coords.DimCoord(timesteps,standard_name='time',
                               var_name='time', units=freqstr)

latdim.guess_bounds()
londim.guess_bounds()


dummy = iris.cube.Cube(data)

dummy.add_dim_coord(timedim, 0)
dummy.add_dim_coord(latdim, 1)
dummy.add_dim_coord(londim, 2)

dummy.var_name = var_name
dummy.attributes['ts_type'] = 'daily'
dummy.units = '1'

print(dummy)



arr = xr.DataArray(data)