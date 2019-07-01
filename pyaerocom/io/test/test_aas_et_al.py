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

VARS = ['sconcso4', 'sconcso2']

# TODO add test or remove unoitconversion to inclkude 'wetso4',

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


def calc_yearly_average(one_station):
    """ Only do this is you have values from all seasons
        1) calc sesonal average
        2) calc yearly average from seasonal avergaes
        return: list containing the yearly averages for one station < less than 7 averages remove station.
    """
    pass

def calc_trend(list_yearly_average):
    """
    Only calc trends for a period if 7 years of this contain yearly averages

    remember to use numpy functionality that doesn't included nans when taking the average

    :param list_yearly_average:
        contains yearly averages, if not all seasons present --> np.nan
    :return: a
        the slope of the trend using Theil-Sen regression (more robust against outliers).
        READ; https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator
    """
    pass


def std(list_of_a):
    """ The standard deviation of the slopes. One per station in the period?.
    Double check the last things. 
    """
    pass

def check_nr_stations():
    """
    Check if the number of stations present is only counting the ones with more than 7 years of averges.
    :return: Boolean
    """
    pass

def create_region(region):
    """
    Function to create regions

    :param region:
    :return:
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


def crop_data_to_region(ungridded, region = "N-America"):
    """ Function which crops the data into correct regions."""
    valid_names = ['N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', 'Central-Europe', 'Most-East-Asia']
    if region in valid_names:
        minLon, maxLon, minLat, maxLat = create_region(region = region)
        return ungridded.filter_by_meta(latitude=(minLat, maxLat), longitude=(minLon, maxLon))
    else:
        raise ValueError("{} is not a valid region. "
                         "Try 'N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India', 'East-US', "
                         "'Central-Europe', 'Most-East-Asia' ".format(region))

#def filter_by_time(data_cropped_by_region, start, stop):
    #station_list = data_dict.stats
    #print(data_dict.keys())
    #return data_dict


def test_trends():
    # TODO fill in content from aas et al notebook
    pass





def test_ungriddeddata_surface_cons_so2():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read()  # read all variables
    assert len(data.station_name) == 890
    #assert 'n/a' in data.data_revision not woriking
    assert data.shape == (436121, 12)
    

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