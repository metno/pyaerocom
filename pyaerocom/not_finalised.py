#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:42:44 2020

@author: jonasg
"""
import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom import const

def correct_model_stp_coldata(coldata, p0=None, t0=273, inplace=False):
    """Correct modeldata in colocated data object to STP conditions
    
    Note
    ----
    BETA version, quite unelegant coded (at 8pm 3 weeks before IPCC deadline), 
    but should do the job for 2010 monthly colocated data files (AND NOTHING
    ELSE)!
    
    """
    if coldata.ndim != 3:
        raise NotImplementedError('Can only handle 3D coldata so far...')
    elif not coldata.ts_type == 'monthly' or not len(coldata.time)==12:
        raise NotImplementedError('Can only handle monthly colocated data files '
                                  'so far (since ERA5 temps are only available) '
                                  'in monthly resolution')
    startyr = pd.Timestamp(coldata.start).year
    stopyr = pd.Timestamp(coldata.stop).year
    if not all([x==2010 for x in (startyr, stopyr)]):
        raise NotImplementedError('Can only handle 2010 monthly data so far')
        
    if not inplace:
        coldata = coldata.copy()
    temp = xr.open_dataset(const.ERA5_SURFTEMP_FILE)['t2m']
    from geonum.atmosphere import pressure
    arr = coldata.data
    
    coords = zip(arr.latitude.values, arr.longitude.values, 
                 arr.altitude.values, arr.station_name.values)
    if p0 is None:
        p0 = pressure() #STD conditions sea level
    const.logger.info('Correcting model data in ColocatedData instance to STP')
    cfacs = []
    meantemps = []
    mintemps = []
    maxtemps =[]
    ps = []
    for i, (lat, lon, alt, name) in enumerate(coords):
        const.logger.info(name, ', Lat', lat, ', Lon', lon)
        p = pressure(alt)
        const.logger.info('Alt', alt)
        const.logger.info('P=', p/100, 'hPa')
        
        ps.append(p/100)
        
        temps = temp.sel(latitude=lat, longitude=lon, method='nearest').data
        
        meantemps.append(temps.mean())
        mintemps.append(temps.min())
        maxtemps.append(temps.min())
        
        if not len(temps) == len(arr.time):
            raise NotImplementedError('Check timestamps')
        const.logger.info('Mean Temp: ', temps.mean() - t0, ' C')
        
        corrfacs = (p0 / p) * (temps / t0)
        
        const.logger.info('Corr fac:', corrfacs.mean(), '+/-', corrfacs.std())
        
        cfacs.append(corrfacs.mean())
    
        #mularr = xr.DataArray(corrfacs)
        
        if not arr.station_name.values[i] == name:
            raise Exception
        elif not arr.dims[1] == 'time':
            raise Exception
    # =============================================================================
    #     const.logger.info(corrfacs)
    #     const.logger.info('Before', arr[1, :, i].data)
    #     corrfacs[0] = 1
    # =============================================================================
        arr[1, :, i] *= corrfacs
        #const.logger.info('After', arr[1, :, i].data)
    cfacs = np.asarray(cfacs)
    
    const.logger.info('Min: ', cfacs.min())
    const.logger.info('Mean: ', cfacs.mean())
    const.logger.info('Max: ', cfacs.max())
    coldata.data.attrs['Model_STP_corr'] = True
    
    newcoords = dict(pres=('station_name', ps),
                     temp_mean=('station_name', meantemps), 
                     temp_min=('station_name', mintemps),
                     temp_max=('station_name', maxtemps),
                     stp_corrfac_mean=('station_name', cfacs))
                 
    coldata.data = coldata.data.assign_coords(newcoords)
    
    info_str = ('Correction factors to convert model data from ambient to '
                'STP were computed using corrfac=(p0/p)*(T/T0) with T0=273K '
                'and p0=1013 hPa and p is the pressure at the station location '
                '(which was computed assuming a standard atmosphere and using '
                'the station altitude) and T is the 2m surface temperature at '
                'the station, applied on a monthly basis and estimated using '
                'ERA5 data')
                
    coldata.data['pres'].attrs['units'] = 'hPa'
    coldata.data['temp_mean'].attrs['units'] = 'K'
    coldata.data['temp_min'].attrs['units'] = 'K'
    coldata.data['temp_max'].attrs['units'] = 'K'
    
    coldata.data.attrs['Model_STP_corr'] = True
    coldata.data.attrs['Model_STP_corr_info'] = info_str
    return coldata