#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:05:50 2019

@author: paulinast
"""

import pytest
import numpy.testing as npt
import numpy as np
from pyaerocom.conftest import lustre_unavail, TEST_RTOL, test_not_working
from pyaerocom.io import ReadGAW

def _make_data():
    r = ReadGAW()
    return r.read('vmrdms')

@pytest.fixture(scope='module')
@lustre_unavail
def data_vmrdms_ams_cvo():
    return _make_data()

@lustre_unavail
@test_not_working
def test_ungriddeddata_ams_cvo(data_vmrdms_ams_cvo):
    data = data_vmrdms_ams_cvo
    # assert data.data_revision['DMS_AMS_CVO'] == 'n/a'
    assert data.shape == (819+7977, 12)
    assert len(data.metadata) == 2

    unique_coords = []
    unique_coords.extend(np.unique(data.latitude))
    unique_coords.extend(np.unique(data.longitude))
    unique_coords.extend(np.unique(data.altitude))
    assert len(unique_coords) == 6
    npt.assert_allclose(unique_coords, [-37.8, 16.848, -24.871, 77.53, 10.0, 65.0],
                        rtol=TEST_RTOL)

    vals = data._data[:, data.index['data']]
    check = [np.nanmean(vals),
             np.nanstd(vals),
             np.nanmax(vals),
             np.nanmin(vals)]
    print(check)
    #npt.assert_allclose(vals,
     #                    [174.8499921813917, 233.0328306938496, 2807.6, 0.0],
      #                   rtol=TEST_RTOL)

@lustre_unavail
@test_not_working
def test_vmrdms_ams(data_vmrdms_ams_cvo):
    stat = data_vmrdms_ams_cvo.to_station_data(meta_idx= 0)

    keys = list(stat.keys())
    assert 'vmrdms' in keys
    assert 'var_info' in keys

    npt.assert_array_equal([stat.dtime.min(), stat.dtime.max()],
                            [np.datetime64('1987-03-01T00:00:00.000000000'),
                             np.datetime64('2008-12-31T00:00:00.000000000')])

    vals = [stat['instrument_name'], stat['ts_type'], stat['filename']]

    npt.assert_array_equal(vals,
                           ['unknown',
                            'daily',
                            'ams137s00.lsce.as.fl.dimethylsulfide.nl.da.dat'])

    d = stat['vmrdms']
    vals = [d.mean(), d.std(), d.max(), d.min()]
    npt.assert_allclose(vals,
                         [185.6800736155262, 237.1293922258991, 2807.6, 5.1],
                         rtol=TEST_RTOL)

@lustre_unavail
def test_vmrdms_ams_subset(data_vmrdms_ams_cvo):

    stat = data_vmrdms_ams_cvo.to_station_data(meta_idx= 0,
                                               start=2000, stop=2008,
                                               freq='monthly')

    npt.assert_array_equal([str(stat.dtime.min()),
                            str(stat.dtime.max())],
                            ['2000-01-15T00:00:00.000000000',
                             '2007-12-15T00:00:00.000000000'])
    assert stat.ts_type == 'monthly'
    assert stat.ts_type_src == 'daily'

if __name__=="__main__":

    d = _make_data()
# =============================================================================
#     test_ungriddeddata_ams_cvo(d)
#     test_vmrdms_ams(d)
# =============================================================================
    test_vmrdms_ams_subset(d)
