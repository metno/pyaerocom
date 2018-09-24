"""
Test script for colocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya
import matplotlib.pyplot as plt
    
model_id = 'TM5_AP3-CTRL2016'
obs_id = 'MODIS6.terra'

YEAR = 2010
VAR = 'od550aer'
TS_TYPE = 'yearly'
REGION = 'EUROPE'
REGION = 'WORLD'

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
    
    print('Colocating data...')
    data = pya.colocation.colocate_gridded_gridded(model, sat,
                                                    ts_type=TS_TYPE,
                                                    filter_name='{}-wMOUNTAINS'.format(REGION))
    
    print(data)
    
    data.plot_scatter()
    
    
    
    