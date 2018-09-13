"""
Test script for collocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
    
model_id_3d = 'SPRINTARS-T213_AP3-CTRL2016-PD'
obs_id = 'EBASMC'

VARS = ['absc550aer', 'scatc550aer']

YEAR = 2010

TS_TYPE = 'daily'

if __name__ == '__main__':
    
    pya.change_verbosity('critical')
     
    obs_reader = pya.io.ReadUngridded()
    obs = obs_reader.read(obs_id, VARS)
    
    print(obs)