# -*- coding: utf-8 -*-

"""
High level test methods that check EBAS time series data for selected stations
Created on Thu Apr 12 14:45:43 2018
@author: hannas
"""
#import pytest
#import numpy.testing as npt
import numpy as np
import pyaerocom as pya
from pyaerocom.test.settings import lustre_unavail, TEST_RTOL
from pyaerocom.io.read_aasetal import ReadSulphurAasEtAl
import matplotlib.pyplot as plt
import datetime
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes
import pandas as pd


VARS = ['sconcso4', 'sconcso2']
# TODO add test or remove unoitconversion to inclkude 'wetso4'


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
    """ Compute trends for station. Used in the trends inte3rface to compute the trends before. 05.06.19.

    Slightly modified code from original trends interface developed by
    A. Mortier.

    s_monthly : pandas dataframe
    periods : list of periods???


    Main changes applied:
        - Keep NaNs

    """
    # sm = to_monthly_current_trends_interface(s0, MIN_DIM)
    d = dict(month=s_monthly.index.month,
             year=s_monthly.index.year,
             value=s_monthly.values)

    mobs = pd.DataFrame(d)

    mobs['season'] = mobs.apply(lambda row: _get_season_current(row['month'],
                                                                row['year']), axis=1)
    mobs = mobs.dropna(subset=['value'])

    # trends with yearly and seasonal averages
    seasons = ['spring', 'summer', 'autumn', 'winter', 'all']
    yrs = np.unique(mobs['year'])

    data = {}

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
            # works only on not nan values
            x = x[~np.isnan(y)]
            y = y[~np.isnan(y)]
            # filtering to the period limit
            jsp0 = (datetime.datetime(p0, 1, 1) - epoch).total_seconds() * 1000
            jsp1 = (datetime.datetime(p1, 12, 31) - epoch).total_seconds() * 1000
            y = y[(x >= jsp0) & (x <= jsp1)]
            x = x[(x >= jsp0) & (x <= jsp1)]

            if len(x) > 2:
                # kendall
                [tau, pval] = kendalltau(x, y)
                data[seas]['trends'][period]['pval'] = pval

                # theil slope
                res = theilslopes(y, x, 0.9)
                reg = res[0] * np.asarray(x) + res[1] * np.ones(len(x))
                slp = res[0] * 1000 * 60 * 60 * 24 * 365 / reg[0]  # slp per milliseconds to slp per year
                data[seas]['trends'][period]['slp'] = slp * 100  # in percent
                # TODO its only the above one which is interresting.

                data[seas]['trends'][period]['reg0'] = reg[0]
                data[seas]['trends'][period]['t0'] = x[0]
                data[seas]['trends'][period]['n'] = len(y)
            else:
                data[seas]['trends'][period]['pval'] = None
                data[seas]['trends'][period]['slp'] = None
                data[seas]['trends'][period]['reg0'] = None
                data[seas]['trends'][period]['t0'] = None
                data[seas]['trends'][period]['n'] = len(y)
    return data



