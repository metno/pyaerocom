#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:45:59 2018

@author: jonasg
"""

import os
import fnmatch

DIR = "."

files = fnmatch.filter(os.listdir(DIR), "[0-9][0-9]*")

for fname in files:
    newname="tut{}".format(fname)
    os.rename(fname, newname)