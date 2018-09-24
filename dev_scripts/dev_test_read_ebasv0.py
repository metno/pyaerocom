"""
Test script for colocation of gridded vs gridded at different resolutions
"""

import pyaerocom as pya


if __name__=="__main__":
    
    reader = pya.io.ReadUngridded(datasets_to_read='EBASMC')

    data = reader.read()

    stations = data.to_station_data_all(freq='D')    
    
    
    
    
    
    
    