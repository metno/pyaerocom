#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small helper utility functions for pyaerocom
"""   
import numpy as np
import os
import multiprocessing as mp
from collections import OrderedDict

class BrowseDict(OrderedDict):
    """Dictionary with get / set attribute methods
    
    Example
    -------
    >>> d = BrowseDict(bla = 3, blub = 4)
    >>> print(d.bla)
    3
    """
    def __getattr__(self, key):
        return self.__getitem__(key)
    
    def __setattr__(self, key, val):
        self.__setitem__(key, val)
        
    def __dir__(self):
        return self.keys()

    def __str__(self):
        return dict_to_str(self)

def check_fun_timeout_multiproc(fun, fun_args=(), timeout_secs=1):
    """Check input function timeout performance
    
    Uses multiprocessing module to test if input function finishes within a 
    certain time interval.
    
    Parameters
    ----------
    fun : callable
        function that is supposed to be tested
    fun_args : tuple
        function arguments
    timeout_secs : float
        timeout in seconds
    
    Returns
    -------
    bool
        True if function execution requires less time than input timeout, else
        False
    """
    
    # Start foo as a process
    OK = True
    p = mp.Process(target=fun, name="test", args=fun_args)
    p.start()
    p.join(timeout_secs)
    if p.is_alive():# Terminate foo
        OK =False
        p.terminate()
        # Cleanup
        p.join()  
    
    return OK   

def _is_interactive():
    import __main__ as main
    return not hasattr(main, '__file__')

def chk_make_subdir(base, name):
    """Check if sub-directory exists in parent directory"""
    d = os.path.join(base, name)
    if not os.path.exists(d):
        os.mkdir(d)
    return d

def check_dirs_exist(*dirs, **add_dirs):
    for d in dirs:
        if not os.path.exists(d):
            print('Creating dir: {}'.format(d))
            os.mkdir(d)
    for k, d in add_dirs.items():
        if not os.path.exists(d):
            os.mkdir(d)
            print('Creating dir: {} ({})'.format(d, k))
        

def list_to_shortstr(lst, indent=0, name=None):
    """Custom function to convert a list into a short string representation"""
    def _short_lst_fmt(lin):
        lout = []
        for val in lin:
            try:
                ndigits = -1*np.floor(np.log10(abs(np.asarray(val)))).astype(int) + 2
                lout.append('{:.{}f}'.format(val, ndigits))
            except:
                lout.append(val)
        return lout
    if name is None:
        name_str = '{} ({} items): '.format(type(lst).__name__, len(lst))
    else:
        name_str = '{} ({}, {} items): '.format(name, type(lst).__name__, len(lst))
    indentstr = indent*" "
    if len(lst) == 0:
        return "\n{}{}[]".format(indentstr, name_str)
    elif len(lst) < 6:
        lfmt = _short_lst_fmt(lst)
        return "\n{}{}{}".format(indentstr, name_str, lfmt)
    else: #first 2 and last 2 items
        lfmt= _short_lst_fmt([lst[0], lst[1], lst[-2], lst[-1]])
        s = ("\n{}{}[{}, {}, ..., {}, {}]"
             .format(indentstr, name_str, lfmt[0], lfmt[1], lfmt[2], lfmt[3]))
    
    return s

def sort_dict_by_name(d):
    """Sort entries of input dictionary by their names and return ordered
    
    Parameters
    ----------
    d : dict
        input dictionary
    
    Returns
    -------
    OrderedDict
        sorted and ordered dictionary
    """
    from collections import OrderedDict as od
    s = od()
    sorted_keys = sorted(d)
    for k in sorted_keys:
        s[k] = d[k]
    return s

def dict_to_str(dictionary, s="", indent=0, ignore_null=False):
    """Custom function to convert dictionary into string (e.g. for print)
    
    Parameters
    ----------
    dictionary : dict
        the dictionary
    s : str
        the input string
    indent : int
        indent of dictionary content
    ignore_null : bool
        if True, None entries in dictionary are ignored
    
    Returns
    -------
    str
        the modified input string
        
    Example
    -------
    
    >>> string = "Printing dictionary d"
    >>> d = dict(Bla=1, Blub=dict(BlaBlub=2))
    >>> print(dict_to_str(d, string))
    Printing dictionary d
       Bla: 1
       Blub (dict)
        BlaBlub: 2
    
    """
    for k, v in dictionary.items():
        if ignore_null and v is None:
            continue
        elif isinstance(v, dict):
            s += "\n{}{} ({}):".format(indent*' ', k, type(v).__name__)
            s = dict_to_str(v, s, indent+2)
        elif isinstance(v, list):
            s += list_to_shortstr(v, indent=indent, name=k)
        elif isinstance(v, np.ndarray) and v.ndim==1:
            s += list_to_shortstr(v, indent=indent, name=k)
        else:
            if v == '':
                v = '<empty_str>'
            s += "\n{}{}: {}".format(indent*" ", k, v)
    return s

def str_underline(s, indent=0):
    """Create underlined string"""
    s = indent*" " + "{}\n".format(s)
    s+= indent*" " + "{}".format(len(s)*"-")
    return s

if __name__ == '__main__':
    d = BrowseDict(bla=1, blub=42, blablub=dict(bla=42, blub=43))
    print(d)
