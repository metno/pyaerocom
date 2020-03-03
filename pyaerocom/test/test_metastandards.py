#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:52:16 2020

@author: jonasg
"""
import pytest
from pyaerocom import metastandards as mst

def test_datasource_empty():
    ds = mst.DataSource()
    
    assert list(ds.keys()) == ['data_id',
                               'dataset_name',
                               'data_product',
                               'data_version',
                               'data_level',
                               'revision_date',
                               'website',
                               'ts_type_src',
                               'stat_merge_pref_attr']
    assert list(set(ds.values())) == [None]
    
@pytest.mark.parametrize('data_id,dataset_name,data_product,data_version,'
                          'data_level,revision_date,stat_merge_pref_attr',
                          [('AeronetSunV3Lev2.daily', 'AERONET', 'Sun', 3.0, 2.0, None, None),
                           ('EBASMC', 'EBAS', None, None, None, None, 'revision_date'),
                           ('EARLINET', 'EARLINET', None, None, None, None, None)])
def test_datasource(data_id, dataset_name, data_product, data_version, 
                    data_level, revision_date, stat_merge_pref_attr):
    
    ds = mst.DataSource(data_id=data_id)
    assert ds['dataset_name'] == dataset_name
    assert ds['data_product'] == data_product
    assert ds['data_version'] == data_version
    assert ds['data_level'] == data_level
    assert ds['revision_date'] == revision_date
    assert ds['stat_merge_pref_attr'] == stat_merge_pref_attr
    
def test_stationmetadata():
    meta=mst.StationMetaData()
    
    assert isinstance(meta, mst.DataSource)
    assert sorted(meta.keys(), key=str.casefold) == [
        'altitude',
        'country',
        'data_id',
        'data_level',
        'data_product',
        'data_version',
        'dataset_name',
        'filename',
        'instrument_name',
        'latitude',
        'longitude',
        'PI',
        'revision_date',
        'stat_merge_pref_attr',
        'station_id',
        'station_name',
        'ts_type',
        'ts_type_src',
        'website'
        ]
    
def test_aerocomdataid_invalid():
    try:
        mst.AerocomDataID('Blaaa')
    except ValueError as e:
        assert str(e) == 'Invalid data ID None. Need format <model-name>_<meteo-config>_<eperiment-name>'
        
    try:
        mst.AerocomDataID('Bla-blub2010_blablub-bla')
    except ValueError as e:
        assert str(e) == 'Meteo config string needs to start with met'
        
def test_aerocomdataid_valid():
    
    data_id = mst.AerocomDataID('NorESM2-met2010_CTRL-AP3')

    dd = data_id.to_dict()
    
    assert dd['model_name'] == 'NorESM2'
    assert dd['meteo'] == 'met2010'
    assert dd['experiment'] == 'CTRL'
    assert dd['perturbation'] == 'AP3'
    
    data_id1 = mst.AerocomDataID(**dd)
    
    assert data_id1 == str(data_id)
    assert data_id1 == data_id
    assert data_id1 == 'NorESM2-met2010_CTRL-AP3'
    
    assert mst.AerocomDataID(**dd) == mst.AerocomDataID.from_dict(dd)
    
if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
    
    
    meta=mst.StationMetaData()
    
# =============================================================================
#     data_ids = ['AeronetSunV3Lev2.daily', 'EBASMC', 'EARLINET']
#     keystr = ('data_id,dataset_name,data_product,data_version,'
#               'data_level,revision_date,stat_merge_pref_attr')
#     
#     results = []
#     for data_id in data_ids:
#         print(data_id)
#         res = []
#         for key in keystr.split(','):
#             ds = mst.DataSource(data_id=data_id)
#             res.append(ds[key])
#             
#         results.append(tuple(res))
# =============================================================================
            
        
    