# TODO: now it contains the values from slope not the std which is displayed now. Test one region and all variables.
regions_slope = {'N-America': {"sconcso4": {'2000–2010': -3.03,
                                          '2000–2015':  -3.15},

                             "wetso4": {'2000–2010': -2.30,
                                        '2000–2015': -2.78},

                             'sconcso2': {'2000–2010': -4.23,
                                          '2000–2015':-4.67
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


regions_nr_stations = {'N-America': {"sconcso4": {'2000–2010': 227,
                                                    '2000–2015': 218},
                                     "wetso4": {'2000–2010': 226,
                                                '2000–2015': 215
                                                },
        
                                     'sconcso2': {'2000–2010': 78,
                                                  '2000–2015': 77
                                                  }},

                       'Europe': {'sconcso4': {'2000–2010': 227,
                                               '2000–2015': 36},

                                  'wetso4': {'2000–2010': 73,
                                             '2000–2015': 67
                                             },
                                  'sconcso2': {'2000–2010': 51,
                                               '2000–2015': 47
                                               },
                                  },
                       }

def create_region(region):
    """ Small modifications to the one in the trends interface.

    Function to create regions

    Parameters:
    -----------------------
    region : str
        Name of existing region.

    Returns:
    -----------------------------
        minLon, maxLon, minLat, maxLat : array[int]
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

    Parameters:
    -------------
    ungridded : UngriddedData-object
        Ungridded data object which contain data from one variable (filter by meta is not implemented for several variables yet.)

    region : str
        Name of region, default is N-America.

    Returns
    -------
    croppped_ungridded : UngriddedData
        Ungridded data object which only contain stations from the correct data.

    """
    valid_names = ['N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', 'Central-Europe', 'Most-East-Asia']
    if region in valid_names:
        minLon, maxLon, minLat, maxLat = create_region(region = region)
        croppped_ungridded = ungridded.filter_by_meta(latitude=(minLat, maxLat), longitude=(minLon, maxLon))
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

@lustre_unavail
def test_std(list_of_a):
    """ The standard deviation of the slopes. One per station in the period

    Parameters:
    -------------
    list_of_a : array-like
        List containing the slopes for the different stations.

        TODO : calc std compare to the correct region for the correct timeperiod.


    Return:
    -----------------
    std : float
        The standard deviation for all stations on the chosen area.

    """
    pass

@lustre_unavail
def test_slope(ungridded, region, period, var):
    """
    Check if the number of stations present is only counting the ones with more than 7 years of averages.
    :return: Boolean
    """
    start, stop = years_from_periodstr(period[0])
    # crop data to region
    regional = crop_data_to_region(ungridded, region = region)

    # crop to timeseries
    stations =  regional.to_station_data_all(var, start, stop, 'monthly')['stats']
    slp_stations = []

    for station in stations:
        #date = station['dtime']
        ts = station[var]
        s_monthly = ts # is a pandas series
        # input to compute_trends_current period is supposed to be a list.
        data = compute_trends_current(s_monthly, period, only_yearly=True)
        seas = 'all'
        slp = data[seas]['trends'][period[0]]['slp']
        if not slp is None:
            slp_stations.append( data[seas]['trends'][period[0]]['slp'])
    # crop to months?
     # this will check what we do
    nr_stations = len(slp_stations)
    return nr_stations, np.mean(slp_stations)

@lustre_unavail
def test_ungriddeddata_surface_cons_so2():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read()  # read all variables
    assert len(data.station_name) == 629
    #assert 'n/a' in data.data_revision not woriking
    assert data.shape == (1008552, 12)

    regions = ['Europe', 'N-America']
    # TODO Add wetso4,k in fact add oxygen to all of them
    VARS = ['sconcso4', 'sconcso2']
    periods = ['2000–2010', '2000–2015'] #

    # todo LOOP OVER PERIODS

    for v in VARS:
        for r in regions:
            ungridded = ReadSulphurAasEtAl().read(vars_to_retrieve=v)

            true_mean_slope1 = regions_slope[r][v]['2000–2010']
            true_mean_slope2 = regions_slope[r][v]['2000–2015']

            ns1 = regions_nr_stations[r][v]['2000–2010']
            ns2 = regions_nr_stations[r][v]['2000–2015']

            nr_stations, predicted_mean_slope1 = test_slope(ungridded, r, ['2000–2010'],v)
            nr_stations2, predicted_mean_slope2 = test_slope(ungridded, r, ['2000–2015'], v)

            assert nr_stations == ns1
            assert nr_stations2 == ns2
            assert predicted_mean_slope1 == true_mean_slope1
            assert predicted_mean_slope2 == true_mean_slope2

"""
TODO:

(*) The units needs to be converted to including weight of oxygen.

(**)  Test shold convert units back before they test anything. 
BUT Look into the model files and double check that these don't contain only the mass of S. 

"""





if __name__ == "__main__":
    # pya.change_verbosity('info')
    # import sys
    test_ungriddeddata_surface_cons_so2()
# =============================================================================
#
#     d = _make_data()
#     stat = d.to_station_data('Jung*', start=2008, stop=2011, freq='monthly')
#     stat.plot_timeseries('scatc550aer')
#
# =============================================================================
# pytest.main(sys.argv)