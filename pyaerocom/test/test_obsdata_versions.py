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

from pyaerocom.conftest import lustre_unavail

obsdata_versions = [
    ['AeronetInvV2Lev2.daily', '20171216'],
    ['AeronetInvV3Lev2.daily', '20201205'],
    ['AeronetSDAV2Lev2.daily', '20180519'],
    ['AeronetSDAV3Lev2.daily', '20201207'],
    ['AeronetSunV2Lev2.daily', '20180519'],
    ['AeronetSunV3Lev2.daily', '20201207'],
    ['DMS_AMS_CVO', '20190807'],
    ['EARLINET', '20190129'],
    ['EBASMC', '20201204'],
    ['GAWTADsubsetAasEtAl', '20190522'],
    ['GHOST.EEA.daily', 'n/d']]

@lustre_unavail
def test_revision_dates():
    f = ReadUngridded()
    l = {}
    for s in f.SUPPORTED_READERS:
        r = s()
        l[r.DATA_ID] = r.data_revision
    res = []
    order = sorted(list(l.keys()))
    for name in order:
        res.append([name, l[name]])

    npt.assert_array_equal(res, obsdata_versions)

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
