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
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom import VerticalProfile

FILES = ['ev1008192050.e532',
         'ev1009162031.e532',
         'ev1012131839.e532',
         'ev1011221924.e532',
         'ev1105122027.e532']

@lustre_unavail
def get_test_paths():
    from pyaerocom import const
    testdir = os.path.join(const.OBSLOCS_UNGRIDDED['EARLINET'], 'ev')
    return [os.path.join(testdir, f) for f in FILES]

@lustre_unavail
def test_all_files_exist():
    for file in get_test_paths():
        if not os.path.exists(file):
            raise AssertionError('File {} does not exist'.format(file))

@lustre_unavail
def test_first_file():
    read = ReadEarlinet()
    paths = get_test_paths()
    read.files = paths

    stat = read.read_file(paths[0], 'ec532aer')

    assert 'data_level' in stat
    assert 'wavelength_det' in stat
    assert 'has_zdust' in stat
    assert 'eval_method' in stat

    assert 'ec532aer' in stat.var_info

    i = stat.var_info['ec532aer']
    assert i['unit_ok']
    assert i['err_read']
    assert i['outliers_removed']

    assert isinstance(stat.ec532aer, VerticalProfile)

    p = stat.ec532aer

    vals_data = [np.nanmean(p.data), np.nanstd(p.data), np.sum(np.isnan(p.data)),
                 len(p.data)]
    vals_dataerr = [np.nanmean(p.data_err), np.nanstd(p.data_err)]
    vals_altitude = [np.min(p.altitude), np.max(p.altitude)]

    npt.assert_allclose(vals_data,[4.463068618148296, 1.8529271228530515, 216, 253],
                        rtol=TEST_RTOL)
    npt.assert_allclose(vals_dataerr, [4.49097234883772, 0.8332285038985179],
                        rtol=TEST_RTOL)
    npt.assert_allclose(vals_altitude, [331.29290771484375, 7862.52490234375],
                        rtol=TEST_RTOL)

@lustre_unavail
def test_read_ungridded():
    read = ReadEarlinet()
    read.files = get_test_paths()

    data = read.read('ec532aer')

    npt.assert_equal(len(data.metadata), 5)
    npt.assert_array_equal(data.shape, (786, 12))

    npt.assert_allclose([np.nanmin(data._data[:, data._DATAINDEX]),
                         np.nanmean(data._data[:, data._DATAINDEX]),
                         np.nanmax(data._data[:, data._DATAINDEX])],
                        [-0.440742, 24.793547, 167.90787], rtol=TEST_RTOL)

    merged = data.to_station_data('Evora', freq='monthly')

    npt.assert_allclose([float(np.nanmin(merged.ec532aer)),
                         float(np.nanmean(merged.ec532aer)),
                         float(np.nanmax(merged.ec532aer))],
                        [0.220322,  23.093238, 111.478665],
                        rtol=TEST_RTOL)

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
