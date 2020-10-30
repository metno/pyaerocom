# -*- coding: utf-8 -*-

"""
High level test methods that check AasEtAl time series data for selected stations
Created on June 12 2019.

@author: hannas@met.no

Largely modified and optimised by J. Gliss (Feb 2020)
"""
import pytest
import numpy as np
import numpy.testing as npt
import pandas as pd
import os

from pyaerocom import const
from pyaerocom.conftest import lustre_unavail
from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.units_helpers import convert_unit

VARUNITS = {
    'concso2'   :   'ug m-3',
    'concso4'   :   'ug m-3',
    'wetso4'    :   'kg m-2 s-1',
    'concso4pr' :   'g m-3',
    'pr'        :   'mm'
}

DATA_ID = 'GAWTADsubsetAasEtAl'

FILENAMES = ['monthly_so2.csv', 'monthly_so4_aero.csv', 'monthly_so4_precip.csv']

VARS = ['concso2', 'concso4', 'concso4pr', 'pr', 'wetso4']

@lustre_unavail
def DATA_DIR():
    return const.OBSLOCS_UNGRIDDED[const.GAWTADSUBSETAASETAL_NAME]

@lustre_unavail
def test_data_files():
    files = [os.path.join(DATA_DIR(), x) for x in FILENAMES]

    assert np.sum([os.path.exists(x) for x in files]) == 3

@lustre_unavail
def test__get_time_stamps():
    reader = ReadAasEtal()
    fp = os.path.join(DATA_DIR(), FILENAMES[0])
    df = pd.read_csv(fp, sep=",", low_memory=False)
    timestamps = reader._get_time_stamps(df[:10])

    assert str(timestamps[0]) == '1997-09-01T00:00:00'
    assert str(timestamps[-1]) == '1998-09-01T00:00:00'

@lustre_unavail
def test_reader():
    reader = ReadAasEtal(DATA_ID)
    assert reader.data_id == DATA_ID
    assert reader.DATASET_PATH == DATA_DIR()
    assert reader.PROVIDES_VARIABLES == ['concso2', 'concso4', 'pr',
                                         'wetso4', 'concso4pr']
    filenames = [os.path.basename(x) for x in reader.get_file_list()]
    assert filenames == FILENAMES

@lustre_unavail
def test_aasetal_data(aasetal_data):
    data = aasetal_data
    assert len(data.station_name) == 890
    assert len(data.unique_station_names) == 667
    assert data.shape == (416243, 12)
    assert data.contains_vars == VARS
    assert data.contains_instruments == ['3_stage_filterpack', 'passive_sampler',
                                         'abs_solution', 'monitor', 'filter_1pack',
                                         'filterpack', '2_stage_filterpack',
                                         'filter_denuder_sampler', 'IMPROVE_PM2.5',
                                         'filter-1pack', 'filter_3pack',
                                         'filter_2pack', 'pm10_sampler',
                                         'filter-3pack', 'wet only', 'bulk',
                                         'bulk ', 'wet-only']

@lustre_unavail
def test_aasetal_data_correct_units(aasetal_data):

    tested = []
    stats = []
    for meta_key, meta in aasetal_data.metadata.items():

        for var, info in meta['var_info'].items():
            if var in tested:
                # test each variable only once
                continue
            assert info['units'] == VARUNITS[var]
            tested.append(var)
            stats.append(meta['station_name'])
        if len(tested) == len(VARS):

            break

    assert meta_key == 520
    assert stats == ['Abington', 'Abington', 'Abington (CT15)',
                     'Abington (CT15)', 'Abington (CT15)']

# TODO: test wetso4 (needs proper unit conversion)
testdata = [
    (0, 'Yellowstone NP', 'concentration_ugS/m3', 'concso2'),
    (1, 'Payerne', 'concentration_ugS/m3', 'concso4'),
    #(2, 'Abington (CT15)', 'deposition_kgS/ha', 'wetso4')
]

@lustre_unavail
@pytest.mark.parametrize('filenum,station_name,colname,var_name', testdata)
def test_reading_routines(aasetal_data, filenum, station_name, colname,
                          var_name):

    UNITCONVERSION = ReadAasEtal().UNITCONVERSION

    files = [os.path.join(DATA_DIR(), x) for x in FILENAMES]

    ungridded = aasetal_data

    df = pd.read_csv(files[filenum], sep=",", low_memory=False)
    subset = df[df.station_name == station_name]
    # values in original units
    vals = subset[colname].astype(float).values
    from_unit, to_unit = UNITCONVERSION[var_name]
    should_be = convert_unit(data=vals, from_unit=from_unit,
                             to_unit=to_unit, var_name=var_name).mean()

    actual = ungridded.to_station_data(station_name, var_name)[var_name].values.mean()

    if var_name == 'wetso4':
        raise NotImplementedError
        #from pyaerocom.helpers import get_tot_number_of_seconds

        #numsecs = get_tot_number_of_seconds(ts_type='monthly',
        #                                    dtime=station_group['dtime'])
        #stat[var] = stat[var]/numsecs
        #to_unit = 'kg m-2 s-1'
    npt.assert_almost_equal(should_be, actual)

if __name__ == "__main__":
    import sys
    #from pyaerocom.test.conftest import aasetal_data
    pytest.main(sys.argv)
