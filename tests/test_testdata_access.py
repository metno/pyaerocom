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

@pytest.fixture(scope='module')
def td():
    return TestDataAccess()

def test_TestDataAccess(td):
    assert td._basedir is None
    assert str(td.basedir) == const.OUTPUTDIR
    assert os.path.basename(td.testdatadir) == 'testdata-minimal'
    with pytest.raises(AttributeError):
        td.testdatadir = '/home'

def test_TestDataAccess_add_paths(td):
    assert os.path.exists(td.testdatadir)
    for name, relpath in td.ADD_PATHS.items():
        assert td.testdatadir.joinpath(relpath).exists()

def test_TestDataAccess_check_access(td):
    assert td.check_access()
    assert not td.check_access(dict(bla='/blub'))

def test_TestDataAccess_init(td):
    assert td.init()

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)