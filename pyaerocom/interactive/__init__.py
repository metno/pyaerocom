#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:31:09 2018

@author: jonasg
"""

try:
    import ipywidgets
    ipw_avail = True
except Exception:
    ipw_avail = False

if ipw_avail:
    from .ipywidgets import ProgressBarLabelled
