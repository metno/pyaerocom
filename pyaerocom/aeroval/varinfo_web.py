#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 08:00:01 2021

@author: jonasg
"""
from pyaerocom.mathutils import is_strictly_monotonic, make_binlist
from pyaerocom.variable import get_variable

class VarinfoWeb:
    _num_bins = 8
    def __init__(self, var_name : str, cmap : str = None,
                 cmap_bins : list = None, vmin : float = None,
                 vmax : float = None):
        if cmap_bins is not None:
            if vmin is not None or vmax is not None:
                raise ValueError('please provide either vmin and vmax OR '
                                 'cmap_bins, not both...')
            if not is_strictly_monotonic(cmap_bins):
                raise ValueError('cmap_bins need to be strictly monotonic')

        self.var_name = var_name
        self.cmap_bins = cmap_bins
        self.cmap = cmap
        self.ndigits = None
        self.autofill_missing(vmin, vmax)

    @property
    def vmin(self):
        return self.cmap_bins[0]

    @property
    def vmax(self):
        return self.cmap_bins[-1]

    def autofill_missing(self, vmin, vmax):
        var = None
        if vmin is not None and vmax is not None:
            self.cmap_bins = make_binlist(vmin, vmax, self._num_bins)
        elif self.cmap_bins is None:
            var = get_variable(self.var_name)
            self.cmap_bins = var.get_cmap_bins(infer_if_missing=True)

        if self.cmap is None:
            if var is None:
                var = get_variable(self.var_name)
            self.cmap = var.get_cmap()

    @staticmethod
    def from_dict(dict):
        return VarinfoWeb(**dict)

    def to_dict(self):
        dd = {**self.__dict__}
        dd['vmin'] = self.vmin
        dd['vmax'] = self.vmax
        return dd


if __name__ == '__main__':

    dd = {'var_name':'od550aer'}
    info = VarinfoWeb.from_dict(dd)

    print(info.to_dict())

