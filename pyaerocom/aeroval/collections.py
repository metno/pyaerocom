#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:27:47 2021

@author: jonasg
"""
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.aeroval.modelentry import ModelEntry

class ObsCollection(BrowseDict):
    """
    Dict-like object that represents a collection of obs entries

    Keys are obs names, values are instances of :class:`ObsEntry`.

    Note
    ----
    This must not necessarily be only observations but may also be models. In
    most cases, it

    """
    ITEM_TYPE = ObsEntry

class ModelCollection(BrowseDict):
    ITEM_TYPE = ModelEntry


if __name__ == '__main__':
    oc = ObsCollection(model1 = dict(obs_id='bla', obs_vars='od550aer',
                                     obs_vert_type='Column'))

    oc['AN-EEA-MP'] = dict(is_superobs = True,
                           obs_id = ('AirNow', 'EEA-NRT-rural', 'MarcoPolo'),
                           obs_vars = ['concpm10', 'concpm25',
                                           'vmro3', 'vmrno2'],
                           obs_vert_type = 'Surface')