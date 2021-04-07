#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 10:14:59 2020

@author: jonasg
"""

import pytest
import numpy as np
import numpy.testing as npt
from pyaerocom.conftest import (aeronetsdav3lev2_subset,
                                aeronetsunv3lev2_subset,
                                does_not_raise_exception)

import pyaerocom.combine_vardata_ungridded as testmod

SUN_DATA = aeronetsunv3lev2_subset
SDA_DATA = aeronetsdav3lev2_subset

TESTSTAT = 'Mauna_Loa'

@pytest.fixture(scope='module')
def stats_sun_aod(SUN_DATA):
    return SUN_DATA.to_station_data_all('od550aer')

@pytest.fixture(scope='module')
def stats_sun_ang(SUN_DATA):
    return SUN_DATA.to_station_data_all('ang4487aer')

@pytest.fixture(scope='module')
def stats_sda_aod(SDA_DATA):
    return SDA_DATA.to_station_data_all('od550aer')

@pytest.fixture(scope='module')
def stats_sda_fineaod(SDA_DATA):
    return SDA_DATA.to_station_data_all('od550lt1aer')

SUN_ID = 'AeronetSunV3L2Subset.daily'
SDA_ID = 'AeronetSDAV3L2Subset.daily'

OD450FUN = f'{SUN_ID};od550aer*(450/550)**(-{SUN_ID};ang4487aer)'
@pytest.mark.parametrize('var1,var2,add_args,numst,mean_first,expectation', [
    ('od550aer', 'od550aer', {}, 13, {'od550aer' : 0.5}, pytest.raises(ValueError)),
    ('od550aer', 'ang4487aer',
     {'merge_how' : 'mean',
      'var_name_out' : 'blaaa'}, 13, {'blaaa' : 0.251},
     pytest.raises(NotImplementedError)),
    ('od550aer', 'ang4487aer', {}, 18,
     {'od550aer' : 0.50155,
      'ang4487aer' : 0.25738}, does_not_raise_exception()),
    ('od550aer', 'ang4487aer', {'merge_how' : 'eval',
                                'merge_eval_fun' : OD450FUN,
                                'var_name_out' : 'od450aer',
                                'var_unit_out' : '1'}, 18,
     {'od550aer' : 0.50155,
      'ang4487aer' : 0.25738,
      'od450aer'  : 0.51902},
     does_not_raise_exception())
    ])
def test_combine_vardata_ungridded_single_ungridded(aeronetsunv3lev2_subset,
                                                    var1, var2,
                                                    add_args, numst,
                                                    mean_first,
                                                    expectation):

    input_data = [(aeronetsunv3lev2_subset, SUN_ID, var1),
                  (aeronetsunv3lev2_subset, SUN_ID, var2)]
    with expectation:
        stats = testmod.combine_vardata_ungridded(input_data, **add_args)

        assert len(stats) == numst
        first = stats[0]
        for var, val in mean_first.items():
            assert var in first
            avg = np.nanmean(first[var])
            npt.assert_allclose(avg, val, rtol=1e-4)


FMFFUN = 'fmf550aer=({};od550lt1aer/{};od550aer)*100'.format(SDA_ID, SUN_ID)

@pytest.mark.parametrize('merge_how,merge_eval_fun,var_name_out,data_id_out,'
                         'var_unit_out,expectation', [
    ('combine',None,None,None,None,does_not_raise_exception()),
    ('eval', FMFFUN, 'fmf550aer', None,'%',does_not_raise_exception()),
    ('eval', FMFFUN, None, 'Bla','%', does_not_raise_exception())

    ])
def test__combine_2_sites_different_vars(
        stats_sun_aod, stats_sda_fineaod, merge_how,
        merge_eval_fun, var_name_out, data_id_out,
        var_unit_out, expectation):
    site_idx1 = stats_sun_aod['station_name'].index(TESTSTAT)
    stat1 = stats_sun_aod['stats'][site_idx1]
    var1 = 'od550aer'

    site_idx2 = stats_sda_fineaod['station_name'].index(TESTSTAT)
    stat2 = stats_sda_fineaod['stats'][site_idx2]
    var2 = 'od550lt1aer'

    prefer='{};{}'.format(SUN_ID, var1)
    with expectation:
        new = testmod._combine_2_sites(stat1, var1, stat2, var2,
                                       merge_how=merge_how,
                                       merge_eval_fun=merge_eval_fun,
                                       match_stats_tol_km=1,
                                       var_name_out=var_name_out,
                                       data_id_out=data_id_out,
                                       var_unit_out=var_unit_out,
                                       resample_how='mean',
                                       apply_time_resampling_constraints=False,
                                       min_num_obs=None,
                                       prefer=prefer,
                                       merge_info_vars={},
                                       add_meta_keys=None)

        assert var1 in new
        assert var2 in new
        assert len(new[var1]) == len(new[var2])
        means_before = [np.nanmean(stat1[var1]), np.nanmean(stat2[var2])]
        means_after = [np.nanmean(new[var1]), np.nanmean(new[var2])]

        npt.assert_allclose(means_after, means_before, rtol=1e-9)
        if merge_how == 'eval':
            if data_id_out is None:
                data_id_out = '{};{}'.format(stat1.data_id, stat2.data_id)
            assert new.data_id == data_id_out

            if var_name_out is None:
                var_name_out = merge_eval_fun
                var_name_out = var_name_out.replace('{};'.format(stat1.data_id), '')
                var_name_out = var_name_out.replace('{};'.format(stat2.data_id), '')
            assert var_name_out in new

            assert new['var_info'][var_name_out]['units'] == var_unit_out


ARGS1 = [(SUN_DATA, SUN_ID, 'od550aer'),
         (SUN_DATA, SUN_ID, 'ang4487aer')]

ARGS_WRONG1 = ARGS1 + ['Bla']
ARGS_WRONG2 = 'Bla'
ARGS_WRONG3 = [(1,2), ARGS1[1]]
ARGS_WRONG4 = [42, ARGS1[0]]
ARGS_WRONG5 = [ARGS1[0], (SDA_DATA, 'Bla', 42)]
ARGS_WRONG6 = [ARGS1[0], (SDA_DATA, 42, 'Bla')]

@pytest.mark.parametrize('args,expectation', [
    (ARGS1, does_not_raise_exception()),
    (ARGS_WRONG1, pytest.raises(NotImplementedError)),
    (ARGS_WRONG2, pytest.raises(ValueError)),
    (ARGS_WRONG3, pytest.raises(ValueError)),
    (ARGS_WRONG4, pytest.raises(ValueError)),
    (ARGS_WRONG5, pytest.raises(ValueError)),
    (ARGS_WRONG6, pytest.raises(ValueError)),
    ])
def test___check_input_data_ids_and_vars(args, expectation):

    with expectation:
        testmod._check_input_data_ids_and_vars(args)


@pytest.mark.parametrize('match_stats_how,match_stats_tol_km', [
    ('station_name', 1),
    ('closest', 0.1),
    ('closest', 1),
    ('closest', 30)
    ])
def test__map_same_stations_samedata(stats_sun_aod, match_stats_how,
                                     match_stats_tol_km):

    (_index_short,
     _index_long,
     _statnames_short,
     _statnames_long) = testmod._map_same_stations(stats_sun_aod,
                                                   stats_sun_aod,
                                                   match_stats_how,
                                                   match_stats_tol_km)
    assert _index_short == _index_long
    assert _statnames_short == _statnames_long

@pytest.mark.parametrize('match_stats_how,match_stats_tol_km,num_matches,diff_idx', [
    ('station_name', 1, 13, 5),
    ('closest', 0.1, 13, 5),
    ('closest', 1, 13, 5),
    ('closest', 30, 13, 5)
    ])
def test__map_same_stations(stats_sun_aod, stats_sda_aod,
                            match_stats_how, match_stats_tol_km,
                            num_matches, diff_idx):

    (_index_short,
     _index_long,
     _statnames_short,
     _statnames_long) = testmod._map_same_stations(stats_sun_aod,
                                                   stats_sda_aod,
                                                   match_stats_how,
                                                   match_stats_tol_km)
    assert len(_index_short) == num_matches
    _diff_idx = np.sum(np.asarray(_index_short) - np.asarray(_index_long))
    assert _diff_idx == diff_idx


aodexpensive = 'od550aer=({};od550aer+{};od550aer)/2'.format(SUN_ID,SUN_ID)

@pytest.mark.parametrize('merge_how,merge_eval_fun,var_name_out,data_id_out,'
                         'var_unit_out', [
    ('combine',None,None,None,None),
    ('mean',None,None,None,None),
    ('eval',aodexpensive,'Bla','Blub','1')

    ])
def test__combine_2_sites_same_site(stats_sun_aod, merge_how, merge_eval_fun,
                                    var_name_out, data_id_out, var_unit_out):
    site_idx = stats_sun_aod['station_name'].index(TESTSTAT)
    stat1 = stat2 = stats_sun_aod['stats'][site_idx]
    var1 = var2 = 'od550aer'
    prefer='{};{}'.format(SUN_ID, var1)
    unit = stat1.get_unit(var1)

    new = testmod._combine_2_sites(stat1, var1, stat2, var2,
                                   merge_how=merge_how,
                                   merge_eval_fun=merge_eval_fun,
                                   match_stats_tol_km=1,
                                   var_name_out=var_name_out,
                                   data_id_out=data_id_out,
                                   var_unit_out=var_unit_out,
                                   resample_how='mean',
                                   apply_time_resampling_constraints=False,
                                   min_num_obs=None,
                                   prefer=prefer,
                                   merge_info_vars={},
                                   add_meta_keys=None)

    vno = var1 if var_name_out is None else var_name_out
    dataid = SUN_ID if data_id_out is None else data_id_out
    unitout = unit if var_unit_out is None else var_unit_out


    assert new.get_var_ts_type(vno) == stat1.get_var_ts_type(var1)
    assert vno in new and vno in new.var_info
    assert new.data_id == dataid
    assert len(stat1[var1].dropna()) == len(new[vno])
    assert new.get_unit(vno) == unitout


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)