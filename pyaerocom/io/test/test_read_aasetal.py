# -*- coding: utf-8 -*-

"""
High level test methods that check AasEtAl time series data for selected stations
Created on June 12 2019.

@author: hannas@met.no

Largely modified and optimised by J. Gliss
"""
import pytest
import numpy as np
import pandas as pd
import os

from pyaerocom.test.settings import lustre_unavail
from pyaerocom.io.read_aasetal import ReadSulphurAasEtAl
from pyaerocom.units_helpers import convert_unit


# (from to unit)
UNITCONVERSION = {
    'concso2':   ('ug S/m3', 'ug m-3'), 
    'concso4':   ('ug S/m3', 'ug m-3'), 
    'wetso4':    ('kg S/ha', 'kg m-2'),  #  s-1
    'concso4pr': ('mg S/L',   'g m-3')
}

DATA_ID = 'GAWTADsubsetAasEtAl'

DATA_DIR = '/lustre/storeA/project/aerocom/aerocom1//AEROCOM_OBSDATA/PYAEROCOM/GAWTADSulphurSubset/data'

FILENAMES = ['monthly_so2.csv', 'monthly_so4_aero.csv', 'monthly_so4_precip.csv']

@lustre_unavail
@pytest.fixture(scope='session')
def aasetal_data():
    reader = ReadSulphurAasEtAl(DATA_ID)
    # that's quite time consuming, so keep it for possible usage in other 
    # tests
    return reader.read()  # read all variables
    
@lustre_unavail
def test_reader():
    reader = ReadSulphurAasEtAl(DATA_ID)
    assert reader.DATA_ID == DATA_ID
    assert reader.DATASET_PATH == DATA_DIR
    assert reader.PROVIDES_VARIABLES == ['concso2', 'concso4', 'pr', 
                                         'wetso4', 'concso4pr']
    filenames = [os.path.basename(x) for x in reader.get_file_list()]
    assert filenames == FILENAMES
    
@lustre_unavail
def test_aasetal_data(aasetal_data):
    data = aasetal_data
    assert len(data.station_name) == 890
    assert data.shape == (416243, 12) 
    assert data.contains_vars == ['concso2', 'concso4', 'concso4pr', 'pr', 'wetso4']
    assert data.contains_instruments == ['3_stage_filterpack', 'passive_sampler',
                                         'abs_solution', 'monitor', 'filter_1pack',
                                         'filterpack', '2_stage_filterpack',
                                         'filter_denuder_sampler', 'IMPROVE_PM2.5',
                                         'filter-1pack', 'filter_3pack', 
                                         'filter_2pack', 'pm10_sampler', 
                                         'filter-3pack', 'wet only', 'bulk', 
                                         'bulk ', 'wet-only']
    
@lustre_unavail
def test_reading_routines(aasetal_data):
    """
    Read one station Yellowstone NP. Retrive station from ungridded data object, 
    convert unit back and compare this to the raw data from the file.    
    """
    
    files = [os.path.join(DATA_DIR, x) for x in FILENAMES]
    
    assert np.sum([os.path.exists(x) for x in files]) == 3
    
    ungridded = aasetal_data
    
    df = pd.read_csv(files[0], sep=",", low_memory=False)
    subset = df[df.station_name == 'Yellowstone NP']
    vals = subset['concentration_ugS/m3'].astype(float).values
    
    station = ungridded.to_station_data('Yellowstone NP', 'concso2')
    from_unit, to_unit = UNITCONVERSION['concso2']
    conv = convert_unit(data=station.concso2.values, from_unit=from_unit, 
                        to_unit=to_unit, var_name='concso2')
    
    #conv = unitconv_sfc_conc_bck(station.concso2.values, 2)
    msg = ('Inconsistancy between reading a file and reading a station. '
            'File: monthly_so2.csv. Station: Yellowstone NP. '
            'Variable: concso2.')
    assert np.abs(conv - vals).sum() < 0.000001, msg
              

    df = pd.read_csv(files[1], sep=",", low_memory=False)
    subset = df[df.station_name == 'Payerne']
    vals = subset['concentration_ugS/m3'].astype(float).values
    ungridded = ReadSulphurAasEtAl().read(vars_to_retrieve = 'concso4')
    station = ungridded.to_station_data('Payerne', 'concso4')
    
    from_unit, to_unit = UNITCONVERSION['concso4']
    conv = convert_unit(data=station.concso4.values, from_unit = from_unit, 
                        to_unit = to_unit, var_name = 'concso4')
    
    #conv = unitconv_sfc_conc_bck(station.concso4.values, 4)
    summed = np.abs(conv - vals).sum()

    msg = ('Inconsistancy between reading a file and reading a station. ' 
           'File: monthly_so4_aero.csv. Station: Payerne. Variable: concso4.')
    assert summed < 0.000001, msg
    
    station_name = 'Abington (CT15)'
    df = pd.read_csv(files[2], sep=",", low_memory=False)
    subset = df[df.station_name == station_name]
    
    tconv = lambda yr, m : np.datetime64('{:04d}-{:02d}-{:02d}'.format(yr, m, 1), 's')
    dates_alt = [tconv(yr, m) for yr, m in zip(subset.year.values, subset.month.values)]
    subset['dtime'] = np.array(dates_alt)
    vals = subset['deposition_kgS/ha'].astype(float).values  
    
    ungridded = ReadSulphurAasEtAl().read(vars_to_retrieve = 'wetso4')
    station = ungridded.to_station_data(station_name, 'wetso4')
    #conv = unitconv_wet_depo_bck(station.wetso4.values, subset['dtime'], 'monthly').values
    conv = station.wetso4.values
    
    
    
    summed = np.abs(conv - vals).sum()
    msg= ('Inconsistancy between reading a file and reading a'
          'station. File: monthly_so4_aero.csv. Station: {}. '
          'Variable: wetso4.'.format(station_name))
    assert summed < 0.00001, msg
    

if __name__ == "__main__":
    reader = ReadSulphurAasEtAl(DATA_ID)
    
    pytest.main(['test_read_aasetal.py'])
