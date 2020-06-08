#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:27:28 2019

@author: jonasg
"""
import pytest
import numpy as np
import numpy.testing as npt
import iris
from cf_units import Unit

from pyaerocom.conftest import (TEST_RTOL, testdata_unavail)
from pyaerocom.colocation import colocate_gridded_ungridded
from pyaerocom.colocateddata import ColocatedData
from pyaerocom import GriddedData
from pyaerocom import helpers

@testdata_unavail
@pytest.mark.parametrize('addargs,ts_type,shape,obsmean,modmean',[
    (dict(),
     'monthly', (2,12,8), 0.315930,0.275671),
    (dict(var_ref_outlier_ranges={'od550aer':[0.1,0.5]},
          var_outlier_ranges={'od550aer':[0.1,0.2]}),
     'monthly', (2,12,8), 0.227333,0.275671),
    (dict(apply_time_resampling_constraints=False),
     'monthly', (2,12,8), 0.316924,0.275671),
    (dict(filter_name='WORLD-wMOUNTAINS'),
     'monthly', (2,12,11), 0.269707, 0.243861),
    (dict(use_climatology_ref=True),
     'monthly', (2,12,13), 0.302636, 0.234147)
    ])
def test_colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset,
                                    addargs, ts_type, shape,
                                    obsmean, modmean):
    coldata = colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset,
                                         **addargs)

    assert isinstance(coldata, ColocatedData)
    assert coldata.ts_type == ts_type
    assert coldata.shape == shape

    means = [np.nanmean(coldata.data.data[0]),
             np.nanmean(coldata.data.data[1])]

    npt.assert_allclose(means, [obsmean, modmean], rtol=TEST_RTOL)

@testdata_unavail
def test_colocate_gridded_ungridded_nonglobal(aeronetsunv3lev2_subset):
    times = [1,2]
    time_unit = Unit("days since 1990-1-1 0:0:0")
    cubes = iris.cube.CubeList()

    for time in times:
        time_coord = iris.coords.DimCoord(time, units=time_unit, standard_name='time')
        cube = helpers.make_dummy_cube_latlon(lat_res_deg=1, lon_res_deg=1, lat_range=[30.05,81.95], lon_range=[-29.5,89.95])
        cube.add_aux_coord(time_coord)
        cubes.append(cube)
    time_cube = cubes.merge_cube()
    gridded = GriddedData(time_cube)
    gridded.var_name = 'od550aer'
    gridded.units = Unit('1')
    gridded.change_base_year(2018)

    coldata = colocate_gridded_ungridded(gridded, aeronetsunv3lev2_subset, colocate_time=False)
    coords = coldata.coords
    assert len(coords['station_name']) == 1

@pytest.mark.skip(reason='No fixture for gridded observation data available yet')
def test_colocate_gridded_gridded(mod, obs, addargs, **kwargs):
    pass

from pyaerocom.colocation_auto import Colocator
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.io.readgridded import ReadGridded
@pytest.mark.parametrize('reader_id,reader_class', [
    ('ReadEMEP', ReadEMEP),
    ('ReadGridded', ReadGridded)
    ])
def test_colocator_reader(reader_id, reader_class):
    col = Colocator(gridded_reader_id=reader_id)
    reader = col.get_gridded_reader()
    assert reader == reader_class

@testdata_unavail
def test_colocator_instantiate_model_reader(path_emep):
    col = Colocator(gridded_reader_id='ReadEMEP')
    col.filepath = path_emep['daily']
    r = col.instantiate_model_reader()
    assert isinstance(r, ReadEMEP)
    assert r.filepath == col.filepath


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
