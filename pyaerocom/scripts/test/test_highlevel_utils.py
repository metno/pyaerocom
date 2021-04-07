#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:53:41 2021

@author: jonasg
"""
import pytest
import os
from pyaerocom import const
from pyaerocom.exceptions import DataSearchError
from getpass import getuser
import pyaerocom.scripts.highlevel_utils as hu

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
        hu.clear_cache()
        assert not fname in os.listdir(cachedir)
    except:
        pass
    finally:
        const.CACHEDIR = _cd

def test_browse_database():
    with pytest.raises(DataSearchError):
        hu.browse_database('blaaa')



if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)

