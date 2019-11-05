#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 09:29:23 2018

@author: jonasg
"""
import pytest
import os
from .synthetic_data import DataAccess
from pyaerocom import const, GEONUM_AVAILABLE

if 'etopo1' in const.SUPPLDIRS and os.path.exists(const.SUPPLDIRS['etopo1']):
    ETOPO1_AVAIL = True
else:
    ETOPO1_AVAIL = False

TEST_RTOL = 1e-4

DATA_ACCESS = DataAccess()
### GLOBAL MARKERS THAT CAN BE IMPORTED AND USED THROUGHOUT THE TEST SESSION
# custom skipif marker that is used below for test functions that 
# require geonum to be installed
lustre_unavail = pytest.mark.skipif(not const.has_access_lustre,
                                    reason='Skipping tests that require access '
                                    'to AEROCOM database on METNo servers')

# custom skipif marker that is used below for test functions that 
# require geonum to be installed
geonum_unavail = pytest.mark.skipif(not GEONUM_AVAILABLE,
                   reason='Skipping tests that require geonum. srtm.py library is '
                   'not installed')
etopo1_unavail = pytest.mark.skipif(not ETOPO1_AVAIL,
                   reason='Skipping tests that require geonum. srtm.py library is '
                   'not installed')

always_skipped = pytest.mark.skipif(True==True, reason='Seek the answer')

test_not_working = pytest.mark.skip(reason='Method raises Exception')


@always_skipped
def test_that_fails_but_should_be_skipped():
    assert 1==42