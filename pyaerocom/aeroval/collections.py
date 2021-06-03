#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:27:47 2021

@author: jonasg
"""
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.aeroval.modelentry import ModelEntry
from fnmatch import fnmatch

class BaseCollection(BrowseDict):
    MAXLEN_KEYS = 25
    FORBIDDEN_CHARS_KEYS =['_']
    def keylist(self, name_or_pattern:str=None) -> list:
        """Find model names that match input search pattern(s)

        Parameters
        ----------
        name_or_pattern : str, optional
            Name or pattern specifying search string.

        Returns
        -------
        list
            list of keys in collection that match input requirements. If
            `name_or_pattern` is None, all keys will be returned.

        Raises
        ------
        KeyError
            if no matches can be found
        """
        if name_or_pattern is None:
            name_or_pattern = '*'

        matches = []
        for key in self.keys():
            if fnmatch(key, name_or_pattern) and not key in matches:
                matches.append(key)
        if len(matches) == 0:
            raise KeyError(
                f'No models could be found that match input {name_or_pattern}')
        return matches

    def get_entry(self, name) -> object:
        """
        Getter for eval entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        return self[name]

class ObsCollection(BaseCollection):
    """
    Dict-like object that represents a collection of obs entries

    Keys are obs names, values are instances of :class:`ObsEntry`. Values can
    also be assigned as dict and will automatically be converted into
    instances of :class:`ObsEntry`.


    Note
    ----
    Entries must not necessarily be only observations but may also be models.
    Entries provided in this collection refer to the y-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by :class:`ObsEntry`.

    """
    ITEM_TYPE = ObsEntry

    @property
    def all_obs_vars(self):
        """List of unique obs variables"""
        obs_vars = []
        for key, cfg in self.items():
            obs_vars.extend(cfg['obs_vars'])
        return sorted(list(set(obs_vars)))

class ModelCollection(BaseCollection):
    """
    Dict-like object that represents a collection of model entries

    Keys are model names, values are instances of :class:`ModelEntry`. Values
    can also be assigned as dict and will automatically be converted into
    instances of :class:`ModelEntry`.


    Note
    ----
    Entries must not necessarily be only models but may also be observations.
    Entries provided in this collection refer to the x-axis in the AeroVal
    heatmap display and must fulfill the protocol defined by
    :class:`ModelEntry`.

    """
    ITEM_TYPE = ModelEntry

if __name__ == '__main__':
    oc = ObsCollection(model1 = dict(obs_id='bla', obs_vars='od550aer',
                                     obs_vert_type='Column'))

    oc['AN-EEA-MP'] = dict(is_superobs = True,
                           obs_id = ('AirNow', 'EEA-NRT-rural', 'MarcoPolo'),
                           obs_vars = ['concpm10', 'concpm25',
                                           'vmro3', 'vmrno2'],
                           obs_vert_type = 'Surface')