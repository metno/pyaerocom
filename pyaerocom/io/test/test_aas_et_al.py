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
from scipy import stats

VARS = ['sconcso4', 'sconcso2']

# TODO add test or remove unoitconversion to inclkude 'wetso4'

regions_std = {'N-America': {"sconcso4": {'1990–2000': 0.025,
                                          '1990–2015': 0.024,
                                          '2000-2010': 0.029,
                                          '2000–2015': 0.029},

                             "wetso4": {'1980-1990': 0.18,
                                        '1990–2000': 0.13,
                                        '1990–2015': 0.10,
                                        '2000–2010': 0.13,
                                        '2000–2015': 0.13
                                        },

                             'sconcso2': {'1990–2000': 0.115,
                                          '1990–2015': 0.109,
                                          '2000–2010': 0.113,
                                          '2000–2015': 0.123
                                          }},

               'Europe': {'sconcso4': {'1980–1990': 0.094,
                                       '1990–2000': 0.052,
                                       '1990–2015': 0.015,
                                       '2000–2010': 0.041,
                                       '2000–2015': 0.028},

                          'wetso4': {'1980–1990': 0.36,
                                     '1990–2000': 0.29,
                                     '1990–2015': 0.12,
                                     '2000–2010': 0.13,
                                     '2000–2015': 0.10

                                     },
                          'sconcso2': {'1980–1990': 0.168,
                                       '1990–2000': 0.275,
                                       '1990–2015': 0.085,
                                       '2000–2010': 0.054,
                                       '2000–2015': 0.036
                                       },
                          },
               'India': {
                             'wetso4': {'1980–1990': 0.18,
                                        '1990–2000': 0.37,
                                         '2000–2010': 0.37,
                                         },
                              },

               'East-Asia': {'sconcso4': {'2000–2010': 0.034,
                                          '2000–2015': 0.037},
                             'wetso4': {'1990–2000': 0.32,
                                        '1990–2015': 0.05,
                                        '2000-2010': 0.37,
                                        '2000-2015': 0.24
                                        },
                             'sconcso2': {'2000–2010': 0.119,
                                          '2000–2015': 0.186}},

               'Africa': {'wetso4': {'2000-2010': 0},

                          'sconcso2': {'2000–2010': 0.121,
                                       '2000–2015': 0.068
                                       }}
               }

regions_nr_stations = {'N-America': {"sconcso4": {'1990–2000': 101,
                                          '1990–2015': 124,
                                          '2000-2010': 227,
                                          '2000–2015': 218},

                             "wetso4": {'1980-1990': 78,
                                        '1990–2000': 186,
                                        '1990–2015': 189,
                                        '2000–2010': 226,
                                        '2000–2015': 215
                                        },

                             'sconcso2': {'1990–2000': 53,
                                          '1990–2015': 71,
                                          '2000–2010': 78,
                                          '2000–2015': 77
                                          }},

               'Europe': {'sconcso4': {'1980–1990': 16,
                                       '1990–2000': 41,
                                       '1990–2015': 33,
                                       '2000–2010': 227,
                                       '2000–2015': 36},

                          'wetso4': {'1980–1990': 23,
                                     '1990–2000': 60,
                                     '1990–2015': 55,
                                     '2000–2010': 73,
                                     '2000–2015': 67

                                     },
                          'sconcso2': {'1980–1990': 20,
                                       '1990–2000': 43,
                                       '1990–2015': 40,
                                       '2000–2010': 51,
                                       '2000–2015': 47
                                       },
                          },
               'India': {'wetso4': {'1980–1990': 10,
                                    '1990–2000': 10,
                                    '2000–2010': 10,
                                    },
                         },
                # TODO fill out the rest of the stations.
               'East-Asia': {'sconcso4': {'2000–2010': 0.034,
                                          '2000–2015': 0.037},
                             'wetso4': {'1990–2000': 0.32,
                                        '1990–2015': 0.05,
                                        '2000-2010': 0.37,
                                        '2000-2015': 0.24
                                        },
                             'sconcso2': {'2000–2010': 0.119,
                                          '2000–2015': 0.186}},

               'Africa': {'wetso4': {'2000-2010': 0},

                          'sconcso2': {'2000–2010': 0.121,
                                       '2000–2015': 0.068
                                       }}
               }



