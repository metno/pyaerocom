# -*- coding: utf-8 -*-

"""
High level test methods that check AasEtAl time series data for selected stations
Created on June 12 2019.

@author: hannas@met.no
"""
import pytest
import numpy.testing as npt
import numpy as np
import pandas as pd

import datetime
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes

import pyaerocom as pya
from pyaerocom.test.settings import lustre_unavail, TEST_RTOL
from pyaerocom.io.read_aasetal import ReadSulphurAasEtAl
from pyaerocom.io.helpers_units import (unitconv_sfc_conc_bck, 
                                        unitconv_sfc_conc, 
                                        unitconv_wet_depo_bck,
                                        unitconv_wet_depo)

TRUE_SLOPE = {'N-America': {"sconcso4": {'2000–2010': -3.03,
                                          '2000–2015': -3.15},

                             "wetso4": {'2000–2010': -2.30,
                                        '2000–2015': -2.78},

                             'sconcso2': {'2000–2010': -4.55,
                                          '2000–2015':-4.69
                                          }},

                   'Europe': {'sconcso4': {'2000–2010':  -2.86,
                                           '2000–2015':  -2.67},

                              'wetso4': {'2000–2010': -3.85,
                                         '2000–2015': -3.40,
                                         },
                              'sconcso2': {'2000–2010': -4.23,
                                           '2000–2015':-3.89
                                           },
                              },
                   }

TRUE_NR_STATIONS = {'N-America': {"sconcso4": {'2000–2010': 227,
                                               '2000–2015': 218},
                              
                                     "wetso4": {'2000–2010': 226,
                                                '2000–2015': 215
                                                },
        
                                     'sconcso2': {'2000–2010': 78,
                                                  '2000–2015': 77
                                                  }},

                       'Europe': {'sconcso4': {'2000–2010': 43,
                                               '2000–2015': 36},

                                  'wetso4': {'2000–2010': 73,
                                             '2000–2015': 67
                                             },
                                  'sconcso2': {'2000–2010': 51,
                                               '2000–2015': 47
                                               },
                                  },
                       }


def _get_season_current(mm,yyyy):
    if mm in [3,4,5]:
        s = 'spring-'+str(int(yyyy))
    if mm in [6,7,8]:
        s = 'summer-'+str(int(yyyy))
    if mm in [9,10,11]:
        s = 'autumn-'+str(int(yyyy))
    if mm in [12]:
        s = 'winter-'+str(int(yyyy))
    if mm in [1,2]:
        s = 'winter-'+str(int(yyyy-1))
    return s

def _mid_season_current(seas, yr):
    """ Calculated the mid date for a season.
    
    From original trends interface developed by A. Mortier.
    
    Parameters
    ------------------
    seas : str
        Season
        
    yr : int
        year
    """
    if seas=='spring':
        date = datetime.datetime(yr,4,15)
    if seas=='summer':
        date = datetime.datetime(yr,7,15)
    if seas=='autumn':
        date = datetime.datetime(yr,10,15)
    if seas=='winter':
        date = datetime.datetime(yr-1,1,15)
    if seas=='all':
        date = datetime.datetime(yr,6,15)
    return date

