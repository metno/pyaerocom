#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:36:24 2019

@author: jonasg
"""
import numpy as np
from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes
import pandas as pd
from pyaerocom import const

#SEASONS = ['spring','summer','autumn','winter','all']

SEASONS = {'spring'     : [3,4,5],
           'summer'     : [6,7,8],
           'autumn'     : [9,10,11],
           'winter'     : [12, 1, 2]}

SEASON_CODES = {'spring'     : 'MAM',
                'summer'     : 'JJA',
                'autumn'     : 'SON',
                'winter'     : 'DJF'}

def _init_trends_result_dict(start_yr):
    keys = ['pval', 'm', 'm_err', 
            'n', 'y_mean', 'y_min', 'y_max', 'coverage',
            'slp', 'slp_err', 'reg0', 't0', # data specific
            'slp_{}'.format(start_yr), # period specific
            'slp_{}_err'.format(start_yr), # period specific
            'reg0_{}'.format(start_yr) # period specific
            ]
    return dict.fromkeys(keys)

def _compute_trend_error(m, m_err, v0, v0_err):
    """Computes error of trend estimate using gaussian error propagation
    
    The (normalised) trend is computed as T = m / v0
    
    where m denotes the slope of a regression line and v0 denotes the 
    normalistation value. This method computes the uncertainty of T (delta_T)
    using gaussian error propagation of uncertainties accompanying m and v0.
    
    Parameters
    ----------
    m : float
        slope in units of <U> yr-1 (where <U> denotes the unit of the data).
        (m -> "montant").
    m_err : float
        slope error (same unit as `m`)
    v0 : float
        normalisation value in units of <U>
    v0_err : float
        error of `v0` (same units as `v0`)
    
    Returns
    -------
    float
        error of T in computed using gaussian error propagation of trend 
        formula in units of %/yr
    """
    
    delta_sl = m_err / v0
    delta_ref = m * v0_err / v0**2
    return np.sqrt(delta_sl**2 + delta_ref**2) * 100

def _get_season(m, yr):
    for seas, months in SEASONS.items():
        if m in months:
            return '{}-{}'.format(seas, int(yr))
    raise ValueError('Failed to retrieve season for m={}, yr={}'
                     .format(m, yr))
 
def _mid_season(seas, yr):
    if seas=='spring':
        return np.datetime64('{}-04-15'.format(yr))    
    if seas=='summer':
        return np.datetime64('{}-07-15'.format(yr))
    if seas=='autumn':
        return np.datetime64('{}-10-15'.format(yr))    
    if seas=='winter':
        return np.datetime64('{}-01-15'.format(yr))    
    if seas=='all':
        return np.datetime64('{}-06-15'.format(yr))    
    raise ValueError('Invalid input for season (seas):', seas)
    

def _find_area(lat, lon, regions_dict=None):
    """Find area corresponding to input lat/lon coordinate
    
    Parameters
    ----------
    lat : float
        latitude
    lon : float
        longitude
    
    Returns
    -------
    str
        name of region
    """
    from pyaerocom.region import find_closest_region_coord
    reg = find_closest_region_coord(lat, lon)
    if regions_dict is not None and reg in regions_dict:
        return regions_dict[reg]
    return reg
    
def compute_trends_station(station, var_name, start_year=None, 
                           stop_year=None, season=None, slope_alpha=0.68,
                           **alt_range):
    # load additional information about data source (if applicable)
    
    freq = station.get_var_ts_type(var_name)
    
    # init empty dictionary that is used to store trends results and daily,
    # monthly and yearly time-series.
    tdata = {}
    
    ts_types = const.GRID_IO.TS_TYPES
    
    if freq in ts_types and ts_types.index(freq) >= ts_types.index('monthly'):
        raise TemporalResolutionError('Need monthly or higher')
    if not freq in ts_types or ts_types.index(freq) <= ts_types.index('daily'):
        tdata['daily'] = station.to_timeseries(var_name, ts_type='daily', 
                                               **alt_range)
    
    tdata['monthly'] = s = station.to_timeseries(var_name, freq='monthly', 
                                                 **alt_range)
    
    if len(s) == 0 or all(np.isnan(s)):
        raise DataCoverageError('Failed to retrieve timeseries')
    

    dates = s.index

    #dates = pd.DatetimeIndex(index)
    d = dict(date=dates,
             value=s.values,
             year=dates.year,
             month=dates.month,
             day=dates.day)    

    mobs = pd.DataFrame(d)
    
    df_fun = lambda row: _get_season(row['month'], row['year'])
    
    mobs['season'] = mobs.apply(df_fun, axis=1)
    mobs = mobs.dropna(subset=['value'])
    # FOLLOWING LINE COMMENTED OUT BY JGLISS (17.12.2018)
    #data['dobs'].dropna(subset=['value'],inplace=True)
    # Group data first by year, then by month
    
    yrs = sorted(np.unique(mobs['year']))
    if start_year is None:
        start_year = yrs[0]
    if stop_year is None:
        stop_year =  yrs[-1]

    dates = []
    values = []
    
    if season in [None, 'all']:
        seas = 'all'
    elif season in SEASONS:
        seas = season
    
    #filter the months
    for yr in yrs:
        dates.append(_mid_season(seas, yr))
        if seas == 'all': #yearly trends
            subset = mobs[mobs['year'] == yr]
        else:
            subset = mobs[mobs['season'].str.contains('{}-{}'.format(seas, yr))]
        #needs 4 seasons to compute seasonal average to avoid biases
        if seas=='all' and len(np.unique(subset['season'].values)) < 4:
            values.append(np.nan)
        else:
            values.append(np.nanmean(subset['value']))
    # assign dates and jsdates vector to data dict
    dates  = np.asarray(dates)
    values = np.asarray(values)

    tdata['yearly'] = pd.Series(values, index=dates)
    
    start_date = _mid_season(seas, start_year)
    stop_date = _mid_season(seas, stop_year)
        
    # datetime index covering whole input period (data may not be fully covered
    # in the whole period)
    period_index = pd.date_range(start=start_date,
                                 end=stop_date, 
                                 freq=pd.DateOffset(years=1))
    
    num_dates_period = period_index.values.astype('datetime64[Y]').astype(np.float64)

    # get period filter mask
    tmask = np.logical_and(dates>=start_date, 
                           dates<=stop_date) 
        
    # apply period mask to jsdate vector and value vector
    dates_data = dates[tmask]
    
    # vector containing data values
    vals = values[tmask]
    
    valid = ~np.isnan(vals)
    
    #works only on not nan values
    dates_data = dates_data[valid]
    vals = vals[valid]
    
    num_dates_data = dates_data.astype('datetime64[Y]').astype(np.float64)
    
    # create empty dictionary that is used to store trends results
    result = _init_trends_result_dict(start_year)
    
    #TODO: len(y) is number of years - 1 due to midseason averages
    result['n'] = len(vals)
    
    if len(vals) > 2:
        result['y_mean'] = np.nanmean(vals)
        result['y_min'] = np.nanmin(vals)
        result['y_max'] = np.nanmax(vals)
        
        #Mann / Kendall test
        [tau, pval] = kendalltau(x=num_dates_data, y=vals)
        
        
        (slope, 
         yoffs, 
         slope_low, 
         slope_up) = theilslopes(y=vals, x=num_dates_data, 
                                 alpha=slope_alpha)
        
        # estimate error of slope at input confidence level
        slope_err = np.mean([abs(slope - slope_low), 
                             abs(slope - slope_up)])
        
        reg_data = slope * num_dates_data + yoffs
        reg_period = slope * num_dates_period  + yoffs
        
        
        # value used for normalisation of slope to compute trend T
        # T=m / v0
        v0_data = reg_data[0]
        v0_period = reg_period[0]
        
        # Compute the mean residual value, which is used to estimate
        # the uncertainty in the normalisation value used to compute
        # trend
        mean_residual = np.mean(np.abs(vals - reg_data))
        
        # trend is slope normalised by first reference value. 
        # 2 trends are computed, 1. the trend using the first value of
        # the regression line at the first available data year, 2. the
        # trend corresponding to the value corresponding to the first
        # year of the considered period.
        
        trend_data = slope / v0_data * 100
        trend_period =  slope / v0_period * 100
        
        # Compute errors of normalisation values
        v0_err_data = mean_residual
        t0_data, tN_data = num_dates_data[0], num_dates_data[-1]
        t0_period = num_dates_period[0]
        
        # sanity check
        assert t0_data < tN_data
        assert t0_period <= t0_data
        
        dt_ratio = (t0_data - t0_period) / (tN_data - t0_data)
        
        v0_err_period = v0_err_data * (1 + dt_ratio)
        
        trend_data_err = _compute_trend_error(m=slope,
                                              m_err=slope_err,
                                              v0=v0_data,
                                              v0_err=v0_err_data)
                                                  
        trend_period_err = _compute_trend_error(m=slope,
                                                m_err=slope_err,
                                                v0=v0_period,
                                                v0_err=v0_err_period)
                        
        result['pval'] = pval
        result['m'] = slope
        result['m_err'] =slope_err
        
        result['slp'] = trend_data
        result['slp_err'] = trend_data_err
        result['reg0'] = v0_data
    
        if v0_period > 0:
            result['slp_{}'.format(start_year)] = trend_period
            result['slp_{}_err'.format(start_year)] = trend_period_err
            result['reg0_{}'.format(start_year)] = v0_period
    
    tdata['result'] = result
    period = '{}-{}'.format(start_year, stop_year)
    if not 'trends' in station:
        station.trends = {}
    station.trends[period]
    return station
    
  
    
if __name__ == '__main__':
    import pyaerocom as pya
    
    r = pya.io.ReadUngridded()
    data = r.read('AeronetSunV3Lev2.daily', vars_to_retrieve='od550aer',
                  file_pattern='Solar*')
    
    stat = data.to_station_data('Solar*')
    
    stat = compute_trends_station(stat, 'od550aer', start_year=1995, 
                                  stop_year=2017)
    
    
    
    
    
    