def create_region(region):
    """
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

    # TODO ask Jonas 1) python functions split into seasons. 2) MAybee for augustin but if they have implemented the theil slope or if they use a python package.

    # TODO check that it contains only one variable --> else raise not implemented yet. This will happen anyways.

    valid_names = ['N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', 'Central-Europe', 'Most-East-Asia']2
    if region in valid_names:
        minLon, maxLon, minLat, maxLat = create_region(region = region)
        croppped_ungridded = ungridded.filter_by_meta(latitude=(minLat, maxLat), longitude=(minLon, maxLon))
        return croppped_ungridded
    else:
        raise ValueError("{} is not a valid region. "
                         "Try 'N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', "
                         "'Central-Europe', 'Most-East-Asia' ".format(region))

#def filter_by_time(data_cropped_by_region, start, stop):
    #station_list = data_dict.stats
    #print(data_dict.keys())
    #return data_dict


def test_trends_slope(variable = "sconcso2", start, stop, region):
    # TODO fill in content from aas et al notebook




    pass

def years_to_string(start, stop):
    """Function to make it simpler to retrieve testdata from dictionary."""
    return "{}-{}".format(start, stop)

def calc_yearly_average(one_station):
    """ Calculated yearly averages based on the below conditions.

        Conditions for calculting the averages:
            1. Need five daily measurments per season to calculate a seasonal average
            2. Require four seasons to calculate yearly average.
                2.2 Yearly average is the mean of the seasonal averages.
            3. Require at least 7 years to calculate a trend. (Sould be a condition in the theil inst4eds????

        Definition of seasons:
        Spring: March, April, May
        Summer: June, July, August
        Autumn: September, October, November
        Winter: December (Year-1), January, February

        Parameters:
        -------------------
        ungridded : UngriddedData
            TODO should this be stations instead.


        Returns:
        ---------------
        yearly_averages : array-like
            List contaning
        return: list containing the yearly averages for one station < less than 7 averages remove station.
    """
    pass


def theil_sen_estimator(y):
    """
    Calculates one slope for one station. This is the median lsope of all combinations for that station

    Calc all possible slopes (a in y = ax+b) and use the median.
    For futher reading check out; https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator

    Conditions:
        1. Exit yearly averages for at lest 7/10 years in the periode.
            1.1 Sesonal averages need to exit for all four seasons in order to calc the yearly mean.
            Which is the average og the seasonal means.
        2. Only calc trends for a period if 7 years of this contain yearly averages

    remember to use numpy functionality that doesn't included nans when taking the average

    :param

    y array-like
    list_yearly_average


    x = None --> set to be the np.arange(len(y))

    :return: a
        the slope of the trend using Theil-Sen regression (more robust against outliers).
        READ;
    """

    if len(y) >= 7:
        medslope, medintercept, lo_slope, up_slope = stats.theilslopes(y=y, x=None, 0.90)
    else:
        raise SomethingError
    # Compute the slope, intercept and 90% confidence interval (this is the same as a confidence level of p=0.010).

    # TODO : only check the slope not the std' currently I don't find python functionality which will give me all slopes.

    # TODO compute the std's from this here.

    pass


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


def test_nr_stations():
    """
    Check if the number of stations present is only counting the ones with more than 7 years of averges.
    :return: Boolean
    """
    pass


def test_ungriddeddata_surface_cons_so2():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read()  # read all variables
    assert len(data.station_name) == 629
    #assert 'n/a' in data.data_revision not woriking
    assert data.shape == (1008552, 12)


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