def compute_trends_current(s_monthly, periods, only_yearly=True):
    """ Compute trends for station. 
    
    Used in the trends interface to compute the trends before. 05.06.19.

    Slightly modified code from original trends interface developed by
    A. Mortier.

    Parameters
    ------------------------

    s_monthly : pd.DataFrame
        Dataframe containing montly values of data.
    
    periods : list[str]
        List containing periods.

    only_yearly : boolean
    
    Returns 
    ------------------------
    data : dict
        Dictionary containing the trends.

    Main changes applied:
        - Keep NaNs

    """
    
    d = dict(month=s_monthly.index.month,
             year=s_monthly.index.year,
             value=s_monthly.values)

    mobs = pd.DataFrame(d)
    #print(mobs.head())

    mobs['season'] = mobs.apply(lambda row: _get_season_current(row['month'],
                                                                row['year']), 
                                                                axis=1)
    # drop rows where value = nan.
    mobs = mobs.dropna(subset=['value'])

    # trends with yearly and seasonal averages
    seasons = ['spring', 'summer', 'autumn', 'winter', 'all']
    yrs = np.unique(mobs['year'])
    #print('yrs {}'.format(yrs))
    data = {}
    
    # added to minimize the computation
    for i, seas in enumerate(seasons):
        if only_yearly and not seas == 'all':
            continue
        # initialize seasonal object
        data[seas] = {'date': [], 'jsdate': [], 'val': []}
        # filter the months
        for yr in yrs:
            if seas != 'all':
                catch = mobs[mobs['season'].str.contains(seas + '-' + str(yr))]
            else:
                catch = mobs[mobs['season'].str.contains('-' + str(yr))]
            date = _mid_season_current(seas, yr)

            data[seas]['date'].append(date)
            epoch = datetime.datetime(1970, 1, 1)
            data[seas]['jsdate'] = [(dat - epoch).total_seconds() * 1000 for dat in data[seas]['date']]

            # needs 4 seasons to compute seasonal average to avoid biases
            if (seas == 'all') & (len(np.unique(catch['season'].values)) < 4):
                data[seas]['val'].append(np.nan)
            else:
                #print(catch['value'])
                data[seas]['val'].append(np.nanmean(catch['value']))
        
        # trends for this season
        data[seas]['trends'] = {}   
        # filter period
        for period in periods:
            p0 = int(period[:4])
            p1 = int(period[5:])
            data[seas]['trends'][period] = {}
      
            # Mann-Kendall test
            x = np.array(data[seas]['jsdate'])
            y = np.array(data[seas]['val'])
            len_period = len(y)

            # works only on not nan values
            x = x[~np.isnan(y)] # Better ith np.isfinite()
            y = y[~np.isnan(y)]

            # filtering to the period limit
            jsp0 = (datetime.datetime(p0, 1, 1) - epoch).total_seconds() * 1000
            jsp1 = (datetime.datetime(p1, 12, 31) - epoch).total_seconds() * 1000
            
            y = y[(x >= jsp0) & (x <= jsp1)] 
            x = x[(x >= jsp0) & (x <= jsp1)]
  
            #print("y: len {}, x : {}".format(len(y), len(x)))
            
            # Making sure there is at least 75% coverage in the data period.
            # and that we have more than two points
            if len(y)/len_period >= 0.75 and len(y) > 1: 
                # kendall
                # TODO THIS IS WHERE YOU SHOULD ASK AUGUSTIN HOW THINGS 
                # SHOULD BE RESTRICTED BY KENTAL TAu
                
                [tau, pval] = kendalltau(x, y)
                #print('pval {}'.format(pval))
                data[seas]['trends'][period]['pval'] = pval
                
                if pval < 0.1:
                    # Theil slope
                    res = theilslopes(y, x, 0.9)
                    print(res)
                    medslope, medintercept, lo_slope, up_slope = res
                    reg = medslope* np.asarray(x) + medintercept * np.ones(len(x))
                    print(res)
                    #print('avrage slp {}'.format(np.mean(res/reg)*1000 * 60 * 60 * 24 * 365.25))
                    #print('reg {}'.format(reg))
                    
                    slp = res[0] * 1000 * 60 * 60 * 24 * 365.25 / reg[0]  # slp per milliseconds to slp per year
                    data[seas]['trends'][period]['slp'] = slp * 100  # in percent
                    data[seas]['trends'][period]['reg0'] = reg[0]
                    data[seas]['trends'][period]['t0'] = x[0]
                    data[seas]['trends'][period]['n'] = len(y)
                else:
                    data[seas]['trends'][period]['pval'] = None
                    data[seas]['trends'][period]['slp'] = None
                    data[seas]['trends'][period]['reg0'] = None
                    data[seas]['trends'][period]['t0'] = None
                    data[seas]['trends'][period]['n'] = len(y) 
            else:
                #print('Not enough data coverage.')
                data[seas]['trends'][period]['pval'] = None
                data[seas]['trends'][period]['slp'] = None
                data[seas]['trends'][period]['reg0'] = None
                data[seas]['trends'][period]['t0'] = None
                data[seas]['trends'][period]['n'] = len(y) 
            #print( data[seas]['trends'][period] )   
    return data

