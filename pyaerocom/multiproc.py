#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:34:57 2018

@author: jonasg
"""

from collections import OrderedDict as od
from multiprocessing.pool import Pool
from functools import partial
#from pyaerocom.plot.mapping import plot_map_aerocom

class PlotMultiCore(Pool):
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
        return self._func_input
        
    def run():
        raise NotImplementedError
        
if  __name__=="__main__":
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    #mp = PlotMultiCore()
    
    def plotfun(yoffs, x, y, color):
        pass
    
    def func(a1, a2, a3, a4, a5):
        val = a1 + a2 + a3 + a4 + a5 
        print(val)
        return val
    
    def fix_params(func, **fix_args):
        import inspect
        args = inspect.getargspec(func).args
        for arg_name in fix_args:
            remove_idx = []
            if not arg_name in args:
                raise KeyError("Function %s does not have input argument %s "
                               %arg_name)
            remove_idx.append(args.index(arg_name))
        
        return func(**fix_args)
    
    #func_fix = fix_params(func, a1=5, a2=5)
    
    fix_args = dict(a2=10, a3=20)
    
    func_reduced = partial(func, **fix_args)
    
    
        
    #print(func())
    print(func(2,2,2,2,2))
    print(func_reduced(a1=2, a4=2, a5=2))
    #print(func_reduced(2, 2, 2))
    
    
    p = Pool()
    jobs = [zip(a1=2, a4=2, a5=2), dict(a1=2, a4=2, a5=2), dict(a1=2, a4=2, a5=2)]
    p.starmap(func, jobs)