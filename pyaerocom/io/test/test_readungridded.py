#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest
from pyaerocom.conftest import lustre_unavail
from pyaerocom.io import ReadUngridded

def test_supported():
    supported_datasets =ReadUngridded().supported_datasets
    assert len(supported_datasets) == 21

@lustre_unavail
def test_basic_attributes():
    r = ReadUngridded()
    assert not r.ignore_cache
    assert r.datasets_to_read == ['AeronetSunV3Lev2.daily']
    assert type(r.get_reader()).__name__ == 'ReadAeronetSunV3'
    assert r.dataset_provides_variables() == ['od340aer', 'od440aer',
                                              'od500aer', 'od870aer',
                                              'ang4487aer', 'ang4487aer_calc',
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
    


    