#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 10:36:24 2019

@author: jonasg
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize
from collections import OrderedDict as od
from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes
import pandas as pd
from pyaerocom import const
from pyaerocom.metastandards import StationMetaData

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

class TrendsEngine(object):
    """Result object for trends analysis
    
    Parameters
    ----------
    var_name : str
        name of variable 
        
    Attributes
    ----------
    var_name : str
        name of variable 
    meta : dict
        dictionary containing relevant meta information about data
    daily : pandas.Series
        daily data
    monthly : pandas.Series
        monthly data
    yearly : dict
        dictionary containing yearly data for each season. Keys are season names, 
        values are instances of :class:`pandas.Series`
    results : dict
        Nested dictionary containing results from trends analysis. First layer
        is season, second layer is period, and values are dictionaries with 
        results (cf. keys of dictionary returned by 
        :func:`_init_trends_result_dict`)
    """
    CMAP = get_cmap('bwr')
    NORM = Normalize(-10, 10)
    
    def __init__(self, var_name=None, **kwargs):
        self.var_name = var_name
        self.meta = StationMetaData()
        
        self._daily = None
        self._monthly = None
        self.yearly = od()
        
        self.results = od()
        self._mobs = None 
        
    @property
    def daily(self):
        """Daily timeseries"""
        return self._daily
    
    @daily.setter
    def daily(self, val):
        if not isinstance(val, pd.Series):
            raise ValueError('Invalid input for attr. daily. Need '
                             'pandas.Series.')
        self._daily = val
        self.compute_monthly()
    
    @property
    def monthly(self):
        """Monthly timeseries"""
        return self._monthly
    
    @monthly.setter
    def monthly(self, val):
        if not isinstance(val, pd.Series):
            raise ValueError('Invalid input for attr. daily. Need '
                             'pandas.Series.')
        self._monthly = val
        self._mobs = _make_mobs_dataframe(val)
        
    @property
    def has_daily(self):
        """Boolean specifying whether daily data is available"""
        return True if isinstance(self.daily, pd.Series) else False
    
    @property
    def has_monthly(self):
        """Boolean specifying whether monthly data is available"""
        return True if isinstance(self.monthly, pd.Series) else False
    
    def compute_monthly(self, daily=None, **kwargs):
        """Computes monthly timeseries from daily
        
        Note
        ----
        Requires that daily timeseries data is available in :attr:`daily` or
        provided via **kwargs using keyword `daily`. This method also computes
        the monthly dataframe that contains the seasons and is available via
        :attr:`_mobs`.
        
        Parameters
        ----------
        daily : pandas.Series
            daily timeseries (will overwrite :attr:`daily`)
        **kwargs
            input args passed to :func:`pyaerocom.helpers.resample_timeseries`
            such as (`min_num_obs`)
        
        Returns
        -------
        pandas.Series
            monthly timeseries
        """
        from pyaerocom.helpers import resample_timeseries
        if daily is not None:
            self.daily = daily
        monthly = resample_timeseries(self.daily, freq='monthly', **kwargs)
        mobs = _make_mobs_dataframe(monthly)
        self._mobs = mobs
        self._monthly = monthly
        return monthly
    
    @property
    def seasons_avail(self):
        """List of all seasons for which trends are available"""
        return self.results.keys()
    
    @property
    def periods_avail(self):
        """List of all periods for which trends are available"""
        periods = []
        for seas, period_data in self.results.items():
            for per in list(period_data):
                if not per in periods:
                    periods.append(per)
        return periods
        
    def get_yearly(self, season):
        """Get yearly time series for a certain season
        
        Parameters
        ----------
        season : str
            name of season
        
        Returns
        -------
        pandas.Series
            yearly data for that season
        
        Raises
        ------
        AttributeError
            if yearly data is not available for that season
        """
        if not season in self.yearly:
            raise AttributeError('Yearly data for season {} is not available'
                                 .format(season))
        return self.yearly[season]
    
    def _get_trend_data(self, season, period):
        if not self.has_monthly:
            raise AttributeError('No monthly data available')
        elif not season in self.seasons_avail:
            raise AttributeError('No results available for season {}'.format(season))
        elif not period in self.periods_avail:
            raise AttributeError('No results available for period {}'.format(period))
        
        result = self.results[season][period]
        if result['m'] is None:
            raise AttributeError('No slope information available')
        
        start_data = self.monthly.index.year[0]
        stop_data = self.monthly.index.year[-1]
        
        start_period, stop_period = _years_from_periodstr(period)
        
        
        (_,_, idx_data, num_dates_data) = _init_period_dates(start_data, 
                                                             stop_data, 
                                                             season)
        (_,_, idx_period, num_dates_period) = _init_period_dates(start_period, 
                                                                 stop_period, 
                                                                 season)
        if start_data < start_period:
            start_data = start_period
        
        
        regr_data = result['m'] * num_dates_data + result['yoffs']
        regr_period = result['m'] * num_dates_period + result['yoffs']
        s_data = pd.Series(regr_data, idx_data)
        s_period = pd.Series(regr_period, idx_period)
        try:
            td = result['slp']
            td_err = result['slp_err']
        except:
            td = None
            td_err = None
        try:
            tp = result['slp_{}'.format(start_period)]
            tp_err = result['slp_{}_err'.format(start_period)]
        except:
            tp = None
            tp_err = None
        pval = result['pval']
        tdstr = ''
        tpstr = ''
        try:
            tdstr = (r'$\mathcal{{T}}_{{{}}}: {:.2f}\,\pm\,{:.2f}\,\%/yr$'
                     .format(start_data, td, td_err))
        except: 
            pass
        try:
            tpstr = (r'$\mathcal{{T}}_{{{}}}: \mathbf{{{:.2f}\,\pm\,{:.2f}\,\%/yr}}$'
                     .format(start_period, tp, tp_err))
        except:
            pass
        try:
            tpstr += '; pval: {:.1e}'.format(pval)
        except:
            tdstr += '; pval: {:.1e}'.format(pval)
        return (s_data, s_period, td, tp, tdstr, tpstr)
    
    def compute_trend(self, start_year, stop_year, season=None, 
                      slope_confidence=.68):
        if slope_confidence is None:
            slope_confidence = .68
        if self._mobs is None:
            raise ValueError('Cannot compute trends: monthly data is not '
                             'available')
        mobs = self._mobs
        start_year, stop_year, period_str, yrs = _init_period(mobs, start_year, 
                                                              stop_year)
        
        if season in [None, 'all']:
            seas = 'all'
        elif season in SEASONS:
            seas = season
           
        if not 'seas' in self.yearly:
            self['yearly'][seas] = yearly = _get_yearly(mobs, seas, yrs)
        else:
            yearly = self['yearly'][seas]
        
        dates = yearly.index.values
        values = yearly.values 
        (start_date, 
         stop_date, 
         period_index, 
         num_dates_period) = _init_period_dates(start_year, stop_year, seas)
        
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
                                     alpha=slope_confidence)
            
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
            result['yoffs'] = yoffs
            
            result['slp'] = trend_data
            result['slp_err'] = trend_data_err
            result['reg0'] = v0_data
            tp, tperr, v0p = None, None, None
            if v0_period > 0:
                tp = trend_period
                tperr = trend_period_err
                v0p = v0_period
            result['slp_{}'.format(start_year)] = tp
            result['slp_{}_err'.format(start_year)] = tperr
            result['reg0_{}'.format(start_year)] = v0p
            result['period'] = period_str
    
        if not seas in self.results:
            self.results[seas] = od()
        self.results[seas][period_str] = result

        return result

    def to_json(self):
        raise NotImplementedError
    
    def from_json(self, filepath):
        raise NotImplementedError
    
    def _plot_trend_result(self, tr, ax):
        pass
    
    def get_trend_color(self, trend_val):
        return self.CMAP(self.NORM(trend_val))
    
    def plot(self, season='all', period=None, ax=None):
        if not season in self.seasons_avail:
            raise AttributeError('No results available for season {}'
                                 .format(season))
        if period is None:
            if len(self.results[season]) > 1:
                raise ValueError('Found multiple trends for different periods: '
                                 '{}. Please specify period...'
                                 .format(list(self.results[season].keys())))
            period = list(self.results[season].keys())[0]
        if ax is None:
            fig, ax = plt.subplots(1,1, figsize=(18, 8))
        if self.has_daily:
            ax.plot(self.daily,'-', marker ='.',  label='daily', c='#d9d9d9')
        if self.has_monthly:
            ax.plot(self.monthly, label='monthly', c='#4d4d4d')
        ax.plot(self.get_yearly(season), ' ok', label='yearly')
        if period in self.periods_avail:
            
            (s_data, s_period, td, tp, tdstr,
             tpstr)= self._get_trend_data(season, period)
            
            ax.plot(s_data, '-', color=self.get_trend_color(td), label='trend', 
                    lw=2)
            ax.plot(s_period, '--', color=self.get_trend_color(tp))
            ax.text(0.01, 0.95, tpstr, transform=ax.transAxes,
                    fontsize=14)
            ax.text(0.01, 0.9, tdstr, transform=ax.transAxes, 
                    fontsize=14)
            
        ax.yaxis.grid(c='#d9d9d9', ls='-.')
        ylbl = self.var_name
        if self.var_name is not None and 'units' in self.meta:
            u = str(self.meta['units'])
            if not u in ['', '1']:
                ylbl += ' [{}]'.format(u)
        ax.set_ylabel(ylbl)
        tit = '' 
        if self.meta['station_name'] is not None:
            tit += self.meta['station_name']
            try:
                self.meta.load_dataset_info()
            except:
                pass
            dsinfo = self.meta.dataset_str()
            if dsinfo is not None:
                tit += '; {}'.format(dsinfo)
            tit += ' - '
        tit += period
        ax.set_title(tit)
        ax.legend(loc=1)
    
        ax.set_xlim(_start_stop_period(period))
        
        return ax
    
    def __getitem__(self, key):
        return self.__getattribute__(key)
        
    def __setitem__(self, key, val):
        self.__setattr__(key, val)
    
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

