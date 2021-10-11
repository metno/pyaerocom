#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 19:31:51 2021

@author: jonasg
"""
import pytest
import os
from pyaerocom.exceptions import DataSearchError
from pyaerocom import tools
from getpass import getuser

from pyaerocom import const

def test_clear_cache(tmpdir):
    _cd = const.CACHEDIR
    try:
        user = getuser()
        cachebase = str(tmpdir.mkdir('_cache'))
        const.CACHEDIR = cachebase
        cachedir = f'{cachebase}/{user}'
        assert os.path.samefile(const.CACHEDIR, cachedir)
        fname = 'cache_dummy.pkl'
        open(f'{cachedir}/{fname}', 'w').close()
        assert fname in os.listdir(cachedir)
        tools.clear_cache()
        assert not fname in os.listdir(cachedir)
    except:
        pass
    finally:
        const.CACHEDIR = _cd

def test_browse_database():
    with pytest.raises(DataSearchError):
        tools.browse_database('blaaa')

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)