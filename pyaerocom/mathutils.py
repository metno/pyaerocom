#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

from numpy import floor, log10, asarray

def exponent(num):
    """Get exponent of input number
        
    Parameters
    ----------
    num : :obj:`float` or iterable
        input number
    
    Returns
    -------
    :obj:`int` or :obj:`ndarray` containing ints
        exponent of input number(s)
        
    Example
    -------
    >>> from pyaerocom.mathutils import exponent
    >>> exponent(2340)
    3
    """
    return floor(log10(abs(asarray(num)))).astype(int)

if __name__ == "__main__":
    import doctest
    exp = exponent(23)
    
    #run tests in all docstrings
    doctest.testmod()
    
    