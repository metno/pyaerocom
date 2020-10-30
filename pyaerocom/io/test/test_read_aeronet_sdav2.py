#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest
import numpy.testing as npt
import numpy as np
import os
from pyaerocom.conftest import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2

@lustre_unavail
def test_load_berlin_AeroSdaV2L2D():
    reader = ReadAeronetSdaV2()
    files = reader.find_in_file_list('*Berlin*')
    assert len(files) == 1
    assert os.path.basename(files[0]) == '920801_180519_Berlin_FUB.ONEILL_20'

    test_vars = ['od870aer',
                 'ang4487aer',
                 'od550aer',
                 'od550gt1aer',
                 'od550lt1aer']

    data = reader.read_file(files[0],
                            vars_to_retrieve=test_vars)

    assert all([x in data for x in test_vars])

    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])

    assert isinstance(data['dtime'][0], np.datetime64)
    assert data['dtime'][0] == np.datetime64('2014-07-06T00:00:00')

    means = []
    for var in test_vars:

        means.append(data[var].mean())

    desired = [0.0671392659574468, 1.5027900015754372, 0.1338938495016503,
               0.02333982521802314, 0.11055405137562464]

    npt.assert_allclose(actual=means,
                        desired = desired,
                        rtol=TEST_RTOL)

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
