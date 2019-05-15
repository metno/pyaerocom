#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level test methods that check EBAS time series data for selected stations
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy.testing as npt
import numpy as np
from pyaerocom.test.settings import lustre_unavail, TEST_RTOL
from pyaerocom.io import ReadEbas

def _make_data():
    r = ReadEbas()
    return r.read('scatc550aer', station_names='Jungfrau*')

@pytest.fixture(scope='module')
def data_scat_jungfraujoch():
    return _make_data()

@lustre_unavail
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
                            [np.datetime64('1995-07-08T23:00:00'), 
                             np.datetime64('2017-12-31T23:00:00')])
    
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