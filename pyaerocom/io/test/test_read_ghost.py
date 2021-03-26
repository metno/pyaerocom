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
from pyaerocom.conftest import lustre_unavail
from pyaerocom.io.read_ghost import ReadGhost
import numpy as np

@pytest.fixture(scope='module')
def ghost_eea_daily():
    return ReadGhost('G.EEA.daily.Subset')

@pytest.fixture(scope='module')
def ghost_eea_hourly():
    return ReadGhost('G.EEA.hourly.Subset')

class TestReadGhost(object):
    PROVIDES_VARIABLES = ['concpm10', 'concpm10al', 'concpm10as', 'concpm25',
                          'concpm1', 'conccl', 'concso4', 'vmrco', 'vmrno',
                          'vmrno2', 'vmro3', 'vmrso2', 'concno3', 'concnh4',
                          'concco', 'concno', 'concno2', 'conco3', 'concso2']

    INVDICT = {'pm10': 'concpm10', 'pm10al': 'concpm10al',
               'pm10as': 'concpm10as', 'pm2p5': 'concpm25',
               'pm1': 'concpm1', 'sconccl': 'conccl', 'sconcso4': 'concso4',
               'sconcco': 'vmrco', 'sconcno': 'vmrno', 'sconcno2': 'vmrno2',
               'sconco3': 'vmro3', 'sconcso2': 'vmrso2', 'sconcno3': 'concno3',
               'sconcnh4': 'concnh4'}

    DEFAULT_VAR = 'conco3'
    DEFAULT_SITE = None

    fixture_names = ('ghost_eea_daily', 'ghost_eea_hourly')

    # cf.: https://hackebrot.github.io/pytest-tricks/fixtures_as_class_attributes/
    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        for name in self.fixture_names:
            setattr(self, name, request.getfixturevalue(name))

    @property
    def default_reader(self):
        """Just a convenience thing used in tests below that would be redundant
        if applied to daily and hourly"""
        return self.get_reader('ghost_eea_daily')

    def get_reader(self, fixture_name):
        return getattr(self, fixture_name)

    def test_meta_keys(self):
        assert len(self.default_reader.META_KEYS) == 142

    @pytest.mark.parametrize('fixture_name', ['ghost_eea_daily', 'ghost_eea_hourly'])
    def test_PROVIDES_VARIABLES(self, fixture_name):
        reader = self.get_reader(fixture_name)
        assert len(reader.PROVIDES_VARIABLES) == len(self.PROVIDES_VARIABLES)
        assert all([x in self.PROVIDES_VARIABLES for x in reader.PROVIDES_VARIABLES])

    def test_var_names_data_inv(self):
        invdict = self.default_reader.var_names_data_inv
        assert isinstance(invdict, dict)
        for key, val in invdict.items():
            assert self.INVDICT[key] == val

    @pytest.mark.parametrize(
        'fixture_name,vars_to_read,pattern,filenum,lastfilename', [
        ('ghost_eea_daily','vmro3',None,1,'sconco3_201810.nc'),
        ('ghost_eea_hourly','vmro3',None,1,'sconco3_201810.nc'),
        ('ghost_eea_daily','concpm10',None,3,'pm10_201912.nc'),
        ('ghost_eea_daily','vmro3','*201810.nc',1,'sconco3_201810.nc'),
        ])
    def test_get_file_list(self, fixture_name, vars_to_read, pattern, filenum,
                           lastfilename):
        files = self.get_reader(fixture_name).get_file_list(
                vars_to_read=vars_to_read,
                pattern=pattern)

        assert len(files) == filenum
        assert os.path.basename(files[-1]) == lastfilename

    def test__ts_type_from_DATASET_PATH(self):
        assert self.get_reader('ghost_eea_daily')._ts_type_from_DATASET_PATH() == 'daily'

    @pytest.mark.parametrize('fixture_name,val', [
            ('ghost_eea_daily', 'daily'),
            ('ghost_eea_hourly', 'hourly')
        ])
    def test_TS_TYPE(self, fixture_name, val):
        assert self.get_reader(fixture_name).TS_TYPE == val

    def test_get_meta_filename(self):
        import pandas as pd
        meta = self.default_reader.get_meta_filename('pm10_201910.nc')
        per = pd.Period(freq='M', year=2019, month=10)
        desired = dict(var_name='pm10',
                       start=per.start_time,
                       stop=per.end_time)
        for key, val in meta.items():
            assert desired[key] == val

    def test__eval_flags_slice(self):
        import xarray as xr
        reader = self.default_reader
        file = reader.files[-1]
        assert os.path.basename(file) == 'sconco3_201810.nc'
        ds = xr.open_dataset(file)

        flagvar = 'qa'
        numvalid = 3
        shape = (1,3)

        assert 'sconco3' in ds
        assert ds['sconco3'].shape == shape
        assert flagvar in reader.FLAG_DIMNAMES

        flagvar_dimname = reader.FLAG_DIMNAMES[flagvar]

        assert flagvar_dimname in ds.dims

        flags = ds[flagvar]

        invalidate = reader.DEFAULT_FLAGS_INVALID[flagvar]

        slice_dim = flags.dims.index(flagvar_dimname)
        valid = np.apply_along_axis(reader._eval_flags_slice,
                                    slice_dim, flags.values,
                                    invalidate)
        assert valid.ndim == 2
        assert valid.shape == shape
        assert valid.sum() == numvalid

    @pytest.mark.parametrize('fixture_name,statnum,first_stat_name', [
        ('ghost_eea_daily', 1, 'Bleak House'),
        ])
    def test_read_file(self, fixture_name, statnum, first_stat_name):
        reader = self.get_reader(fixture_name)
        data = reader.read_file(reader.files[-1])
        assert isinstance(data, list)
        assert len(data) == statnum
        first_stat = data[0]
        assert isinstance(first_stat, dict)
        assert first_stat['meta']['station_name'] == first_stat_name

if __name__ == '__main__':
    import os
    import sys
    pytest.main(sys.argv)

# =============================================================================
#     reader =  ReadGhost()
#     from time import time
#     for var in reader.PROVIDES_VARIABLES:
#         lst = reader.get_file_list(var)
#         print(os.path.basename(lst[-1]))
#         t0 =time()
#         reader.read_file(lst[-1], var_to_read=var)
#         print('{:.1f} s'.format(time()-t0))
# =============================================================================
