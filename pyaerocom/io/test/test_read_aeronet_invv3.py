#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import numpy.testing as npt
import numpy as np

from pyaerocom.conftest import TEST_RTOL, lustre_unavail
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3

@lustre_unavail
def test_load_berlin():
    dataset = ReadAeronetInvV3()
    files = dataset.find_in_file_list('*Berlin*')
    assert len(files) == 1
    #assert os.path.basename(files[0]) == '19930101_20190914_Berlin_FUB.all'
    data = dataset.read_file(files[0],
                             vars_to_retrieve=['abs550aer'])

    test_vars = ['abs440aer', 'angabs4487aer', 'abs550aer']
    assert all([x in data for x in test_vars])

    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])

    assert isinstance(data['dtime'][0], np.datetime64)
    t0 = data['dtime'][0]

    assert t0 == np.datetime64('2014-07-07T12:00:00')

    first_vals = [np.nanmean(data[var]) for var in test_vars]

    # nominal = [0.014629, 0.908436, 0.012112] before 20/03/2020
    # nominal = [0.014570, 0.908349, 0.012069] before 05/12/2020
    nominal = [0.014458, 0.894376, 0.012001]
    npt.assert_allclose(actual=first_vals, desired=nominal, rtol=TEST_RTOL)

if __name__=="__main__":
    test_load_berlin()
