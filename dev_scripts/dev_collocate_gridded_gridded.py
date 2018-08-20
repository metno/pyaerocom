"""
Test script for collocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
import matplotlib.pyplot as plt

model_id = 'TM5_AP3-CTRL2016'
obs_id = 'MODIS6.terra'

YEAR = 2010
VAR = 'od550aer'
TS_TYPE = 'daily'

RELOAD = 1
if __name__ == '__main__':
    pya.change_verbosity('critical')
    if RELOAD:
        print('Reading data...')
        read_model = pya.io.ReadGridded(model_id)
        model = read_model.read_individual_years('od550aer', 2010)['od550aer'][2010]
         
        read_sat = pya.io.ReadGridded(obs_id)
        sat = read_sat.read_individual_years('od550aer', 2010)['od550aer'][2010]
         
    model_daily = model.downscale_time(TS_TYPE)
    sat_daily = sat.downscale_time(TS_TYPE)
    
    print('Model resolution: {}'.format(model_daily.shape))
    print('Sattelite resolution: {}'.format(sat_daily.shape))

    
    model_daily.quickplot_map(0)
    model_daily.quickplot_map(364)
    