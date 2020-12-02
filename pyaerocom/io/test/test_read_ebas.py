#!/usr/bin/env python3
# this file is part of the pyaerocom package
# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# Author: Jonas Gliss
# E-mail: jonasg@met.no
# License: https://github.com/metno/pyaerocom/blob/master/LICENSE
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

import pytest
import os
import numpy as np
import numpy.testing as npt

from pyaerocom import const
from pyaerocom.conftest import testdata_unavail, NASA_AMES_FILEPATHS
from pyaerocom.io.read_ebas import ReadEbas, ReadEbasOptions
from pyaerocom.io.ebas_varinfo import EbasVarInfo
import pyaerocom.mathutils as mu
from pyaerocom.stationdata import StationData

@pytest.fixture(scope='module')
@testdata_unavail
def reader():
    return ReadEbas('EBASSubset')

@testdata_unavail
class TestReadEBAS(object):

    PROVIDES_VARIABLES = ['DEFAULT',
                         'sc550aer',
                         'sc440aer',
                         'sc700aer',
                         'sc550dryaer',
                         'sc440dryaer',
                         'sc700dryaer',
                         'ang4470dryaer',
                         'sc550lt1aer',
                         'bsc550aer',
                         'ac550aer',
                         'ac550dryaer',
                         'ac550lt1aer',
                         'bsc550dryaer',
                         'scrh',
                         'acrh',
                         'concso4',
                         'concso2',
                         'concpm10',
                         'concpm25',
                         'concso4t',
                         'concso4c',
                         'concbc',
                         'conceqbc',
                         'conctc',
                         'concoa',
                         'concoc',
                         'concss',
                         'concnh3',
                         'concno3',
                         'concnh4',
                         'conchno3',
                         'conctno3',
                         'concno2',
                         'conco3',
                         'concco',
                         'vmro3',
                         'vmrso2',
                         'vmrco',
                         'vmrno2',
                         'vmrno',
                         'concprcpso4',
                         'concprcpso4t',
                         'concprcpso4c',
                         'concprcpno3',
                         'concprcpso4scavenging',
                         'concprcpnh4',
                         'wetso4',
                         'wetconcso4',
                         'wetso4t',
                         'wetso4c',
                         'wetoxn',
                         'wetrdn',
                         'wetnh4',
                         'precip',
                         'wetconcph',
                         'wetno3',
                         'scavratioso4',
                         'test',
                         'concpm1']

    def test_DATA_ID(self, reader):
        assert reader.data_id == 'EBASSubset'

    def test_FILE_SUBDIR_NAME(self, reader):
        assert reader.FILE_SUBDIR_NAME == 'data'
    #: Name of sqlite database file

    def test_SQL_DB_NAME(self, reader):
        assert reader.SQL_DB_NAME == 'ebas_file_index.sqlite3'

    def test_SUPPORTED_DATASETS(self, reader):
        assert reader.SUPPORTED_DATASETS == ['EBASMC', 'EBASSubset']

    def test_CACHE_SQLITE_FILE(self, reader):
        assert reader.CACHE_SQLITE_FILE == ['EBASMC']

    def test_TS_TYPE(self, reader):
        assert reader.TS_TYPE == 'undefined'

    def test_MERGE_STATIONS(self, reader):
        assert reader.MERGE_STATIONS == {'Birkenes' : 'Birkenes II'}

    def test_DEFAULT_VARS(self, reader):
        assert reader.DEFAULT_VARS == ['ac550aer','sc550aer']

    def test_TS_TYPE_CODES(self, reader):
        assert reader.TS_TYPE_CODES == {'1mn'  :   'minutely',
                                         '1h'   :   'hourly',
                                         '1d'   :   'daily',
                                         '1w'   :   'weekly',
                                         '1mo'  :   'monthly',
                                         'mn'   :   'minutely',
                                         'h'    :   'hourly',
                                         'd'    :   'daily',
                                         'w'    :   'weekly',
                                         'mo'   :   'monthly'}

    AUX_REQUIRES = {'sc550dryaer'    :   ['sc550aer',
                                          'scrh'],
                    'sc440dryaer'    :   ['sc440aer',
                                          'scrh'],
                    'sc700dryaer'    :   ['sc700aer',
                                          'scrh'],
                    'ac550dryaer'    :   ['ac550aer',
                                          'acrh'],
                    'ang4470dryaer'  :   ['sc440dryaer',
                                          'sc700dryaer']}

    def test_AUX_REQUIRES(self, reader):
        for var, req in self.AUX_REQUIRES.items():
            assert var in reader.AUX_REQUIRES
            assert req == reader.AUX_REQUIRES[var]

    AUX_USE_META = {'sc550dryaer'    :   'sc550aer',
                    'sc440dryaer'    :   'sc440aer',
                    'sc700dryaer'    :   'sc700aer',
                    'ac550dryaer'    :   'ac550aer'}

    def test_AUX_USE_META(self, reader):
        for var, ovar in self.AUX_USE_META.items():
            assert var in reader.AUX_USE_META
            assert reader.AUX_USE_META[var] == ovar

    AUX_FUNS = {'sc440dryaer'    :   mu.compute_sc440dryaer,
                'sc550dryaer'    :   mu.compute_sc550dryaer,
                'sc700dryaer'    :   mu.compute_sc700dryaer,
                'ac550dryaer'    :   mu.compute_ac550dryaer,
                'ang4470dryaer'  :   mu.compute_ang4470dryaer_from_dry_scat}

    def test_AUX_FUNS(self, reader):
        for var, func in self.AUX_FUNS.items():
            assert var in reader.AUX_FUNS
            assert reader.AUX_FUNS[var] == func

    def test_IGNORE_WAVELENGTH(self, reader):
        assert reader.IGNORE_WAVELENGTH == ['conceqbc']

    def test_ASSUME_AE_SHIFT_WVL(self, reader):
        assert reader.ASSUME_AE_SHIFT_WVL == 1.0

    def test_ASSUME_AAE_SHIFT_WVL(self, reader):
        assert reader.ASSUME_AAE_SHIFT_WVL == 1.0

    def test_IGNORE_FILES(self, reader):
        assert reader.IGNORE_FILES == ['CA0420G.20100101000000.20190125102503.filter_absorption_photometer.aerosol_absorption_coefficient.aerosol.1y.1h.CA01L_Magee_AE31_ALT.CA01L_aethalometer.lev2.nas']

    OPTS = {'prefer_statistics': ['arithmetic mean', 'median'],
             'ignore_statistics': ['percentile:15.87', 'percentile:84.13'],
             'wavelength_tol_nm': 50,
             'shift_wavelengths': True,
             'assume_default_ae_if_unavail': True,
             'check_correct_MAAP_wrong_wvl': False,
             'eval_flags': True,
             'keep_aux_vars': False,
             'merge_meta': False,
             'convert_units': True}

    def test_opts(self, reader):
        assert isinstance(reader.opts, ReadEbasOptions)
        assert len(self.OPTS) == len(reader.opts)
        for opt, val in reader.opts.items():
            assert opt in self.OPTS
            assert val == self.OPTS[opt]

    def test_data_id(self, reader):
        assert reader.data_id == 'EBASSubset'

    def test_file_dir(self, reader):
        fd = reader.file_dir
        assert fd.endswith('data')
        assert os.path.exists(fd)
        with pytest.raises(FileNotFoundError):
            reader.file_dir = 42

    def test_FILE_REQUEST_OPTS(self, reader):
        assert reader.FILE_REQUEST_OPTS == ['variables',
                                            'start_date',
                                            'stop_date',
                                            'station_names',
                                            'matrices',
                                            'altitude_range',
                                            'lon_range',
                                            'lat_range',
                                            'instrument_types',
                                            'statistics',
                                            'datalevel']

    def test__FILEMASK(self, reader):
        with pytest.raises(AttributeError):
            reader._FILEMASK

    def test_NAN_VAL(self, reader):
        with pytest.raises(AttributeError):
            reader.NAN_VAL

    def test_PROVIDES_VARIABLES(self, reader):

        assert sorted(reader.PROVIDES_VARIABLES) == sorted(self.PROVIDES_VARIABLES)

    def test_prefer_statistics(self, reader):
        assert reader.prefer_statistics == ['arithmetic mean', 'median']

    def test_ignore_statistics(self, reader):
        assert reader.ignore_statistics == ['percentile:15.87',
                                            'percentile:84.13']

    def test_wavelength_tol_nm(self, reader):
        assert reader.wavelength_tol_nm == 50

    def test_keep_aux_vars(self, reader):
        assert reader.keep_aux_vars == False

    def test_merge_meta(self, reader):
        assert reader.merge_meta == False

    def test_eval_flags(self, reader):
        assert reader.eval_flags == True

    def test_sqlite_database_file(self, reader):
        fp = reader.sqlite_database_file
        assert os.path.exists(fp)
        assert fp.endswith('ebas_file_index.sqlite3')

    @pytest.mark.parametrize('vars_to_retrieve,constraints,num_files', [
        ('sc550aer', {}, 5),
        ('sc550dryaer', {}, 5),
        ('sc550dryaer', {'station_names': 'Jungfraujoch'}, 2),
        ('ac550aer', {}, 4),
        ('concpm10', {}, 4),
        ('conco3', {}, 4),
        (['sc550aer', 'ac550aer', 'concpm10', 'conco3'], {'station_names': '*Kose*'}, 4),
        (['sc550aer', 'ac550aer', 'concpm10', 'conco3'], {}, 17),
        ])
    def test_get_file_list(self, reader, vars_to_retrieve, constraints,
                           num_files):

        lst = reader.get_file_list(vars_to_retrieve, **constraints)

        assert isinstance(lst, list)
        assert len(lst)==num_files

    def test__merge_lists(self, reader):
        var = ['sc550aer', 'ac550aer']
        lst = reader.get_file_list(var)
        assert list(reader._lists_orig.keys()) == var
        merged = reader._merge_lists(reader._lists_orig)
        assert merged == lst

    def test_find_station_matches(self, reader):
        assert reader.find_station_matches('*fraujo*') == ['Jungfraujoch']

    def test__precheck_vars_to_retrieve(self, reader):
        assert reader._precheck_vars_to_retrieve(['sconco3']) == ['conco3']

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__get_var_cols(self, reader):
        pass

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__find_best_data_column(self):
        pass

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__add_meta(self):
        pass

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__find_wavelength_matches(self):
        pass

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__find_closest_wavelength_cols(self):
        pass

    @pytest.mark.skip(reason='Not implemented, is tested via read_file')
    def test__shift_wavelength(self):
        pass

    def test_find_var_cols(self, reader, loaded_nasa_ames_example):
        var = ['sc550aer', 'scrh']
        desired = {'sc550aer' : 17,
                   'scrh'     : 3}

        cols = reader.find_var_cols(var, loaded_nasa_ames_example)
        for k, v in desired.items():
            assert k in cols
            assert cols[k] == v

    @pytest.mark.parametrize('var', ['sc550aer'])
    def test_get_ebas_var(self, reader, var):
        vi = reader.get_ebas_var(var)
        assert isinstance(vi, EbasVarInfo)
        assert var in reader._loaded_ebas_vars

    @pytest.mark.parametrize('filename,vars_to_retrieve,start,stop,totnum,'
                             'var_nanmeans,var_numnans,var_units,meta', [
        (NASA_AMES_FILEPATHS['scatc_jfj'], ['scrh'],
         np.datetime64('2018-01-01T00:30:00'),
         np.datetime64('2018-12-31T23:29:59'),
        8760,8.2679,78,['%'],
        {'latitude': 46.5475, 'longitude': 7.985, 'altitude': 3580.0,
         'filename': 'CH0001G.20180101000000.20190520124723.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas',
         'station_id': 'CH0001G', 'station_name': 'Jungfraujoch',
         'instrument_name': 'TSI_3563_JFJ_dry',
         'PI': 'Bukowiecki, Nicolas; Baltensperger, Urs',
         'ts_type': 'hourly', 'data_id': 'EBASSubset', 'data_level': 2,
         'revision_date': np.datetime64('2019-05-20T00:00:00'),
         'framework' : 'ACTRIS CREATE EMEP GAW-WDCA'})
        ])
    def test_read_file(self, reader, filename, vars_to_retrieve, start,
                       stop, totnum, var_nanmeans, var_numnans, var_units,
                       meta):
        data = reader.read_file(filename=filename,
                                vars_to_retrieve=vars_to_retrieve)
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        assert isinstance(data, StationData)
        assert isinstance(data, dict)
        assert 'var_info' in data
        assert [var in data for var in vars_to_retrieve]
        assert [var in data['var_info'] for var in vars_to_retrieve]
        assert data.dtime[0] == start
        assert data.dtime[-1] == stop
        assert len(data.dtime) == totnum
        nanmeans = []
        numnans = []
        varunits = []
        for i, var in enumerate(vars_to_retrieve):
            assert isinstance(data[var], np.ndarray)
            varunits.append(data['var_info'][var]['units'])
            nanmeans.append(np.nanmean(data[var]))
            numnans.append(np.isnan(data[var]).sum())
        npt.assert_allclose(nanmeans, var_nanmeans, rtol=1e-3)
        npt.assert_array_equal(numnans, var_numnans)
        npt.assert_array_equal(varunits, var_units)

        _meta = data.get_meta()
        assert len(_meta) == len(meta)
        for key, val in _meta.items():
            assert val == meta[key]

if __name__ == '__main__':
    import os
    import sys
    pytest.main(sys.argv)