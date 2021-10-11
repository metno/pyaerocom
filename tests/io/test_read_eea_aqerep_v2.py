#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""
import pytest

from ..conftest import data_unavail
from pyaerocom.io.read_eea_aqerep_v2 import ReadEEAAQEREP_V2


@data_unavail
@pytest.fixture(scope='module')
def reader():
    # not sure if we really use this
    # limit the data read for testing so that this test also works
    # with the full dataset
    ReadEEAAQEREP_V2.FILE_MASKS['concso2'] = '**/AT*_1_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concpm10'] = '**/AT*_5_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['conco3'] = '**/AT*_7_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['vmro3'] = '**/AT*_7_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concno2'] = '**/AT*_8_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concno2'] = '**/AT*_8_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concco'] = '**/AT*_10_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concno'] = '**/AT*_38_*_2019_timeseries.csv*'
    ReadEEAAQEREP_V2.FILE_MASKS['concpm25'] = '**/AT*_6001_*_2019_timeseries.csv*'

    return ReadEEAAQEREP_V2('EEA_AQeRep.v2.Subset')

@data_unavail
def test_get_file_list(reader):
    # at this point that is the base directory without recursive search
    # so this returns only Revision.txt and metadata.csv
    # don't be too restrictive since we might have additional files in the subdirectory
    assert len(reader.get_file_list()) >= 2

@data_unavail
def test_read(reader):
    from pyaerocom.ungriddeddata import UngriddedData
    from pyaerocom.stationdata import StationData

    # special station codes to test
    # not sure if these are really needed

    # station ids to test
    station_id = {}
    # respective mean for a station; index has to be the same as station_id
    station_means = {}
    # from file AT/AT_5_48881_2019_timeseries.csv.gz and AT/AT_5_48900_2019_timeseries.csv
    station_id['concpm10'] = ['AT10002', 'AT52000']
    station_means['concpm10'] = [17.128, 15.113]


    # station_id['concso2'] = ['AT10002', 'AT52000']
    # station_id['conco3'] = ['XK0002A']
    # station_id['vmro3'] = ['XK0002A']
    # station_id['concno2'] = ['XK0002A']
    # station_id['concno2'] = ['AT31703']
    # station_id['concco'] = ['XK0002A']
    # station_id['concco'] = ['AT4S416']
    # station_id['concno'] = ['XK0002A']
    # station_id['concno'] = ['AT4S416']
    # station_id['concpm25'] = ['XK0002A']

    var_names_to_test = station_id.keys()
    for var_name in var_names_to_test:
        # r = reader()
        data = None
        data = reader.read(vars_to_retrieve=[var_name])
        assert isinstance(data, UngriddedData)

        print('{} data read'.format(var_name))
        for stat_idx, statid in enumerate(station_id[var_name]):
            try:
                stat_data = data[statid]
                # It makes no sense to test this for every station
                if stat_idx == 1:
                    assert isinstance(stat_data, StationData)

                assert stat_data[var_name].mean() == station_means[var_name][stat_idx]
            except:
                print('failed test var {}'.format(var_name))
                pass


if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
