#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:31:35 2021

@author: jonasg
"""
import importlib, sys, os
from pyaerocom._lowlevel_helpers import (ListOfStrings, AsciiFileLoc)
def check_aux_info(fun, vars_required, funcs):
    spec =_AuxReadSpec(fun, vars_required, funcs)
    return dict(fun=spec.fun, vars_required=spec.vars_required)


class _AuxReadSpec:
    #func_name = StrType()
    vars_required = ListOfStrings()
    def __init__(self, fun, vars_required:list, funcs:dict):
        self.vars_required = vars_required
        self.fun = self.get_func(fun, funcs)

    def get_func(self, fun, funcs):
        if callable(fun):
            return fun
        elif isinstance(fun, str):
            return funcs[fun]
        raise ValueError('failed to retrieve aux func')


class ReadAuxHandler:
    aux_file = AsciiFileLoc(assert_exists=True, auto_create=False)
    def __init__(self, aux_file:str):
        self.aux_file = aux_file

    def import_module(self):

        moddir, fname = os.path.split(self.aux_file)
        if not moddir in sys.path:
            sys.path.append(moddir)
        modname = fname.split('.')[0]
        return importlib.import_module(modname)

    def import_all(self):
        mod = self.import_module()
        return mod.FUNS