"""
Test script for colocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
from time import time
MODEL_ID_3D = 'SPRINTARS-T213_AP3-CTRL2016-PD'
OBS_ID = 'EBASMC'

OBS_VARS = ['absc550aer', 'scatc550aer']
MODEL_VAR = 'ec550aer3d'
YEAR = 2010

TS_TYPE = 'daily'

if __name__ == '__main__':
    
    pya.change_verbosity('critical')
     
    obs_reader = pya.io.ReadUngridded()
    obs = obs_reader.read(OBS_ID, OBS_VARS)
    print(obs)
    
    model_reader = pya.io.ReadGridded(MODEL_ID_3D)
    model = model_reader.read_var(MODEL_VAR, start=YEAR)
    print(model)
    
    
    print('\nDecreasing temporal resolution')
    t0=time()
    model = model.downscale_time(TS_TYPE)
    print('Successfully decreased t-res (in {:.3f} s)'.format(time() - t0))
    
    tseries_surf = model.to_time_series(longitude=obs.longitude, 
                                        latitude=obs.latitude,
                                        vert_scheme='surface')
    raise Exception
    tseries_mean = model.to_time_series(longitude=obs.longitude, 
                                        latitude=obs.latitude)
    
    #model = model.downscale_time(TS_TYPE)
    
    #get one column of sigma levels
    
    sigma = model.atmosphere_sigma_coordinate.points
    
    psurf = model.surface_air_pressure
    
    ptop = 0
    
    ps = float(psurf[0,0,0].points)
    
    altitude = pya.vert_coords.atmosphere_sigma_coordinate_to_pressure(sigma, 
                                                                       ps, 
                                                                       ptop)
    #pya.vert_coords.atmosphere_sigma_coordinate_to_pressure(leve)
    
    
    #pya.colocation.colocate_gridded_ungridded_2D(model, obs, var_ref='scatc550aer')