#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest
import numpy.testing as npt
import numpy as np
import os
from pyaerocom.conftest import TEST_RTOL, testdata_unavail
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3

@testdata_unavail
def test_load_thessaloniki(aeronet_sda_subset_reader):
    reader = aeronet_sda_subset_reader
    files = reader.find_in_file_list('*Thessaloniki*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == 'Thessaloniki.lev30', files[0]

    test_vars = ['ang4487aer',
                 'od550aer',
                 'od550gt1aer',
                 'od550lt1aer']

    data = reader.read_file(files[0], vars_to_retrieve=test_vars)

    assert all([x in data for x in test_vars])

    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])

    assert isinstance(data['dtime'][0], np.datetime64)
    assert data['dtime'][0] == np.datetime64('2003-06-01T12:00:00'), data['dtime'][0]

    means = []
    for var in test_vars:
        means.append(np.nanmean(data[var]))

    desired = [1.4777584841303428, 0.1988665578854858, 0.036805761707404114,
               0.16206080598741934]

    npt.assert_allclose(actual=means,
                        desired = desired,
                        rtol=TEST_RTOL)

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
