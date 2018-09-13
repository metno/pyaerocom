"""
Test script for collocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
import xarray as xarr
model_id_3d = 'SPRINTARS-T213_AP3-CTRL2016-PD'
obs_id = 'EBASMC'

OBS_VARS = ['absc550aer', 'scatc550aer']
MODEL_VAR = 'ec550aer3d'
YEAR = 2010

TS_TYPE = 'daily'

if __name__ == '__main__':
    
    pya.change_verbosity('critical')
     
    obs_reader = pya.io.ReadUngridded()
    obs = obs_reader.read(obs_id, OBS_VARS)
    
    model_reader = pya.io.ReadGridded(model_id_3d)
    model = model_reader.read_var(MODEL_VAR)
    
    print(obs)
    print(model)
    
    ds = xarr.open_dataset(model.suppl_info['from_files'][0])
    print(ds)
    
    