def compute_trends_station(station, var_name, start_year=None, 
                           stop_year=None, season=None, slope_confidence=0.68,
                           **alt_range):
    # load additional information about data source (if applicable)
    if not 'trends' in station:
        station['trends'] = od()
    tr = station['trends']
    if not var_name in tr:
        station['trends'][var_name] = trv = TrendsEngine(var_name)
    else:
        trv = station['trends'][var_name]

    freq = station.get_var_ts_type(var_name)
    
    ts_types = const.GRID_IO.TS_TYPES
    
    if not trv.has_daily:
        if not freq in ts_types or (ts_types.index(freq) <= ts_types.index('daily')):
            trv['daily'] = station.to_timeseries(var_name, freq='daily', **alt_range)
    # monthly is mandatory
    if not trv.has_monthly:
        if freq in ts_types and ts_types.index(freq) >= ts_types.index('monthly'):
            raise TemporalResolutionError('Need monthly or higher')
        ms = station.to_timeseries(var_name, freq='monthly', **alt_range)
        trv['monthly'] = ms
    else:
        ms = trv['monthly']
        
    if len(ms) == 0 or all(np.isnan(ms)):
        raise DataCoverageError('Failed to retrieve monthly timeseries for '
                                '{} ({})'.format(station.station_name,
                                 var_name))
      
    if trv._mobs is None:
        trv._mobs = _make_mobs_dataframe(ms)
    
    result = trv.compute_trend(start_year, stop_year, season, 
                               slope_confidence)
    
    
    trv.meta.update(station.get_meta(add_none_vals=True))
    if var_name in station.var_info:
        trv.meta.update(station.var_info[var_name])
    return result
    
if __name__ == '__main__':
    import pyaerocom as pya
    plt.close('all')
    
    r = pya.io.ReadUngridded()
    data = r.read('AeronetSunV3Lev2.daily', vars_to_retrieve='od550aer',
                  file_pattern='Solar*')
    
    stat = data.to_station_data('Solar*')
    
    compute_trends_station(stat, 'od550aer', start_year=1995, 
                           stop_year=2017)
    
    stat.compute_trend('od550aer', 2002, 2012)
    tr = stat.trends['od550aer']
    
    ax = tr.plot(season='all', period='1995-2017')
    
    ax = tr.plot(season='all', period='2002-2012')
    plt.show()
    
    
    