#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:34:57 2018

@author: jonasg
"""

from collections import OrderedDict as od
import multiprocessing
from functools import partial

class PlotMultiCore(multiprocessing.pool.Pool):
    """Class that may be used for running multi
    
    Attributes
    ----------
    
    """
    _func_input = None
    def __init__(self, plotfun, varargs_prep, **fixargs):
        super(self, PlotMultiCore).__init__()
        self._func_input = plotfun
        self.varargs_prep = varargs_prep
        self.fixargs = fixargs
    
    @property
    def plotfun(self):
        raise NotImplementedError
    def run():
        raise NotImplementedError
        
if  __name__=="__main__":
    #mp = PlotMultiCore()
    import numpy as np
    import matplotlib.pyplot as plt
    
    def plotfun(yoffs, x, y, color):
        pass
    
    def func(a1=1, a2=1, a3=1, a4=1, a5=1):
        return a1 + a2 + a3 + a4 +a5 
    
    
    
    def fix_params(func, **fix_args):
        import inspect
        args = inspect.getargspec(func).args
        for arg_name in fix_args:
            remove_idx = []
            if not arg_name in args:
                raise KeyError("Function %s does not have input argument %s "
                               %arg_name)
            remove_idx.append(args.index(arg_name))
        
        return func( **fix_args)
    
    func_fix = fix_params(func, a1=2, a2=2)
        
    print(func())
    print(func(2,2,2,2,2))
    #print(func_fix(2, 2, 2))