#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:32:52 2018

@author: jonasg
"""
import ipywidgets as ipw
from IPython.display import display

def ProgressBarLabelled(num, label=''):
    try:
        f = ipw.IntProgress(0, max=num)
        l = ipw.Label(label)
        display(ipw.HBox([l, f]))
        return f
    except Exception:
        pass
