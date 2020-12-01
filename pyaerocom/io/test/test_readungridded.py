#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest
from pyaerocom import const
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.io import ReadUngridded


def test_invalid_init_data_dir():
    with pytest.raises(ValueError):
        ReadUngridded(['EBASMC', 'GHOST.EEA.daily'], data_dir='/bla/blub')

def test_supported():
    supported_datasets =ReadUngridded().supported_datasets
    print(supported_datasets)
    assert len(supported_datasets) >= 17
    assert all(x in supported_datasets for x in ['AeronetInvV3Lev2.daily',
                                                 'AeronetInvV3Lev1.5.daily',
                                                 'AeronetInvV3L2Subset.daily',
                                                 'AeronetInvV2Lev2.daily',
                                                 'AeronetInvV2Lev1.5.daily',
                                                 'AeronetSDAV2Lev2.daily',
                                                 'AeronetSDAV3Lev1.5.daily',
                                                 'AeronetSDAV3Lev2.daily',
                                                 'AeronetSDAV3L2Subset.daily',
                                                 'AeronetSunV2Lev2.daily',
                                                 'AeronetSunV2Lev2.AP',
                                                 'AeronetSunV3Lev1.5.daily',
                                                 'AeronetSunV3Lev1.5.AP',
                                                 'AeronetSunV3Lev2.daily',
                                                 'AeronetSunV3Lev2.AP',
                                                 'AeronetSunV3L2Subset.daily',
                                                 'EARLINET',
                                                 'EBASMC',
                                                 'EBASSubset',
                                                 'DMS_AMS_CVO',
                                                 'GAWTADsubsetAasEtAl',
                                                 'GHOST.EEA.monthly',
                                                 'GHOST.EEA.hourly',
                                                 'GHOST.EEA.daily',
                                                 'GHOST.EBAS.monthly',
                                                 'GHOST.EBAS.hourly',
                                                 'GHOST.EBAS.daily'])


@pytest.mark.parametrize('dsr,vtr,oc,fp,kw,nst,nmeta,raises,caching', [
    ('AeronetSunV3L2Subset.daily', 'od550aer',False,None,{},22,22,
     does_not_raise_exception(),False),
    ('AeronetSunV3L2Subset.daily', 'od550aer', False,
     dict(station_name='La_Paz'),{},1, 1,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', 'od550aer', False,
     dict(station_name=['La_Paz', 'AAO*']),{},2, 2,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', ['od550aer'], False,
     dict(altitude=[1000, 10000],
          ignore_station_names=dict(od550aer='La_Paz')),{},2, 2,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', ['od550aer', 'ang4487aer'], False,
     dict(altitude=[1000, 10000],
          ignore_station_names=dict(od550aer='La_Paz')),{},2, 2,
     pytest.raises(NotImplementedError),True),
    ('AeronetSunV3L2Subset.daily', 'od550aer',True,None,{},22,22,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', 'od550aer',True,
     dict(altitude=[1000, 10000]),{},3,3,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', 'od550aer', False,
     dict(altitude=[1000, 10000],
          ignore_station_names='La_*'),{},2, 2,
     does_not_raise_exception(),True),
    ('AeronetSunV3L2Subset.daily', 'od550aer', False,
     dict(altitude=[1000, 10000],
          ignore_station_names=['La_*', 'Mauna_Loa']),{},1, 1,
     does_not_raise_exception(),True)

    ])
def test_ReadUngridded_read(dsr,vtr,oc,fp,kw,nst,nmeta,raises,caching):
    reader = ReadUngridded()

    const.CACHING = False if not caching else True
    with raises:
        data = reader.read(datasets_to_read=dsr,
                           vars_to_retrieve=vtr,
                           only_cached=oc,
                           filter_post=fp,
                           **kw)

        assert len(data.metadata) == nmeta
        assert len(data.unique_station_names) == nst

    const.CACHING = True

def test_basic_attributes():
    reader = ReadUngridded()
    assert not reader.ignore_cache
    assert reader.datasets_to_read == []
    with pytest.raises(ValueError):
        reader.get_reader()
    with pytest.raises(ValueError):
        reader.dataset_provides_variables()

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
