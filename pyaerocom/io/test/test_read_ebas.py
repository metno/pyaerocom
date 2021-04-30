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

from pyaerocom import const
import pyaerocom.exceptions as err
from pyaerocom.conftest import (testdata_unavail, EBAS_FILES,
                                EBAS_ISSUE_FILES,
                                EBAS_FILEDIR, does_not_raise_exception)

from pyaerocom.exceptions import (DataCoverageError,
                                  MetaDataError,
                                  TemporalResolutionError)
from pyaerocom.io.read_ebas import ReadEbas, ReadEbasOptions
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.io.ebas_varinfo import EbasVarInfo
import pyaerocom.mathutils as mu
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

@pytest.fixture(scope='module')
@testdata_unavail
def reader():
    r = ReadEbas('EBASSubset')
    return r

@testdata_unavail
class TestReadEbas(object):

    PROVIDES_VARIABLES = sorted([
                         'DEFAULT',
                         'sc550aer',
                         'sc440aer',
                         'sc700aer',
                         'sc550dryaer',
                         'sc440dryaer',
                         'sc700dryaer',
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
                         'concCec',
                         'concCecpm25',
                         'concCoc',
                         'concCocpm25',
                         'concNno3pm10',
                         'concNno3pm25',
                         'concNhno3',
                         'concNtno3',
                         'concNtnh',
                         'concss',
                         'concnh3',
                         'concNnh3',
                         'concNnh4',
                         'concno3',
                         'concnh4',
                         'concsspm10',
                         'concsspm25',
                         'concno2',
                         'conco3',
                         'concco',
                         'vmro3',
                         'vmrso2',
                         'vmrco',
                         'vmrno2',
                         'vmrno',
                         'concprcpoxs',
                         'concprcpoxn',
                         'concprcprdn',
                         'wetoxs',
                         'wetoxn',
                         'wetrdn',
                         'pr',
                         'concpm1',
                         'concca',
                         'concmg',
                         'conck'])

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
        assert reader.DEFAULT_VARS == reader.PROVIDES_VARIABLES

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

    def test_ASSUME_AE_SHIFT_WVL(self, reader):
        assert reader.ASSUME_AE_SHIFT_WVL == 1.0

    def test_ASSUME_AAE_SHIFT_WVL(self, reader):
        assert reader.ASSUME_AAE_SHIFT_WVL == 1.0

    def test_IGNORE_FILES(self, reader):
        assert reader.IGNORE_FILES == [
        'CA0420G.20100101000000.20190125102503.filter_absorption_photometer.aerosol_absorption_coefficient.aerosol.1y.1h.CA01L_Magee_AE31_ALT.CA01L_aethalometer.lev2.nas',
        'DK0022R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_22.DK01L_IC.lev2.nas',
        'DK0012R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_12.DK01L_IC.lev2.nas',
        'DK0008R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_08.DK01L_IC.lev2.nas',
        'DK0005R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_05.DK01L_IC.lev2.nas'
        ]

    OPTS = {'prefer_statistics': ['arithmetic mean', 'median'],
             'ignore_statistics': ['percentile:15.87', 'percentile:84.13'],
             'wavelength_tol_nm': 50,
             'shift_wavelengths': True,
             'assume_default_ae_if_unavail': True,
             'check_correct_MAAP_wrong_wvl': False,
             'eval_flags': True,
             'keep_aux_vars': False,
             'convert_units': True,
             'try_convert_vmr_conc' : True,
             'ensure_correct_freq': True,
             'freq_from_start_stop_meas': True,
             }

    def test_opts(self, reader):
        opts = reader._opts
        assert isinstance(opts, dict)
        assert 'default' in opts
        assert isinstance(opts['default'], ReadEbasOptions)
        assert len(self.OPTS) == len(opts['default'])
        for opt, val in opts['default'].items():
            assert opt in self.OPTS
            assert val == self.OPTS[opt]


    def test_data_id(self, reader):
        assert reader.data_id == 'EBASSubset'

    def test_file_dir(self, reader):
        fd = reader.file_dir
        assert reader._file_dir is None
        assert fd.endswith('data')
        assert os.path.exists(fd)
        with pytest.raises(FileNotFoundError):
            reader.file_dir = 42
        reader.file_dir = fd #sets private attr _file_dir
        assert reader._file_dir == reader.file_dir == fd

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

    def test_sqlite_database_file(self, reader):
        fp = reader.sqlite_database_file
        assert os.path.exists(fp)
        assert fp.endswith('ebas_file_index.sqlite3')

    @pytest.mark.parametrize('vars_to_retrieve,constraints,raises', [
        ('vmrno', {}, does_not_raise_exception()),
        ('vmrno', {'station_names' : 'xkcd'}, pytest.raises(FileNotFoundError)),
        ('sc550aer', {}, does_not_raise_exception()),
        ('sc550dryaer', {}, does_not_raise_exception()),
        ('sc550dryaer', {'station_names': 'Jungfraujoch'}, does_not_raise_exception()),
        ('ac550aer', {}, does_not_raise_exception()),
        ('concpm10', {}, does_not_raise_exception()),
        ('conco3', {}, does_not_raise_exception()),
        (['sc550aer', 'ac550aer', 'concpm10', 'conco3'], {'station_names': '*Kose*'}, does_not_raise_exception()),
        (['sc550aer', 'ac550aer', 'concpm10', 'conco3'], {}, does_not_raise_exception()),
        ])
    def test_get_file_list(self,reader,vars_to_retrieve,constraints,raises):
        with raises:
            lst = reader.get_file_list(vars_to_retrieve, **constraints)

            assert isinstance(lst, list)
            assert len(lst) > 0

    def test__merge_lists(self, reader):
        var = ['sc550aer', 'ac550aer']
        lst = reader.get_file_list(var)
        assert list(reader._lists_orig.keys()) == var
        merged = reader._merge_lists(reader._lists_orig)
        assert merged == lst

    @pytest.mark.parametrize('val,raises,output', [
        ('Bla', pytest.raises(FileNotFoundError), []),
        ('*fraujo*', does_not_raise_exception(), ['Jungfraujoch']),
        (42, pytest.raises(ValueError), None)
        ])
    def test__find_station_matches(self, reader,val,raises,output):
        with raises:
            assert reader._find_station_matches(val) == output

    @pytest.mark.parametrize('val,raises,output', [
        (['sconco3'], does_not_raise_exception(), ['conco3']),
        (None, does_not_raise_exception(), None)
        ])
    def test__precheck_vars_to_retrieve(self, reader,val,raises,output):
        if val is None:
            output = reader.PROVIDES_VARIABLES
        with raises:
            assert reader._precheck_vars_to_retrieve(val) == output

    @pytest.mark.parametrize('var,raises', [
        ('sc550aer', does_not_raise_exception()),
        ('blaaa', pytest.raises(err.VariableDefinitionError)),
        ('abs550aer', pytest.raises(err.VarNotAvailableError)),

        ])
    def test_get_ebas_var(self, reader, var, raises):
        with raises:
            vi = reader.get_ebas_var(var)
            assert isinstance(vi, EbasVarInfo)
            assert var in reader._loaded_ebas_vars

    @pytest.mark.parametrize('var,raises,colnums', [
        ('sc550aer', does_not_raise_exception(), [14, 17, 20]),
        ('ac550aer', pytest.raises(err.NotInFileError), None),
        ('sc550dryaer', pytest.raises(err.NotInFileError), None),
        ])
    def test__get_var_cols(self, reader, loaded_nasa_ames_example,
                           var, raises, colnums):
        vi = EbasVarInfo(var)
        with raises:
            cols = reader._get_var_cols(vi, loaded_nasa_ames_example)
            assert cols == colnums

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
    @pytest.mark.skip(reason='Updated in more recent dev version, example file not in testdata anymore')
    def test_find_var_cols(self, reader, loaded_nasa_ames_example):
        var = ['sc550aer', 'scrh']
        desired = {'sc550aer' : 17,
                   'scrh'     : 3}

        cols = reader.find_var_cols(var, loaded_nasa_ames_example)
        for k, v in desired.items():
            assert k in cols
            assert cols[k] == v

    @pytest.mark.parametrize('ts_type,tol_percent,num_flagged', [
        ('hourly', 5, 0),
        ('daily', 5, 8760),
        ('hourly', 0, 5840),
        ])
    def test__flag_incorrect_frequencies(self, reader, loaded_nasa_ames_example,
                                         ts_type, tol_percent, num_flagged):
        st = StationData()
        from pyaerocom import TsType
        _default_tol = TsType.TOL_SECS_PERCENT

        TsType.TOL_SECS_PERCENT = tol_percent

        num = len(loaded_nasa_ames_example.start_meas)
        st.start_meas = loaded_nasa_ames_example.start_meas
        st.stop_meas = loaded_nasa_ames_example.stop_meas
        st.var_info['bla'] = dict(units='1')
        st.bla = np.ones(num)
        st.ts_type=ts_type


        reader._flag_incorrect_frequencies(st)

        assert 'bla' in st.data_flagged
        flagged = st.data_flagged['bla']
        assert flagged.sum() == num_flagged
        TsType.TOL_SECS_PERCENT = _default_tol

    conco3_tower_var_info = {'conco3': {
        'name': 'ozone', 'units': 'ug m-3', 'tower_inlet_height': '50.0 m',
        'measurement_height': '50.0 m', 'instrument_name': 'uv_abs_kre_0050',
        'volume_std._temperature': '293.15 K',
        'volume_std._pressure': '1013.25 hPa',
        'detection_limit': '1.995 ug/m3',
        '"comment': "Data converted on import into EBAS from 'nmol/mol' to 'ug/m3' at standard conditions (293.15 K", 'matrix': 'air', 'statistics': 'arithmetic mean'}
        }
    vmro3_tower_var_info = {'vmro3': {
        'name': 'ozone', 'units': 'nmol mol-1', 'tower_inlet_height': '50.0 m',
        'measurement_height': '50.0 m', 'instrument_name': 'uv_abs_kre_0050',
        'detection_limit': '1.0 nmol/mol',
        '"comment': "Data converted on import into EBAS from 'nmol/mol' to 'ug/m3' at standard conditions (293.15 K", 'matrix': 'air', 'statistics': 'arithmetic mean'}}


    @pytest.mark.parametrize('filename,vars_to_retrieve,raises,check_attrs', [
        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['o3_tower']), 'vmro3',
         does_not_raise_exception(), {'var_info' : vmro3_tower_var_info}),
        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['o3_tower']), 'conco3',
         does_not_raise_exception(), {'var_info' : conco3_tower_var_info}),


        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['pm10_tstype']), 'concpm10',
         does_not_raise_exception(), {'ts_type' : '2daily'}),
        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['pm10_colsel']), 'concpm10',
         pytest.raises(ValueError), {}),
        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['o3_neg_dt']), 'conco3',
         pytest.raises(TemporalResolutionError), {}),
        (EBAS_FILEDIR.joinpath(EBAS_ISSUE_FILES['o3_tstype']), 'conco3',
         pytest.raises(TemporalResolutionError), {}),
        (EBAS_FILEDIR.joinpath(EBAS_FILES['sc550dryaer']['Jungfraujoch'][0]),
         ['sc550aer'],does_not_raise_exception(), {'station_name' : 'Jungfraujoch'}),


        ])
    def test_read_file(self, reader, filename, vars_to_retrieve, raises,
                       check_attrs):
        with raises:
            data = reader.read_file(filename=filename,
                                    vars_to_retrieve=vars_to_retrieve)
            assert isinstance(data, StationData)
            for key, val in check_attrs.items():
                assert data[key] == val

    def get_ebas_filelist(var_name):
        files = []
        for stat, filenames in EBAS_FILES[var_name].items():
            for filename in filenames:
                fp = EBAS_FILEDIR.joinpath(filename)
                assert fp.exists()
                files.append(str(fp))
        return files

    def test__try_get_pt_conversion(self, reader):
        fname = 'CH0001G.19910101000000.20181029122358.uv_abs.ozone.air.1y.1h.CH01L_TEI94C_1.CH01L_O3..nas'
        fp = os.path.join(reader.file_dir, fname)
        assert os.path.exists(fp)
        data = EbasNasaAmesFile(fp)
        with pytest.raises(MetaDataError):
            reader._try_get_pt_conversion(data.meta)
        p, T = reader._try_get_pt_conversion(data.var_defs[2])
        assert p == 65300 #Pa
        assert T == 265.15 #K


    @pytest.mark.parametrize(
        'vars_to_retrieve,first_file,last_file,files,constraints,num_meta,num_stats,raises', [
            ('concno2',None,None,get_ebas_filelist('concno2'),{}, 2, 2, does_not_raise_exception()),
            ('vmrno2',None,None,get_ebas_filelist('vmrno2'),{}, 2, 2, does_not_raise_exception()),
            ('vmrno2',None,None,get_ebas_filelist('vmrno2') + get_ebas_filelist('concno2'), {}, 4, 4, does_not_raise_exception()),
            ('conco3',None,None,get_ebas_filelist('conco3'),{}, 4, 4, does_not_raise_exception()),
            ('vmro3',None,None,get_ebas_filelist('conco3'),{}, 4, 4, does_not_raise_exception()),
            ('concpm10',None,None,get_ebas_filelist('concpm10'),{}, 4, 4, does_not_raise_exception()),
            ('sc550aer',None,None,None,{}, 5, 4, does_not_raise_exception()),
            ('sc550dryaer',None,None,get_ebas_filelist('sc550dryaer'),{}, 5, 4, does_not_raise_exception()),
            ('ac550aer',None,None,get_ebas_filelist('sc550dryaer'),{}, 4, 4, pytest.raises(DataCoverageError)),
            ('ac550aer',None,None,get_ebas_filelist('ac550aer'),{}, 4, 4, does_not_raise_exception()),

            ])
    def test_read(self, reader, vars_to_retrieve, first_file,
                  last_file, files, constraints, num_meta, num_stats, raises):
        with raises:
            data = reader.read(vars_to_retrieve, first_file,
                      last_file, files, **constraints)
            assert isinstance(data, UngriddedData)
            assert len(data.metadata) == num_meta
            assert len(data.unique_station_names) == num_stats
            if isinstance(vars_to_retrieve, str):
                vars_to_retrieve = [vars_to_retrieve]
            for meta in data.metadata.values():
                for var in vars_to_retrieve:
                    if var in meta['var_info']:
                        unit_desired = const.VARS[var].units
                        assert meta['var_info'][var]['units'] == unit_desired

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
