#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Low level utility methods of pyaerocom
"""

from numpy import floor, log10

def exponent(num):
    """Get exponent of input number
    E.g.:
        *. 1000     ->  3
        #. 0.1      ->  -1
        #. 0.001    ->  -3
        #. 5        ->  1
        
    Parameters
    ----------
    num : float
        input number
    
    Returns
    -------
    int
        exponent of input number
    """
    return int(floor(log10(abs(num)))) 