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
import pandas as pd
from cf_units import Unit

from pyaerocom.conftest import (TEST_RTOL, testdata_unavail)
from pyaerocom.colocation import (_regrid_gridded,
                                  _colocate_site_data_helper,
                                  colocate_gridded_ungridded,
                                  colocate_gridded_gridded)
from pyaerocom.colocateddata import ColocatedData
from pyaerocom import GriddedData
from pyaerocom import helpers
from pyaerocom.io import ReadMscwCtm

def test__regrid_gridded(data_tm5):
     one_way = _regrid_gridded(data_tm5, 'areaweighted', 5)
     another_way = _regrid_gridded(data_tm5, 'areaweighted',
                                   dict(lon_res_deg=5, lat_res_deg=5))

     assert one_way.shape == another_way.shape

def test__colocate_site_data_helper(aeronetsunv3lev2_subset):
    var = 'od550aer'
    stat1 = aeronetsunv3lev2_subset.to_station_data(3, var)
    stat2 = aeronetsunv3lev2_subset.to_station_data(4, var)
    df = _colocate_site_data_helper(stat1, stat2, var, var,
                                    'daily',None,False,None,False)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 9483
    means = [np.nanmean(df['data']),
             np.nanmean(df['ref'])]
    should_be = [0.31171085422102346,
                 0.07752743643132792]
    npt.assert_allclose(means, should_be, rtol=1e-5)

def test_colocate_gridded_ungridded_new_var(data_tm5, aeronetsunv3lev2_subset):
    data = data_tm5.copy()
    data.var_name='Blaaa'
    coldata = colocate_gridded_ungridded(data, aeronetsunv3lev2_subset,
                                         var_ref='od550aer')

    assert coldata.metadata['var_name'] == ['od550aer', 'Blaaa']

@testdata_unavail
@pytest.mark.parametrize('addargs,ts_type,shape,obsmean,modmean',[
    (dict(),
     'monthly', (2,12,8), 0.315930,0.275671),
    (dict(apply_time_resampling_constraints=False),
     'monthly', (2,12,8), 0.316924,0.275671),
    (dict(filter_name='WORLD-wMOUNTAINS'),
     'monthly', (2,12,11), 0.269707, 0.243861),
    (dict(use_climatology_ref=True),
     'monthly', (2,12,13), 0.302636, 0.234147),
    (dict(regrid_res_deg=30),
     'monthly', (2,12,8), 0.31593 , 0.169897),
    (dict(ts_type='yearly', apply_time_resampling_constraints=False),
     'yearly', (2,1,8), 0.417676, 0.275671)

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


@testdata_unavail
def test_colocate_gridded_gridded_same_new_var(data_tm5):
    data = data_tm5.copy()
    data.var_name = 'Blaaa'
    coldata = colocate_gridded_gridded(data, data_tm5)

    assert coldata.metadata['var_name'] == ['od550aer', 'Blaaa']

@testdata_unavail
def test_colocate_gridded_gridded_same(data_tm5):
    coldata = colocate_gridded_gridded(data_tm5, data_tm5)

    assert isinstance(coldata, ColocatedData)
    stats = coldata.calc_statistics()
    # check mean value
    npt.assert_allclose(stats['data_mean'], 0.09825691)
    # check that mean value is same as in input GriddedData object
    npt.assert_allclose(stats['data_mean'], data_tm5.mean(areaweighted=False))
    assert stats['refdata_mean'] == stats['data_mean']
    assert stats['nmb'] == 0
    assert stats['mnmb'] == 0
    assert stats['R'] == 1
    assert stats['R_spearman'] == 1

@testdata_unavail
def test_read_emep_colocate_emep_tm5(data_tm5, path_emep):
    filepath = path_emep['monthly']
    r = ReadMscwCtm(path_emep['monthly'])
    data_emep = r.read_var('concpm10', ts_type='monthly')

    # Change units and year to match TM5 data
    data_emep.change_base_year(2010)
    data_emep.units = '1'
    col = colocate_gridded_gridded(data_emep, data_tm5)
    assert isinstance(col, ColocatedData)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
