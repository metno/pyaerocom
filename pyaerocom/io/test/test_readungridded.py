#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest
from pyaerocom.conftest import lustre_unavail
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

@lustre_unavail
def test_basic_attributes():
    r = ReadUngridded('AeronetSunV3Lev2.daily')
    assert not r.ignore_cache
    assert r.datasets_to_read == ['AeronetSunV3Lev2.daily']
    assert type(r.get_reader()).__name__ == 'ReadAeronetSunV3'
    assert r.dataset_provides_variables() == ['od340aer', 'od440aer',
                                              'od500aer', 'od870aer',
                                              'ang4487aer', 'ang44&87aer',
                                              'od550aer']

@lustre_unavail
def test_read_aeronet_sunv3():
    r = ReadUngridded()
    data = r.read('AeronetSunV3Lev2.daily',
                   vars_to_retrieve=['od550aer', 'ang4487aer'],
                   file_pattern='Bo*')
    data._check_index()

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
