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

def test_provides_variables():
    assert ReadGhost.PROVIDES_VARIABLES == ['concpm10', 'concpm25', 'concco', 
                                            'concno', 'concno2', 'conco3', 
                                            'concso2']
    
@pytest.fixture(scope='module', params=['GHOST.daily', 'GHOST.hourly'])
def reader(request):
    yield ReadGhost(request.param)

@lustre_unavail
@pytest.mark.parametrize('var,filenum,lastfilename',[
    ('sconco3',24,'sconco3_201912.nc'),
    ])
def test_get_file_list(reader, var, filenum, lastfilename):
    files = reader.get_file_list(var)
    assert len(files) == filenum
    assert os.path.basename(files[-1]) == lastfilename

# =============================================================================
# @lustre_unavail
# def test_read_file(reader):
#     from pyaerocom.stationdata import StationData
#     file = reader.files[-3]
#     assert os.path.basename(file) == 'Thessaloniki.lev30'
#     data = reader.read_file(file)
#     assert isinstance(data, StationData)
#     assert data.latitude[0] == 40.63
#     assert data.longitude[0] == 22.96
#     assert data.station_name[0] == 'Thessaloniki'
#     assert all(x in data for x in ['od550aer', 'ang4487aer'])
#     
#     actual = [data['od550aer'][:10].mean(), data['ang4487aer'][:10].mean()]
#     desired = [0.287, 1.787]
#     npt.assert_allclose(actual, desired, rtol=1e-3)
#     
# 
# @lustre_unavail
# def test_read(reader):
#     from pyaerocom.ungriddeddata import UngriddedData
#     files = reader.files[2:4]
#     assert all(os.path.basename(x) in ('Agoufou.lev30', 'Alta_Floresta.lev30')
#                for x in files)
#     data = reader.read(files=files)
#     
#     assert isinstance(data, UngriddedData)
#     assert data.unique_station_names == ['Agoufou', 'Alta_Floresta']
#     assert data.contains_vars == ['od550aer', 'ang4487aer']
#     assert data.contains_instruments == ['sun_photometer']
#     assert data.shape == (11990, 12)
#     npt.assert_allclose(np.nanmean(data._data[:, data._DATAINDEX]), 0.676, 
#                         rtol=1e-3)
# =============================================================================
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
        
