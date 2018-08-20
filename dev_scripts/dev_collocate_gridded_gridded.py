"""
Test script for collocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
import matplotlib.pyplot as plt
from time import time
import iris
    
model_id = 'TM5_AP3-CTRL2016'
obs_id = 'MODIS6.terra'

YEAR = 2010
VAR = 'od550aer'
TS_TYPE = 'daily'

RELOAD = 0
if __name__ == '__main__':
    plt.close('all')
    pya.change_verbosity('critical')
    if RELOAD:
        print('Reading data...')
        read_model = pya.io.ReadGridded(model_id)
        model = read_model.read_individual_years('od550aer', 2010)['od550aer'][2010]
         
        read_sat = pya.io.ReadGridded(obs_id)
        sat = read_sat.read_individual_years('od550aer', 2010)['od550aer'][2010]
         
        model = model.downscale_time(TS_TYPE)
        obs = sat.downscale_time(TS_TYPE)
        
        model.grid.coord('longitude').guess_bounds()
        model.grid.coord('latitude').guess_bounds()
        obs.grid.coord('longitude').guess_bounds()
        obs.grid.coord('latitude').guess_bounds()
    
        model.quickplot_map(0)
    
        obs.quickplot_map(0)
    
    
    t0 = time()
    model_rg = model.regrid(obs)
    t1 = time()
    model_rg_aw = model.regrid(obs, iris.analysis.AreaWeighted())
    t2=time()
    model_rg_aw2 = model.regrid(obs, iris.analysis.AreaWeighted(mdtol=0.1))
    t3=time()
    
    ax = model_rg.quickplot_map(0).axes[0]
    ax.set_title('Model regrid (linear)')
    
    ax = model_rg_aw.quickplot_map(0).axes[0]
    ax.set_title('Model regrid (areat weighted mdtol=1)')
    
    ax = model_rg_aw2.quickplot_map(0).axes[0]
    ax.set_title('Model regrid (areat weighted mdtol=0.1)')
    
    diff_LIN_AW = model_rg.grid[0].data - model_rg_aw.grid[0].data
    fig = plt.figure()
    
    
    
    print('Elapsed time (linear regrid): {}s'.format(t1-t0))
    print('Elapsed time (area weighted regrid): {}s'.format(t2-t1))
    print('Elapsed time (area weighted regrid mdtol = 0.1): {}s'.format(t3-t2))
    
    print('Model resolution: {}'.format(model.shape))
    print('Satellite resolution: {}'.format(obs.shape))
    print('Model resolution (regrid): {}'.format(model_rg.shape))
    
    
    
    
    
    