def test_unitconversion_surface_conc():
    a = 10
    temp = unitconv_sfc_conc(a, 2)
    A = unitconv_sfc_conc_bck(temp, 2)
    #print("a {}, temp {} , A{}".format(a, temp,  A))
    assert np.abs(a - A) < 0.001

def test_unitconversion_wetdep():
    a = 10
    temp = unitconv_wet_depo(a)
    A = unitconv_wet_depo_bck(temp)
    #print("a {}, temp {} , A{}".format(a, temp,  A))
    assert np.abs(a - A) < 0.001

def create_region(region):
    """ Small modifications to the one in the trends interface.

    Function to create regions.

    Parameters
    -----------------------
    region : str
        Name of existing region.

    Returns
    -----------------------------
        minLon, maxLon, minLat, maxLat : ndarray[int]
    """

    regions = {
        # 'US': {'minLat': 22.5, 'maxLat': 71.0, 'minLon': -167, 'maxLon': -59.6},
        'N-America': {'minLat': 15.0, 'maxLat': 72.0, 'minLon': -170.0, 'maxLon': -50.0},
        'S-America': {'minLat': -55.0, 'maxLat': 14.0, 'minLon': -85.0, 'maxLon': -33.0},
        'Europe': {'minLat': 34.2, 'maxLat': 67.2, 'minLon': -28.7, 'maxLon': 69.1},
        'East-Asia': {'minLat': -12.62, 'maxLat': 59.9, 'minLon': 97.0, 'maxLon': 161.19},
        'Africa': {'minLat': -41.03, 'maxLat': 33.08, 'minLon': -18.45, 'maxLon': 58.54},
        'India': {'minLat': 3.06, 'maxLat': 36.0, 'minLon': 65.92, 'maxLon': 96.0},
        'East-US': {'minLat': 30, 'maxLat': 45, 'minLon': -95, 'maxLon': -75},
        'Central-Europe': {'minLat': 40, 'maxLat': 55, 'minLon': -5, 'maxLon': 40},
        'Most-East-Asia': {'minLat': 25, 'maxLat': 45, 'minLon': 100, 'maxLon': 130},
        'World': {'minLat': -90, 'maxLat': 90, 'minLon': -180, 'maxLon': 180},
        '': {'minLat': 0, 'maxLat': 0, 'minLon': 0, 'maxLon': 0, 'zf': 0},
    }
    return regions[region]['minLon'], regions[region]['maxLon'], regions[region]['minLat'], regions[region]['maxLat']


def crop_data_to_region(ungridded, region = "Europe"):
    """ Function which filter out the stations in the correct region.

    Parameters
    -------------
    ungridded : :class:`UngriddedData`
        Ungridded data object which contain data from one variable (filter by meta is not implemented for several variables yet.)

    region : str
        Name of region, default is N-America.

    Returns
    -------
    croppped_ungridded : :class:`UngriddedData`
        Ungridded data object which only contain stations from the correct data.

    """
    valid_names = ['N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 
                   'India', 'East-US', 'Central-Europe', 'Most-East-Asia']
    
    if region in valid_names:
        minLon, maxLon, minLat, maxLat = create_region(region = region)
        croppped_ungridded = ungridded.filter_by_meta(latitude=(minLat, maxLat), 
                                                      longitude=(minLon, maxLon))
        return croppped_ungridded
    else:
        raise ValueError("{} is not a valid region. "
                         "Try 'N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', "
                         "'Central-Europe', 'Most-East-Asia' ".format(region))

def years_to_string(start, stop):
    """Function to make it simpler to retrieve testdata from dictionary."""
    return "{}–{}".format(start, stop)

