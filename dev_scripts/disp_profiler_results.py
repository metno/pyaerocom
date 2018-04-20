#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:30:15 2018

@author: jonasg
"""

import argparse
import pstats

p = argparse.ArgumentParser()

p.add_argument("file", help="Provide file path")

args = p.parse_args()

res = pstats.Stats(args.file).sort_stats('cumulative').print_stats(20)

