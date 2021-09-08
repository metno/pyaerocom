#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 12:27:47 2021

@author: jonasg
"""
from fnmatch import fnmatch
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.exceptions import EntryNotAvailable
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.aeroval.modelentry import ModelEntry


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
                f'No matches could be found that match input {name_or_pattern}')
        return matches

    def get_entry(self, key) -> object:
        """
        Getter for eval entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        try:
            return self[key]
        except (AttributeError, KeyError):
            raise EntryNotAvailable(f'no such entry {key}')


    def get_web_iface_name(self, key):
        """
        Get webinterface name for obs entry

        Note
        ----
        Normally this is the key of the obsentry in :attr:`obs_config`,
        however, it might be specified explicitly via key `web_interface_name`
        in the corresponding value.

        Parameters
        ----------
        key : str
            key of entry.

        Returns
        -------
        str
            corresponding name

        """
        if not 'web_interface_name' in self[key]:
            return key
        return self[key]['web_interface_name']

    def get_all_vars(self):
        vars = []
        for key, cfg in self.items():
            vars.extend(cfg.get_all_vars())
        return sorted(list(set(vars)))


    @property
    def web_iface_names(self):
        """
        Get webinterface name for obs entry

        Note
        ----
        Normally this is the key of the obsentry in :attr:`obs_config`,
        however, it might be specified explicitly via key `web_interface_name`
        in the corresponding value.

        Parameters
        ----------
        key : str
            key of entry.

        Returns
        -------
        str
            corresponding name

        """
        return [self.get_web_iface_name(key) for key in self.keylist()]

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
    SETTER_CONVERT = {dict : ObsEntry}

    def get_entry(self, key) -> object:
        """
        Getter for obs entries

        Raises
        ------
        KeyError
            if input name is not in this collection
        """
        cfg = super(ObsCollection, self).get_entry(key)
        cfg['obs_name'] = self.get_web_iface_name(key)
        return cfg

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

    SETTER_CONVERT = {dict : ModelEntry}
    def get_entry(self, key) -> object:
        """Get model entry configuration

        Since the configuration files for experiments are in json format, they
        do not allow the storage of executable custom methods for model data
        reading. Instead, these can be specified in a python module that may
        be specified via :attr:`add_methods_file` and that contains a
        dictionary `FUNS` that maps the method names with the callable methods.

        As a result, this means that, by default, custom read methods for
        individual models in :attr:`model_config` do not contain the
        callable methods but only the names. This method will take care of
        handling this and will return a dictionary where potential custom
        method strings have been converted to the corresponding callable
        methods.

        Parameters
        ----------
        model_name : str
            name of model

        Returns
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        cfg = super(ModelCollection, self).get_entry(key)
        cfg['model_name'] = self.get_web_iface_name(key)
        return cfg


if __name__ == '__main__':
    oc = ObsCollection(model1 = dict(obs_id='bla', obs_vars='od550aer',
                                     obs_vert_type='Column'))

    oc['AN-EEA-MP'] = dict(is_superobs = True,
                           obs_id = ('AirNow', 'EEA-NRT-rural', 'MarcoPolo'),
                           obs_vars = ['concpm10', 'concpm25',
                                           'vmro3', 'vmrno2'],
                           obs_vert_type = 'Surface')