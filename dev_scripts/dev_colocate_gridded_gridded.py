"""
Test script for colocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
import matplotlib.pyplot as plt
from time import time
import numpy as np
    
model_id = 'TM5_AP3-CTRL2016'
obs_id = 'MODIS6.terra'

YEAR = 2010
VAR = 'od550aer'
TS_TYPE = 'yearly'
REGION = 'EUROPE'

RELOAD = 1
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
        
        f = pya.Filter(region=REGION)
        
        model = f(model)
        obs = f(obs)
        model.quickplot_map(0)
    
        obs.quickplot_map(0)
    
    
    t0 = time()
    model_rg = model.regrid(obs, scheme='linear')
    t1 = time()
    model_rg_aw = model.regrid(obs, scheme='areaweighted')
    t2 = time()
    
    ax = model_rg.quickplot_map(0).axes[0]
    ax.set_title('Model regrid (linear)')
    
    ax = model_rg_aw.quickplot_map(0).axes[0]
    ax.set_title('Model regrid (areat weighted)')

    
    diff_LIN_AW = model_rg.grid[0].data - model_rg_aw.grid[0].data
    fig = plt.figure()
    plt.imshow(diff_LIN_AW)
    plt.colorbar()
    plt.title('Difference (linear vs. Area weighted regridding)')
    
    model_np = model_rg.grid.data
    obs_np = obs.grid.data
    
    if not isinstance(obs_np, np.ma.core.MaskedArray):
        raise NotImplementedError
    mask = ~obs_np.mask
    
    model_vals = model_np[mask]
    obs_vals = obs_np[mask].data
    
    ax = pya.plot.plotscatter_new.plot_scatter(model_vals, 
                                          obs_vals)
    print('Elapsed time (linear regrid): {}s'.format(t1-t0))
    print('Elapsed time (area weighted regrid): {}s'.format(t2-t1))
    
    print('Model resolution: {}'.format(model.shape))
    print('Satellite resolution: {}'.format(obs.shape))
    print('Model resolution (regrid): {}'.format(model_rg.shape))
    
    
    
    
    
    
    
    