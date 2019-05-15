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

def _make_data():
    r = ReadSulphurAasEtAl()
    vars_to_retrieve = ["wetso4", "sconcso2", "sconcso4"]
    # IDEA TO DO THIS FOR seperate data. 
    return r.read( vars_to_retrieve = vars_to_retrieve)

"""
OBS OBS: STD for wetso4 is in a different unit, its in the original one. 

"""



def _true_std():
        regions = {
        'N-America': {"sconcso4": {'1990–2000': , 
                                  '1990–2015': , 
                                  '2000-2010': , 
                                  '2000–2015': },
                         
                        "wetso4":{ '1980-1990': ,
                                '1990–2015' : ,
                                '2000–2010': , 
                                }
                        
                     'sconcso4':{ '1990–2000': ,
                                  '1990–2015': ,
                                  '2000–2010': ,
                                  '2000–2015': 
                                 }
    
    }
        'Europe':    {'1980–1990': 3.10, 
                      '1990–2000': 2.11, 
                      '1990–2015': 0.69, 
                      '2000–2015': 2.03},
                   
        'East-Asia': {#'1980–1990': 3.10, 
                      #'1990–2000': 2.11, 
                      '2000-2010': 4.25, 
                      '2000–2015': 9.41},
        #'Africa': ,
        'India': ,
        #'East-US': ,
        #'Central-Europe': ,
        #'Most-East-Asia': ,
        #'World': ,
        #'': 0,
    }


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


def test_ungriddeddata_jungfraujoch(data_scat_jungfraujoch):
    data = data_scat_jungfraujoch
    assert 'EBASMC' in data.data_revision
    assert data.data_revision['EBASMC'] == '20190319'
    assert data.shape == (227928, 12)
    assert len(data.metadata) == 26
    
    unique_coords = []
    unique_coords.extend(np.unique(data.latitude))
    unique_coords.extend(np.unique(data.longitude))
    unique_coords.extend(np.unique(data.altitude))
    assert len(unique_coords) == 4
    npt.assert_allclose(unique_coords, [46.5475, 7.985, 3578.0, 3580.0],
                        rtol=TEST_RTOL)
    
    vals = data._data[:, data.index['data']]
    check = [np.nanmean(vals), 
             np.nanstd(vals),
             np.nanmax(vals),
             np.nanmin(vals)]
    print(check)
    npt.assert_allclose(check, 
                        [4.433951143197965, 
                         7.398103000409265, 182.7, -5.574], rtol=TEST_RTOL)

@lustre_unavail   
def test_scat_jungfraujoch(data_scat_jungfraujoch):
    stat = data_scat_jungfraujoch.to_station_data('Jung*')
    
    keys = list(stat.keys())
    
    assert 'scatc550aer' in stat.overlap
    assert len(stat.overlap['scatc550aer']) == 17466
    assert stat['stat_merge_pref_attr'] == 'revision_date'
    npt.assert_array_equal(keys, 
                           ['dtime', 
                            'var_info',
                            'station_coords',
                            'data_err', 
                            'overlap', 
                            'filename', 
                            'station_id', 
                            'station_name', 
                            'instrument_name', 
                            'PI', 'country', 
                            'ts_type', 
                            'latitude', 
                            'longitude', 
                            'altitude', 
                            'data_id', 
                            'dataset_name', 
                            'data_product', 
                            'data_version', 
                            'data_level', 
                            'revision_date', 
                            'ts_type_src', 
                            'stat_merge_pref_attr',
                            'data_revision',
                            'scatc550aer'])
   
    npt.assert_array_equal([stat.dtime.min(), stat.dtime.max()],
                            [np.datetime64('1995-07-08T23:29:59'), 
                             np.datetime64('2017-12-31T23:29:59')])
    
    vals = [stat['instrument_name'], stat['ts_type'], stat['PI'],
            len(stat.filename.split(';'))]
    print(vals)
    
    npt.assert_array_equal(vals,
                           ['IN3563; Ecotech_Aurora3000_JFJ_dry; TSI_3563_JFJ_dry', 
                            'hourly', 
                            'Baltensperger, Urs; Weingartner, Ernest; Bukowiecki, Nicolas', 
                            26])
    
    d = stat.scatc550aer
    vals = [d.mean(), d.std(), d.min(), d.max()]
    npt.assert_allclose(vals,
                         [4.7192396520408515, 7.702181266525312, -5.574, 182.7],
                         rtol=TEST_RTOL)
    
    d = stat.overlap['scatc550aer']
    vals = [d.mean(), d.std(), d.min(), d.max()]
    npt.assert_allclose(vals,
                         [2.662519,  4.303533, -3.468499, 54.971412], rtol=TEST_RTOL)

@lustre_unavail   
def test_scat_jungfraujoch_subset(data_scat_jungfraujoch):
    
    stat = data_scat_jungfraujoch.to_station_data('Jung*', 
                                                  start=2008, stop=2011, 
                                                  freq='monthly')
    
    npt.assert_array_equal([stat.dtime.min(), stat.dtime.max()],
                            [np.datetime64('2008-01-15'),
                             np.datetime64('2010-12-15') ])
    assert stat.ts_type == 'monthly'
    assert stat.ts_type_src == 'hourly'
    
    d = stat['scatc550aer']
    vals = [d.mean(), d.std(), d.min(), d.max()]

    npt.assert_allclose(vals, 
                        [4.267739428649354, 3.535263046555806, 
                         0.12036760000000003, 11.898275310344818],
                         rtol=TEST_RTOL)
    
if __name__=="__main__":
   # pya.change_verbosity('info')
    #import sys
    d = _make_data()
    test_ungriddeddata_jungfraujoch(d)
    test_scat_jungfraujoch(d)
    test_scat_jungfraujoch_subset(d)
# =============================================================================
#     
#     d = _make_data()
#     stat = d.to_station_data('Jung*', start=2008, stop=2011, freq='monthly')
#     stat.plot_timeseries('scatc550aer')
#     
# =============================================================================
    #pytest.main(sys.argv)