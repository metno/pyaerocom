"""
Test script for collocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya

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
    model = model_reader.read_var(MODEL_VAR, start_time=YEAR)
    print(model)
    
    #model = model.downscale_time(TS_TYPE)
    
    #get one column of sigma levels
    
    sigma_levels = model[0,:,0,0]
    
    psurf = model
    
    #pya.vert_coords.atmosphere_sigma_coordinate_to_pressure(leve)
    
    
    #pya.collocation.collocate_gridded_ungridded_2D(model, obs, var_ref='scatc550aer')