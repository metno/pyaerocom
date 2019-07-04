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

def test_revision_dates():
    f = ReadUngridded()
    l = {}
    for s in f.SUPPORTED:
        r = s()
        l[r.DATA_ID] = r.data_revision
    
    ids = list(l.keys())
    revs = list(l.values())
    npt.assert_array_equal(ids, ['AeronetInvV3Lev2.daily', 
                                 'AeronetInvV2Lev2.daily',
                                 'AeronetSDAV2Lev2.daily', 
                                 'AeronetSDAV3Lev2.daily',
                                 'AeronetSunV2Lev2.daily', 
                                 'AeronetSunV3Lev2.daily', 
                                 'EARLINET',
                                 'EBASMC',
                                 'DMS_AMS_CVO',
                                 'GAWTADsubsetAasEtAl'])

    npt.assert_array_equal(revs, ['20190330', '20171216', '20180519', 
                                  '20190425', '20180519', '20190606', 
                                  '20190129', '20190530', '20190619',
                                  '20190522'])
    
if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
    #stat.plot_timeseries('scatc550aer')