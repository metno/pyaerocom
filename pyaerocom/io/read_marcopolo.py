import pyaerocom as pya
import os
import csv
from glob import glob
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import numpy as np

# variables conversion and units dictionnary
pyvars = {
    'vmrco': {
        'var': 'co',
        'unit': 'nmole mole-1'
    },
    'vmrso2': {
        'var': 'so2',
        'unit': 'nmole mole-1'
    },
    'vmrno2': {
        'var': 'no2',
        'unit': 'nmole mole-1'
    },
    'vmro3': {
        'var': 'o3',
        'unit': 'nmole mole-1'
    },
    'concpm10': {
        'var': 'pm10',
        'unit': 'ug m-3'
    },
    'concpm25': {64Z
        'var': 'pm2_5',
        'unit': 'ug m-3'
    }
}

def read_cams84_china(files, vars_to_retrieve=None):

    # first, read configuration file
    print('read configuration file')
    path_cfg = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/CHINA_SON2020_MP_NRT'
    fn = os.path.join(path_cfg,'station_info.xlsx')
    cfg = pd.read_excel(fn,engine='openpyxl')

    # read data using pandas read_csv: faster than csv reading routines..?
    # csv.DictReader took 271.47131180763245 seconds
    # pd.read_csv took 101.79213833808899 seconds
    print('read data file(s)')
    # initialize empty dataframe
    data = pd.DataFrame()
    for i in tqdm(range(len(files))):
        data = data.append(pd.read_csv(files[i],sep=','))

    # convert dateTime from string to datetime and set as index
    data['dateTime'] = pd.to_datetime(data['dateTime'].values)
    data.set_index('dateTime', inplace=True)


    #list of available variables
    av_data = ['vmrco', 'vmrso2', 'vmrno2', 'vmro3', 'concpm10', 'concpm25']
    if vars_to_retrieve == None:
        vars_to_retrieve = av_data

    #convert dataframes to dictionnaries
    dic_cfg = dict()
    for column in cfg.columns:
        dic_cfg[column] = np.array(cfg[column].values)
    dic_data = dict()
    for column in data.columns:
        dic_data[column] = np.array(data[column].values)

    # list of stationData objects
    print('create stationData objects')
    stationsData = []
    for i in tqdm(range(len(dic_cfg['stationId']))):
        for var in vars_to_retrieve:
            try:
                #initialize stationData object
                stationData = pya.StationData()

                # fill stationData with cfg
                stationData['data_id'] = 'CAMS84_CHINA'
                stationData['station_name'] = dic_cfg['stationName'][i]
                stationData['station_id'] = dic_cfg['stationId'][i]
                stationData['latitude'] = dic_cfg['latitude'][i]
                stationData['longitude'] = dic_cfg['longitude'][i]
                stationData['ts_type'] = 'hourly'

                # fill stationData with data
                mask = (dic_data['species'] == pyvars[var]['var']) & (dic_data['station_ID'] == stationData['station_id'])
                stationData[var] = dic_data['value'][mask].astype('datetime64[s]')

                # for each variable, there needs to be an entry in the var_info dict
                stationData['var_info'][var] = dict()
                stationData['var_info'][var]['units'] = pyvars[var]['unit']

                stationsData.append(stationData)
            except KeyError:
                print("Available variables: ",av_data)
                raise
    return stationsData

path_data = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/CHINA_SON2020_MP_NRT'
files = glob(os.path.join(path_data, '*.csv'))
data = read_cams84_china(files, ['concpm10','concpm25'])
