#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 11:34:43 2018

@author: jonasg
"""
import cProfile
 
pr = cProfile.Profile()
pr.enable()
 
import pyaerocom as pya
 
pr.disable()
 
stats = pr.stats()
pr.print_stats(sort='cumtime')


#pya.const.change_database_paths('bla')