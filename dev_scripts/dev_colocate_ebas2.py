"""
Test script for colocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
from time import time

MODEL_ID_3D = 'CAM5.3-Oslo_AP3-CTRL2016-PD'
OBS_ID = 'EBASMC'

OBS_VARS = ['absc550aer', 'scatc550aer']
MODEL_VAR = 'ec5503Daer'
MODEL_VAR = 'ec550dryaer'
YEAR = 2010

TS_TYPE = 'monthly'

if __name__ == '__main__':
    
    pya.change_verbosity('critical')
     
    obs_reader = pya.io.ReadUngridded()
    obs = obs_reader.read(OBS_ID, OBS_VARS)
    
    model_reader = pya.io.ReadGridded(MODEL_ID_3D)
    model = model_reader.read_var(MODEL_VAR, start=YEAR)
    print(obs)
    print(model)
    
    model_at_stats = model.compute_at_stations_file(out_dir='out', 
                                                    obs_data=obs)
    
    model_reload = pya.GriddedData(model_at_stats)
    
    
    coll1 = pya.colocation.colocate_gridded_ungridded_2D(model,
                                                          obs, 
                                                           'monthly',
                                                          var_ref='scatc550aer',
                                                          vert_scheme='surface')
    
    coll2 = pya.colocation.colocate_gridded_ungridded_2D(model_reload,
                                                          obs, 
                                                           'monthly',
                                                          var_ref='scatc550aer',
                                                          vert_scheme='surface')
    
    coll1.plot_scatter()
    coll2.plot_scatter()