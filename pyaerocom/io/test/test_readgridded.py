#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

# TODO: Docstrings
import pytest
import numpy.testing as npt
from pandas import Timestamp, DataFrame
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.io.readgridded import ReadGridded

START = "1-1-2003"
STOP = "31-12-2007"

def init_reader():
    return ReadGridded(data_id="ECMWF_CAMS_REAN")

@lustre_unavail
@pytest.fixture(scope='session')
def reader_reanalysis():
    return init_reader()
    
def test_ReadGridded_class_empty():
    r = ReadGridded()
    assert r.data_id == None
    assert r.data_dir == None
    from pyaerocom.io.aerocom_browser import AerocomBrowser
    assert isinstance(r.browser, AerocomBrowser)
    
    failed = False
    try:
        r.years_avail
    except AttributeError:
        failed = True
    assert failed
    assert r.vars == []  
    
@lustre_unavail    
def test_file_info(reader_reanalysis):
    assert isinstance(reader_reanalysis.file_info, DataFrame)
    assert len(reader_reanalysis.file_info.columns) == 11, 'Mismatch colnum file_info (df)'

@lustre_unavail    
def test_years_available(reader_reanalysis):
    years = list(range(2003, 2020)) + [9999]
    npt.assert_array_equal(reader_reanalysis.years_avail, years)    

@lustre_unavail
def test_data_dir(reader_reanalysis):
    assert reader_reanalysis.data_dir == '/lustre/storeA/project/aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed'
    
@lustre_unavail    
def test_read_var(reader_reanalysis):
    from numpy import datetime64
    d = reader_reanalysis.read_var(var_name="od550aer", ts_type="daily",
                         start=START, stop=STOP)
    
    from pyaerocom import GriddedData
    assert isinstance(d, GriddedData)
    npt.assert_array_equal([d.var_name, sum(d.shape), d.start, d.stop],
                           ["od550aer", 1826 + 161 + 320,
                            datetime64('2003-01-01T00:00:00.000000'),
                            datetime64('2007-12-31T23:59:59.999999')])
    vals = [d.longitude.points[0],
            d.longitude.points[-1],
            d.latitude.points[0],
            d.latitude.points[-1]]
    nominal = [-180.0, 178.875, 90.0, -90.0]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d

@lustre_unavail
def test_prefer_longer(reader_reanalysis):
    daily = reader_reanalysis.read_var('od550aer', ts_type='monthly', 
                             flex_ts_type=True,
                             prefer_longer=True)
    assert daily.ts_type == 'daily'
    
@lustre_unavail
def test_read_vars(reader_reanalysis):
    data = reader_reanalysis.read(['od440aer', 'od550aer', 'od865aer'], 
                        ts_type="daily", start=START, stop=STOP)
    vals = [len(data),
            sum(data[0].shape),
            sum(data[1].shape),
            sum(data[2].shape)]
    nominal = [3, 2307, 2307, 2307]
    npt.assert_array_equal(vals, nominal)
    # this was removed as mean values of GriddedData objects should not be
    # tested here
# =============================================================================
#     vals = [data[0][1825].mean(), 
#             data[1][1825].mean(), 
#             data[2][1825].mean()]
#     #nominal = [0.11754113, 0.09734518, 0.06728536]
#     # updated on 25.11.2019 since now by default area weighted mean is used
#     nominal = [0.14793, 0.12195, 0.08345]
#     npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
# =============================================================================
    

    
if __name__=="__main__":
    pytest.main(['./test_readgridded.py'])
    
    