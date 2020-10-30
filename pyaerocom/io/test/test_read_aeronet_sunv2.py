#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import numpy.testing as npt
import numpy as np
import os
from pyaerocom.conftest import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2

@lustre_unavail
def test_load_berlin_AeroSunV2L2D():
    reader = ReadAeronetSunV2()
    files = reader.find_in_file_list('*Berlin*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == '920801_180519_Berlin_FUB.lev20'
    data = reader.read_file(files[0],
                            vars_to_retrieve=['od550aer'])

    test_vars = ['od440aer',
                 'od500aer',
                 'od550aer',
                 'ang4487aer']

    assert all([x in data for x in test_vars])

    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])

    assert isinstance(data['dtime'][0], np.datetime64)
    assert data['dtime'][0] == np.datetime64('2014-07-06T00:00:00')

    first_vals = [data[var][0] for var in test_vars]

    nominal = [0.229427, 0.18302 , 0.151227, 2.002052]
    npt.assert_allclose(actual=first_vals, desired=nominal, rtol=TEST_RTOL)

if __name__=="__main__":
    test_load_berlin_AeroSunV2L2D()
