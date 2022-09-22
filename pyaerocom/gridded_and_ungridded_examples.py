import pickle

import pyaerocom as pya
from pyaerocom.extras.satellite_l2.sentinel5p import ReadL2Data

with open('/home/lewisb/Python/PyaDevScripts/GriddedDataExample.pickle', 'rb') as handle:
    gridded = pickle.load(handle)

with open('/home/lewisb/Python/PyaDevScripts/UngriddedDataExample.pickle', 'rb') as handle:
    ungridded = pickle.load(handle)

ungridded._data

file_path = "/home/lewisb/data/TROPOMI/CopernicusHub/O3_Profiles/"
testfiles = []
testfiles.append(file_path + "S5P_OFFL_L2__O3__PR_20211231T010540_20211231T024709_21844_02_020301_20220101T165013.nc")

obj = ReadL2Data()
data=obj.read(files=testfiles, vars_to_retrieve = "ozone_profile")
breakpoint()

