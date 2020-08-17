#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
from pathlib import Path
import os
import requests
import tarfile

from traceback import format_exc
from pyaerocom import const

def _download_test_data(url_testdata, basedir=None):
    print("TEMP OUTPUT: DOWNLOADING TESTDATA")
    #raise Exception('Temporarily disabled...')
    if basedir is None:
        basedir = const.OUTPUTDIR

    download_loc = Path(basedir).joinpath('{}.tar.gz'.format(const._testdatadirname))

    try:
        r = requests.get(url_testdata)
        with open(download_loc, 'wb') as f:
            f.write(r.content)

        with tarfile.open(download_loc, 'r:gz') as tar:
            tar.extractall(const.OUTPUTDIR)
            tar.close()
    except Exception:
        const.print_log.warning('Failed to download testdata. Traceback:\n{}'
                                .format(format_exc()))
        return False
    finally:
        if download_loc.exists():
            os.remove(download_loc)
    return True

def _check_access_testdata(basedir, test_paths):
    if isinstance(basedir, str):
        basedir = Path(basedir)
    elif not isinstance(basedir, Path):
        raise ValueError('Invalid input for basedir ({}), need str or Path'
                         .format(type(basedir)))
    if not basedir.exists():
        return False

    if not isinstance(test_paths, dict):
        raise ValueError('Invalid input for test_paths, need dict')

    for data_id, data_dir in test_paths.items():
        if not basedir.joinpath(data_dir).exists():
            return False
    return True

def check_access_testdata(basedir, test_paths, url_testdata):
    if not _check_access_testdata(basedir, test_paths):
        try:
            if _download_test_data(url_testdata, const.OUTPUTDIR):
                if _check_access_testdata(basedir, test_paths):
                    return True
        except Exception:
            pass
        return False
    return True

def _init_testdata(const, add_paths, testdatadir, ungridded_readers):
    for name, relpath in add_paths.items():
        ddir = str(testdatadir.joinpath(relpath))
        if name in ungridded_readers:
            reader = ungridded_readers[name]

            const.add_ungridded_obs(name, ddir,
                                    reader=reader,
                                    check_read=True)

        else:
            const.add_data_search_dir(ddir)

def _load_coldata_tm5_aeronet_from_scratch(file_path):
    from xarray import open_dataarray
    from pyaerocom import ColocatedData
    arr = open_dataarray(file_path)
    if '_min_num_obs' in arr.attrs:
        info = {}
        for val in arr.attrs['_min_num_obs'].split(';')[:-1]:
            to, fr, num = val.split(',')
            if not to in info:
                info[to] = {}
            if not fr in info[to]:
                info[to][fr] = {}
            info[to][fr] = int(num)
        arr.attrs['min_num_obs'] = info
    cd = ColocatedData()
    cd.data = arr
    return cd