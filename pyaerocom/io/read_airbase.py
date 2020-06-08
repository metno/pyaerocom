#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Development template for reading routine of AirBase data.

NOTE
----

At the moment, the code below is just to illustrate the inheritance example
from ReadUngriddedBase class. The code is not functional at the moment.

"""

from pyaerocom.io.readungriddedbase import ReadUngriddedBase

class ReadAirBase(ReadUngriddedBase):
    """Reading class for AirBase data"""
    DATASET_PATH = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AIRBASE/'
    DATA_ID = 'AirBase'
    _FILEMASK = '*.nc'

    DEFAULT_VARS = ['pm10']
    PROVIDES_VARIABLES = ['pm10']
    SUPPORTED_DATASETS = ['AirBase']
    TS_TYPE = None
    __version__ = '0.0.1'

    def read(self):
        pass

    def read_file(self):
        pass

if __name__=='__main__':

    r = ReadAirBase()

    files = r.get_file_list()
