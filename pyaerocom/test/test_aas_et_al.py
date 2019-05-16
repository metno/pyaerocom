# -*- coding: utf-8 -*-

"""
High level test methods that check EBAS time series data for selected stations
Created on Thu Apr 12 14:45:43 2018

@author: hannas
"""
import pytest
import numpy.testing as npt
import numpy as np
from pyaerocom.test.settings import lustre_unavail, TEST_RTOL
from pyaerocom.io import ReadSulphurAasEtAl


def _true_std():
        # Mesuring this: Absolute annual trend (STD) μgS/m3 year
        regions_std = {'N-America': {"sconcso4": {'1990–2000': 0.025, 
                                              '1990–2015': 0.024, 
                                              '2000-2010': 0.029, 
                                              '2000–2015': 0.029},
                                     
                                    "wetso4":{'1980-1990': 0.18,
                                              '1990–2000': 0.13,
                                              '1990–2015': 0.10,
                                              '2000–2010': 0.13, 
                                              '2000–2015': 0.13 
                                            },
                                    
                                 'sconcso2':{ '1990–2000': 0.115,
                                              '1990–2015': 0.109,
                                              '2000–2010': 0.113,
                                              '2000–2015': 0.123 
                                             }},
                                        
                                        
                          'Europe': { 'sconcso4':  {'1980–1990': 0.094, 
                                                      '1990–2000': 0.052, 
                                                      '1990–2015': 0.015,
                                                      '2000–2010': 0.041,
                                                      '2000–2015': 0.028},
                                    'wetso4':{'1980–1990': 0.36,
                                              '1990–2000': 0.29, 
                                              '1990–2015': 0.12,
                                              '2000–2010': 0.13,
                                              '2000–2015': 0.10
                                            
                                            },
                                    'sconcso2':{ '1980–1990': 0.168, 
                                                '1990–2000': 0.275,
                                                  '1990–2015': 0.085,
                                                  '2000–2010': 0.054,
                                                  '2000–2015': 0.036 
                                                   },
                                    },
                             'India':{ 'sconcso4':  {'1980–1990': 3.10, 
                                                      '1990–2000': 2.11, 
                                                      '1990–2015': 0.69, 
                                                      '2000–2015': 2.03},
                                    'wetso4':{'1980–1990': 0.18,
                                              '1990–2000': 0.37, 
                                              '2000–2010': 0.37,
                                            },
                                    },
                                     
                    'East-Asia': {'sconcso4':  {'2000–2010': 0.034, 
                                                '2000–2015': 0.037},
                                            'wetso4':{'1990–2000': 0.32, 
                                                      '1990–2015': 0.05,
                                                      '2000-2010': 0.37,
                                                      '2000-2015': 0.24 
                                                    },
                                            'sconcso2':{'2000–2010': 0.119,
                                                        '2000–2015': 0.186}},
                 
                    'Africa':{ 'wetso4':{'2000-2010':0 },
                                                    
                                'sconcso2':{  '2000–2010': 0.121,
                                              '2000–2015': 0.068
                                               }}
                }
        return regions_std

def def_regions(region):
    regions = {
        #'US': {'minLat': 22.5, 'maxLat': 71.0, 'minLon': -167, 'maxLon': -59.6},
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
    if region in regions:
        [minLat, maxLat, minLon, maxLon] = [regions[region][key] for key in regions[region]]
    else:
        print('unknown region: ',region)
        minLat, maxLat, minLon, maxLon = 0, 0, 0, 0
    return minLat, maxLat, minLon, maxLon

def _find_area(lat,lon,typ):
    #print(lat,lon,type(lat), type(lon))
    #list of regions
    if typ=='region':
        regions = ['N-America', 'S-America', 'Europe', 'East-Asia', 'Africa', 'India']
    elif typ == 'subregion':
        regions = ['East-US', 'Central-Europe', 'Most-East-Asia']
    #check if coo in the box
    area = np.nan
    for region in regions:
        [minLat, maxLat, minLon, maxLon] = def_regions(region)
        if float(lat)>=minLat and float(lat)<=maxLat and float(lon)>=minLon and float(lon)<=maxLon:
            area = region
    return area


def test_ungriddeddata_surface_cons_so2():
    reader = ReadSulphurAasEtAl('GAWTADsubsetAasEtAl')
    data = reader.read() # read all variables
    assert len(data.station_name) == 629
    assert 'n/a' in data.data_revision
    assert data.shape == (1008552, 12)

    # TODO : FILTER THIS REGION AND CALCULATE STDs.    

if __name__=="__main__":
   # pya.change_verbosity('info')
    #import sys
    test_ungriddeddata_surface_cons_so2()
# =============================================================================
#     
#     d = _make_data()
#     stat = d.to_station_data('Jung*', start=2008, stop=2011, freq='monthly')
#     stat.plot_timeseries('scatc550aer')
#     
# =============================================================================
    #pytest.main(sys.argv)