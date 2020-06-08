#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods for computation of trends

Note
----
Most methods here are private and not to be used directly. Please use
:class:`TrendsEngine` instead.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

def _years_from_periodstr(period):
    """Convert period str to start / stop years

    Parameters
    ----------
    period : str
        period str, e.g. '1990-2010'

    Returns
    -------
    int
        start year
    int
        stop year
    """
    return [int(x) for x in period.split('-')]

def _start_stop_period(period):
    """Convert period str to start / stop dates

    Parameters
    ----------
    period : str
        period str, e.g. '1990-2010'

    Returns
    -------
    date
        start datetime
    date
        stop datetime
    """
    from datetime import date
    y0, y1, = _years_from_periodstr(period)
    return (date(y0, 1, 1), date(y1, 12, 31))

def _make_mobs_dataframe(monthly_series):

    dates = monthly_series.index

    #dates = pd.DatetimeIndex(index)
    d = dict(date=dates,
             value=monthly_series.values,
             year=dates.year,
             month=dates.month,
             day=dates.day)

    mobs = pd.DataFrame(d)

    add_season = lambda row: _get_season(row['month'], row['year'])
    # add season column to dataframe
    mobs['season'] = mobs.apply(add_season, axis=1)

    # remove all NaN values
    mobs = mobs.dropna(subset=['value'])

    return mobs

def _init_period(mobs, start_year=None, stop_year=None):
    yrs = sorted(np.unique(mobs['year']))
    if start_year is None:
        start_year = yrs[0]
    if stop_year is None:
        stop_year =  yrs[-1]
    if stop_year < yrs[0] or start_year > yrs[-1]:
        from pyaerocom.exceptions import TimeMatchError
        raise TimeMatchError('Input period {}-{} is not covered by data ({}-{})'
                             .format(start_year, stop_year, yrs[0],yrs[-1]))
    pstr = '{}-{}'.format(int(start_year), int(stop_year))
    return (start_year, stop_year, pstr, yrs)

def _get_yearly(mobs, seas, yrs):
    dates = []
    values = []
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

    return pd.Series(values, index=dates)

def _init_period_dates(start_year, stop_year, season):
    start_date = _mid_season(season, start_year)
    stop_date = _mid_season(season, stop_year)

    # datetime index covering whole input period (data may not be fully covered
    # in the whole period)
    period_index = pd.date_range(start=start_date,
                                 end=stop_date,
                                 freq=pd.DateOffset(years=1))

    num_dates_period = period_index.values.astype('datetime64[Y]').astype(np.float64)
    return (start_date, stop_date, period_index, num_dates_period)

if __name__ == '__main__':
    import pyaerocom as pya
    plt.close('all')

    r = pya.io.ReadUngridded()
    data = r.read('AeronetSunV3Lev2.daily', vars_to_retrieve='od550aer',
                  file_pattern='Solar*')

    stat = data.to_station_data('Solar*')

    stat.compute_trend('od550aer', 2002, 2012)
    tr = stat.trends['od550aer']

    ax = tr.plot(season='all', period='1995-2017')

    ax = tr.plot(season='all', period='2002-2012')
    plt.show()
