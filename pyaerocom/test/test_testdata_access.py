#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:28:45 2020

@author: jonasg
"""

import pytest
import os
from pyaerocom import const
from pyaerocom.testdata_access import TestDataAccess

def test_TestDataAccess():
    td = TestDataAccess()
    assert td._basedir is None
    assert str(td.basedir) == const.OUTPUTDIR
    assert os.path.basename(td.testdatadir) == 'testdata-minimal'
    with pytest.raises(AttributeError):
        td.testdatadir = '/home'

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)