#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings for I/O of obervation data 

Note
----
Some settings like paths etc can be found in :mod:`pyaerocom.config.py`
"""
#: Wavelength tolerance for observations if data for required wavelength
        #: is not available
OBS_WAVELENGTH_TOL_NM = 10.0
        
#: This boolean can be used to enable / disable the former (i.e. use
#: available wavelengths of variable in a certain range around variable
#: wavelength).
OBS_ALLOW_ALT_WAVELENGTHS = True