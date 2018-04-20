from os.path import join, exists
from os import mkdir

OUT_DIR = join(".", "out")
OUT_DIR_MAPS = join(".", "out", "maps")

if not exists(OUT_DIR):
    mkdir(OUT_DIR)

if not exists(OUT_DIR_MAPS):
    mkdir(OUT_DIR_MAPS)    
    
TEST_FILE = ('/lustre/storeA/project/aerocom/aerocom1/ECMWF_OSUITE_NRT_test/'
             'renamed/aerocom.ECMWF_OSUITE_NRT_test.daily.od550aer.2018.nc')
    


