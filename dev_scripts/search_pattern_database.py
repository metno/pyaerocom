#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:56:24 2018

@author: jonasg
"""

from pyaerocom import const
from os import listdir
from os.path import join, isdir
import fnmatch, re

sid = "noresm*"
pattern = fnmatch.translate(sid)
_candidates = []
_msgs = []
DIR =None

for search_dir in const.MODELDIRS:
    # get the directories
    if isdir(search_dir):
        #subdirs = listdir(search_dir)
        subdirs = [x for x in listdir(search_dir) if isdir(join(search_dir, x))]
        for subdir in subdirs:
            if bool(re.search(pattern, subdir,re.IGNORECASE)):
                if sid == subdir:
                    _dir = join(search_dir, subdir)
                    if const.GRID_IO.USE_RENAMED_DIR:
                        _dir = join(_dir, "renamed")
                    if isdir(_dir):
                        DIR = _dir
            
                _candidates.append(subdir)

if _candidates:
    print("Did you mean either of: {} ?".format(_candidates))