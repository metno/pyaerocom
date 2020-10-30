#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 12:58:34 2020

@author: jonasg
"""

import pytest
from pyaerocom.conftest import testdata_unavail
from pyaerocom.io.aerocom_browser import AerocomBrowser

@testdata_unavail
@pytest.mark.parametrize('searchstr,endswith', [
    ('TM5*TEST', 'modeldata/TM5-met2010_CTRL-TEST/renamed'),
    ('AeronetSunV3L2Subset.daily', 'obsdata/AeronetSunV3Lev2.daily/renamed')
    ])
def test_find_data_dir(searchstr, endswith):
    browser = AerocomBrowser()

    data_dir = browser.find_data_dir(searchstr)
    assert data_dir.endswith(endswith)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
