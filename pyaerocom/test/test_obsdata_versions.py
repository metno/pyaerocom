#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level test that checks the revision dates of all observation datasets
that are registered in ReadUngridded factory class

@author: jonasg
"""
import pytest
import numpy.testing as npt
from pyaerocom.io import ReadUngridded

from pyaerocom.test.settings import lustre_unavail

@lustre_unavail
def test_revision_dates():
    f = ReadUngridded()
    l = {}
    for s in f.SUPPORTED:
        r = s()
        l[r.DATA_ID] = r.data_revision
    res = []
    order = sorted(list(l.keys()))
    for name in order:
        res.append([name, l[name]])

    npt.assert_array_equal(res, 
                           [['AeronetInvV2Lev2.daily', '20171216'], 
                            ['AeronetInvV3Lev2.daily', '20190914'], 
                            ['AeronetSDAV2Lev2.daily', '20180519'], 
                            ['AeronetSDAV3Lev2.daily', '20190920'], 
                            ['AeronetSunV2Lev2.daily', '20180519'], 
                            ['AeronetSunV3Lev2.daily', '20190920'], 
                            ['DMS_AMS_CVO', '20190807'], 
                            ['EARLINET', '20190129'], 
                            ['EBASMC', '20191001'], 
                            ['GAWTADsubsetAasEtAl', '20190522']])

    
if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
    #stat.plot_timeseries('scatc550aer')