def years_from_periodstr(period):
    return [int(x) for x in period.split('–')]

def convert_data(data, var):
    if var == "sconcso4":
        return unitconv_sfc_conc_bck(data, x=4)
    elif var == "sconcso2":
        unitconv_sfc_conc_bck(data, x=2)
    elif var == "wetso4":
        unitconv_wet_depo_bck(data)
    else:
        raise ValueError("{} is not a valid variable.".format(var))


def calc_slope(ungridded, region, period, var):
    """
    Check if the number of stations present is only counting the ones with more 
    than 7 years of averages.
    
    :return: Boolean
    """
    # crop data to region
    start, stop = years_from_periodstr(period[0])
    regional = crop_data_to_region(ungridded, region = region)

    # crop to timeseries
    stations =  regional.to_station_data_all(var, start, stop, 'monthly')
    name = stations['station_name']
    #print('nbr names {}'.format(len(name)))
    slp_stations = []
    station_names = []

    for station in stations['stats']:
        #date = station['dtime']
        ts = station[var]
        s_monthly = convert_data(ts.values, var)
        # not pandas series now may need to convert it back to that
        s_monthly = ts
        # input to compute_trends_current period is supposed to be a list.
        data = compute_trends_current(s_monthly, period, only_yearly=True)
        slp = data['all']['trends'][period[0]]['slp']

        if slp is not None:
            slp_stations.append(slp)
            station_names.append(station.station_name)
            
            
    print('\n Percentage {}/{} = {}'.format(len(station_names), len(name), 
                                          len(station_names)/ len(name) ))
    
    max_name = station_names[np.argmax(slp_stations)] 
    slp_stations.remove(np.max(slp_stations))
    slp_stations.remove(np.max(slp_stations))
    nr_stations = len(slp_stations)
    
    #plt.plot(slp_stations)
    #plt.title('Station {}'.format(max_name))
    #plt.xticks(station_names)
    #plt.show()
    
    return nr_stations, np.mean(slp_stations)

@lustre_unavail
def test_ungriddeddata():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read()  # read all variables
    #print('len(data.station_name = {})'.format( len(data.station_name) ))
    #print('data.shape {} '.format(data.shape))
    assert len(data.station_name) == 890
    assert data.shape == (436121, 12)

@lustre_unavail
def test_article():
    regions = ['Europe', 'N-America']
    VARS = ['sconcso4', 'sconcso2', 'wetso4']
    periods = ['2000–2010', '2000–2015'] # OBS (bad coding) problems with the heigfen. 

    for v in VARS:
        # can reuse the ungridded data object for all regions and periods.
        ungridded = ReadSulphurAasEtAl().read(vars_to_retrieve=v)
        for r in regions:
            for p in periods:
                
                # true values
                true_mean_slope = TRUE_SLOPE[r][v][p]
                ns = TRUE_NR_STATIONS[r][v][p]
                
                # computed values              
                nr_stations, predicted_mean_slope = calc_slope(ungridded, r, [p], v)
                print("REGION {}, variable {}, period {} ".format(r, v, p))
                print("calc {} ,  true [nr stations] {}".format(nr_stations, ns))
                print("calc_slope {}, true_slope   {}".format(
                                        np.around(predicted_mean_slope, 2), true_mean_slope))
                
                # Test similarity:
                
                # TODO 1) check slope (calc_slope - true_slope) / true_slope x 100
                # TODO 2) check that the number of stations are the same.
                
                #assert nr_stations == ns1
                #assert nr_stations2 == ns2
                #assert predicted_mean_slope1 == true_mean_slope1
                #assert predicted_mean_slope2 == true_mean_slope2



if __name__ == "__main__":
    # pya.change_verbosity('info')
    # import sys
    
    # OBS the three below works
    #test_unitconversion_surface_conc()
    #test_unitconversion_wetdep()
    #test_ungriddeddata()
    
    # TODO test article on hold 
    test_article()

    
    
# =============================================================================
