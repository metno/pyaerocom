from netCDF4 import num2date
from pydap.client import open_dods
import matplotlib.pyplot as plt
import pyaerocom
import os

### COMMENT JGLISS: This was just a test from NILU which ended up too slow,
# DON'T USE
### Online access using OpenDAP

mercury_ds = open_dods('http://dev-ebas-pydap.nilu.no/NO0042G.Hg_mon.IMG.air.mercury.1h.NO01L_tekran_42_dup.NO01L_afs..dods')

# We get the keys
keys = mercury_ds.keys()

print(keys)

mercury = mercury_ds['mercury']


print(mercury.keys())

print(mercury.mercury.data)

y = mercury.mercury.data

x = num2date(mercury.time.data,units='days since 1900-01-01 00:00:00',calendar='gregorian')

plt.plot(x,y)


path = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data'

file = "NO0042G.20100101.20131231.aerosol_light_backscattering_coefficient.pm10.1y.1h.SE02L_TSI_3563_ZEP_dry.SE02L_scat_coef.nas"

