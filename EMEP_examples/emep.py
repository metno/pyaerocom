#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:20:40 2020

@author: eirikg
"""


from iris.cube import CubeList
import os
import pyaerocom as pya
import iris
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.helpers import get_tot_number_of_seconds
from pyaerocom.helpers import to_pandas_timestamp
from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom.helpers import seconds_in_periods

# =============================================================================
# aerodir = '/home/eirikg/aerocom'
# storeb = '/run/user/433729/gvfs/smb-share\:server\=cifs-int-gw-b.met.no\,share\=storeb/'
# emep_2017 = storeb + '/lustre/storeB/project/fou/kl/emep/ModelRuns/2019_REPORTING/EMEP01_L20EC_rv4_33.2017'
# 
# # pya.const.add_data_search_dir(aerodir)
# #pya.const.add_data_search_dir(emep_2017)
# 
# =============================================================================


basepath = '/home/eirikg/Desktop/pyaerocom/data/'
file = '2020_AerocomHIST/1850_GLOB1_2010met/Base_month.nc'
filepath = '{}{}'.format(basepath, file)

reader = ReadEMEP(filepath)
wetso4 = reader.read_var('wetso4', ts_type='monthly')

ts = wetso4.time_stamps()
seconds = seconds_in_periods(ts, 'yearly')


# seconds =s seconds_in_periods(ts, 'monthly')

# =============================================================================
# try:
#     pya.const.add_ungridded_obs('aasetal', basepath + 'aas', 
#                             reader=pya.io.ReadAasEtal)
# except Exception as e:
#     print(repr(e))
#     
# =============================================================================
# pya.browse_database('Aas*')
# reader = pya.io.ReadUngridded('aasetal')
# wetso4_aas = reader.read(vars_to_retrieve='wetso4')
# pya.const.add_data_search_dir(basepath + 'aas')


# =============================================================================
# reader = ReadEMEP(basepath + 'EMEP_ctrl_2010/EMEPglob_rv4_33-81_2010_month.nc')
# =============================================================================

# wetso4 = reader.read_var(var_name='wetso4', ts_type='monthly', data_id='EMEP-test')
# wetso4.change_base_year(1850 - 110)
# wetso4.to_netcdf(os.path.join(basepath, 'emep_out'), vert_code='test')

# =============================================================================
# wetso4.data *= 10**-6 / 2592000 # mg -> kg && month to seconds
# wetso4.units = 'kg m-2 s-1'
# 
# 
# coloc = pya.colocation.colocate_gridded_ungridded(wetso4, wetso4_aas, filter_name="WORLD-wMOUNTAINS")#, ts_type='monthly')
# 
# coloc.plot_scatter()
# 
# =============================================================================
# import pandas as pd

# tidx = pd.DatetimeIndex(data.time_stamps())

# res = pya.helpers.get_tot_number_of_seconds(data.ts_type, tidx)

# print(res)
# data = reader.read(['dryso4','wetso4'], ts_type='monthly')
# dry = data[0]
# wet = data[1]




# # x = dry.cube.attributes


# # total = dry.data + wet.data
# # dry[0].quickplot_map()
# # wet[0].quickplot_map()

# cube = add_cubes(dry, wet)
# cube.var_name = 'depso4'
        
# data = pya.GriddedData(cube,
#                    ts_type=data[0].ts_type,
#                    computed=True)