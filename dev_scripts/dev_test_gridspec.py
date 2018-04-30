#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 16:52:53 2018

@author: jonasg
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.close("all")


fig = plt.figure(figsize=(12, 8))

gs = plt.GridSpec(1, 2, width_ratios=[1, .02], 
                  hspace=0.05)

ax_field = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
cax = fig.add_subplot(gs[0, 1])