#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

from numpy import floor, log10

def exponent(num):
    """Get exponent of input number
        
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
