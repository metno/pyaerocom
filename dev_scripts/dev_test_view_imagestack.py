#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Based on

https://www.datacamp.com/community/tutorials/matplotlib-3d-volumetric-data

"""

import matplotlib.pyplot as plt
from pyaerocom.plot import plot_map
import numpy

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        self.slices, rows, cols, = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[self.ind, :, :])
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = numpy.clip(self.ind + 1, 0, self.slices - 1)
        else:
            self.ind = numpy.clip(self.ind - 1, 0, self.slices - 1)
        self.update()

    def update(self):
        self.im.set_data(self.X[self.ind, :, :])
        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()

class GriddedDataViewer(object):
    def __init__(self, data, fig=None):
        if fig is None:
            fig, ax = plt.subplots(1,1, figsize=(16, 10))
        self.fig = fig
        #ax.set_title('use scroll wheel to navigate images')

        self.data = data
        
        self.slices, rows, cols, = data.shape
        self.ind = 0
        
        self.update()
        self.fig.canvas.mpl_connect('scroll_event', self.onscroll)
        
    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = numpy.clip(self.ind + 1, 0, self.slices - 1)
        else:
            self.ind = numpy.clip(self.ind - 1, 0, self.slices - 1)
        self.update()

    def update(self):
        self.data.quickplot_map(self.ind, fig=self.fig)
        #ax.set_ylabel('slice %s' % self.ind)
        self.fig.canvas.draw()
        
    
if __name__ == "__main__":
    import pyaerocom as pya
    
    data = pya.GriddedData()
    
    data._init_testdata_default()
    
    data = data.crop(region="EUROPE")
    #data = data[0:30]
    #print(data.shape)
    
    #arr = data.grid.data
    
    tracker = GriddedDataViewer(data)
    
    plt.show()