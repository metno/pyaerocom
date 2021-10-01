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

    keys_sorted = ['data_id', 'data_level', 'data_product', 'data_version',
                   'dataset_name', 'framework', 'instr_vert_loc',
                   'revision_date', 'stat_merge_pref_attr', 'ts_type_src',
                   'website']
    assert sorted(list(ds.keys())) == keys_sorted
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
        'country_code',
        'data_id',
        'data_level',
        'data_product',
        'data_version',
        'dataset_name',
        'filename',
        'framework',
        'instr_vert_loc',
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

@pytest.mark.parametrize('data_id,values,test_addstuff', [
    ('NorESM2-met2010_AP3-CTRL', ['NorESM2', 'met2010', 'AP3', 'CTRL'], True),
    ('Blaaa', ['Blaaa', '', '', ''], False),
    ('Bla-blub2010_blablub-bla', ['Bla-blub2010', '', 'blablub', 'bla'], False),
    ('Bla-met2042_blablub-bla', ['Bla', 'met2042', 'blablub', 'bla'], False)

     ])
def test_aerocomdataid(data_id, values, test_addstuff):

    data_id = mst.AerocomDataID(data_id)

    assert data_id.values == values

    if test_addstuff:
        dd = data_id.to_dict()

        assert dd['model_name'] == values[0]
        assert dd['meteo'] == values[1]
        assert dd['experiment'] == values[2]
        assert dd['perturbation'] == values[3]

        data_id1 = mst.AerocomDataID(**dd)

        assert data_id1 == str(data_id)
        assert data_id1 == data_id
        assert data_id1 == 'NorESM2-met2010_AP3-CTRL'

        assert mst.AerocomDataID(**dd) == mst.AerocomDataID.from_dict(dd)

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
