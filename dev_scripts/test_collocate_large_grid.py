#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 11:23:15 2018

@author: jonasg
"""

import pyaerocom

start=2000
stop=2018

var = "od550aer"

ts_type = "daily"

model_id = "ECMWF_CAMS_REAN"
obs_id = pyaerocom.const.AERONET_SUN_V2L2_AOD_DAILY_NAME


model_io = pyaerocom.io.ReadGridded(model_id, start=start, stop=stop)

model_io.read_var(var)
model_data = model_io["od550aer"]

go = False


if go:
    obs_data = pyaerocom.io.readungridded.ReadUngridded(obs_id, verbose=True)
    obs_data.read()
    
    lons, lats = obs_data.longitude, obs_data.latitude
    
    model_data.interpolate(longitude=lons, latitude=lats)