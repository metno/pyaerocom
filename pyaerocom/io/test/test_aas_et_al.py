# -*- coding: utf-8 -*-

"""
High level test methods that check AasEtAl time series data for selected stations
Created on June 12 2019.

@author: hannas
"""
import pytest
import numpy.testing as npt
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

# TODO Now you need to convert back the units before you write the tests


TRUE_SLOPE = {'N-America': {"sconcso4": {'2000–2010': -3.03,
                                          '2000–2015':  -3.15},

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


def mass_to_nr_molecules(mass, Mm):
    """ Calculating the number of molecules form mass and molarmass.

    Mass, Molar mass need to be in the same unit, either both g and g/mol 
    or kg and kg/mol.
    
    Parameters
    ---------------------------
    mass : float
        mass of all compounds.
        
    mm : float
        molar mass of compound.
    
    Returns 
    -----------------
    nr_molecules : float
        number of molecules     
    """
    A = 6.022*10**23
    nr_molecules = mass/Mm*A
    return nr_molecules

def nr_molecules_to_mass(nr_molecules, mm):
    """ Calculates the mass from the number of molecules and molar mass.
    
    Parameters
    ---------------
    nr_molecules : int
        Number of molecules
        
    mm : float
        Molar mass [g/mol]
    
    Returns 
    ---------------------
    mass : float
        mass in grams
    """
    A = 6.022*10**23 # avogadros number
    mass = mm*nr_molecules/A
    return mass

    
def unitconversion_wet_deposition_back(data, ts_type = "monthly"):
    """ The unitconversion ugSOx/m3 to ugS/m3.

    Removing the weight of oxygen.

    Parameters
    ------------------
    data: ndarray
        Sulphur data you wish to convert.
        
    ts_type: str    
       The timeseries type. Default monthly.
    
    Returns
    ------------------
    data : ndarray
       Sulphur data in units of ugSOx/m3.
    """
    mm_compund = 0.001*32.065 + 0.001*15.999*4
    mm_s = 0.001*32.065   
    nr_molecules = nr_molecules_to_mass(data, mm_compund) # in the order of 10**27 
    mass_S = nr_molecules_to_mass(nr_molecules, mm_s)
    #TODO : to be mulitplied with the number of days in one year.
    return mass_S/10000 # to be multiplied by the numebers of days in a month

def unitconversion_surface_consentrations_back(data, x = 2):
    """ Converting: ug SOx/m3 to  ugS/ m3.
    
    Parameters
    ------------------
    data: ndarray
        Contains the data in units of ug ugS/m3.
    
    x: int
        The number of oxygen atoms, O in you desired SOx compound.
    
    Returns
    ------------
    data : ndarray  
        in units of ugS/ m3.
    
    """

    mmO = x*15.9999*10**6 # molar mass oxygen
    mmS = 32.065 # molar mass sulphur
    
    nr_molecules = data/ (x*mmO*10**6) * (6.022*10**23)
    weight_sox = nr_molecules*mmS*10**6 
    return weight_sox

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

    Parameters:
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
    # sm = to_monthly_current_trends_interface(s0, MIN_DIM)
    d = dict(month=s_monthly.index.month,
             year=s_monthly.index.year,
             value=s_monthly.values)

    mobs = pd.DataFrame(d)

    mobs['season'] = mobs.apply(lambda row: _get_season_current(row['month'],
                                                                row['year']), 
                                                                axis=1)
    # drop rows where value = nan.
    mobs = mobs.dropna(subset=['value'])

    # trends with yearly and seasonal averages
    seasons = ['spring', 'summer', 'autumn', 'winter', 'all']
    yrs = np.unique(mobs['year'])

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
            x = x[~np.isnan(y)]
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
                [tau, pval] = kendalltau(x, y)
                data[seas]['trends'][period]['pval'] = pval
                
                # theil slope
                res = theilslopes(y, x, 0.9)
                reg = res[0] * np.asarray(x) + res[1] * np.ones(len(x))
                slp = res[0] * 1000 * 60 * 60 * 24 * 365 / reg[0]  # slp per milliseconds to slp per year
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
    return data



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

    Parameters:
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
    stations =  regional.to_station_data_all(var, start, stop, 'monthly')
    slp_stations = []
    station_names = []
    # Since the true value have two decimals. We allow a error, diff < 0.01
    # this would be attributed to all other decimals.

    for station in stations['stats']:
        #date = station['dtime']
        ts = station[var]
        s_monthly = ts # is a pandas series
        # input to compute_trends_current period is supposed to be a list.
        data = compute_trends_current(s_monthly, period, only_yearly=True)
        slp = data['all']['trends'][period[0]]['slp']

        if slp is not None:
            slp_stations.append(slp)
        else:     
            station_names.append( station.station_name )
            
    print(station_names)
    nr_stations = len(slp_stations)
    return nr_stations, np.mean(slp_stations)

@lustre_unavail
def test_ungriddeddata_surface_cons_so2():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read()  # read all variables
    
    assert len(data.station_name) == 890
    assert data.shape == (1063631, 12)

    regions = ['Europe', 'N-America']
    # TODO Add wetso4,k in fact add oxygen to all of them
    VARS = ['sconcso4', 'sconcso2']
    periods = ['2000–2010', '2000–2015'] # not useed yet bcause of problems with the heigfen. 

    # todo LOOP OVER PERIODS

    for v in VARS:
        # can reuse the ungridded data object for all regions and periods.
        ungridded = ReadSulphurAasEtAl().read(vars_to_retrieve=v)
        for r in regions:
            for p in periods:
                #true_mean_slope1 = true_slope[r][v]['2000–2010']
                #true_mean_slope2 = true_slope[r][v]['2000–2015']
                true_mean_slope = TRUE_SLOPE[r][v][p]
                #ns1 = true_nr_stations[r][v]['2000–2010']
                #ns2 = true_nr_stations[r][v]['2000–2015']
                ns = TRUE_NR_STATIONS[r][v][p]
                print("  ")
                nr_stations, predicted_mean_slope = test_slope(ungridded, r, [p], v)
                print(" REGION {}, variable {}, period {} ".format(r, v, p))
                print("calc {} ,  true [nr stations] {}".format(nr_stations, ns))
                print("calc_slope {}, true_slope   {}".format(
                                        predicted_mean_slope, true_mean_slope))
                
                #assert nr_stations == ns1
                #assert nr_stations2 == ns2
                #assert predicted_mean_slope1 == true_mean_slope1
                #assert predicted_mean_slope2 == true_mean_slope2

#   Montly means are calculated for months with 70% or better data converage.

"""
TODO:

(*) The units needs to be converted to including weight of oxygen.

(**)  Test shold convert units back before they test anything. 
BUT Look into the model files and double check that these don't contain only the mass of S. 

1. Make the test pass without unitconverision 
2. Apply unitconversion make sure all test pass.
OBS! Ask Jonas about the units available on the trends interface.


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