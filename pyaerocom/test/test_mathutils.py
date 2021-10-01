#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for _lowlevel_helpers.py module of pyaerocom
"""
import pytest
import numpy as np
import numpy.testing as npt
from pyaerocom.conftest import does_not_raise_exception
import pyaerocom.mathutils as mu

@pytest.mark.parametrize('inputval, desired', [
    (0.01, -2), (4, 0), (234, 2)
    ])
def test_exponent(inputval, desired):
    """Test method :func:`exponent` of :mod:`pyaerocom.utils`"""
    assert mu.exponent(inputval) == desired

@pytest.mark.parametrize('inputval, p, T, vmr_unit, mmol_var, mmol_air, to_unit, desired', [
    (1, 101300,293,'nmol mol-1',48,None,'ug m-3', 1.9959),
    (1, 101300,273,'nmol mol-1',48,None,'ug m-3', 2.1421),
    (1, 101300,273,'nmol mol-1',48,None,'kg m-3', 2.1421e-9),
    (1, 101300,273,'mol mol-1',48,None,'kg m-3', 2.1421),
    (1, 98000,273,'mol mol-1',48,None,'kg m-3', 2.0724),
    ])
def test_vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var,
                       mmol_air, to_unit, desired):
    val = mu.vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var, mmol_air,
                           to_unit)
    npt.assert_allclose(val, desired, rtol=1e-4)

@pytest.mark.parametrize('data,expected', [
    ([1], (1,0)), (np.asarray([1]), (1,0)),
    ([1, np.nan], (1,0)), ([np.nan, np.nan], (np.nan, np.nan)),
    (np.random.normal(loc=3, scale=0.01,size=100000), (3,0.01)),
    ([1, np.nan,0,2], (1,0.816497))
    ])
def test__nanmean_and_std(data,expected):
    mean, std = mu._nanmean_and_std(data)
    mean_, std_ = expected
    if np.isnan(mean_):
        assert np.isnan(mean)
    else:
        npt.assert_allclose(mean,mean_,atol=0.001,rtol=1e-2)
    if np.isnan(std_):
        assert np.isnan(std)
    else:
        npt.assert_allclose(std,std_,atol=0.001,rtol=1e-2)

perfect_stats_num1_mean1 = {'totnum': 1.0, 'num_valid': 1.0, 'refdata_mean': 1.0,
                       'refdata_std': 0.0, 'data_mean': 1.0, 'data_std': 0.0,
                       'weighted': False, 'rms': 0.0, 'nmb': 0.0,
                       'mnmb': 0.0, 'fge': 0.0, 'R': np.nan,
                       'R_kendall' : np.nan, 'R_spearman' : np.nan}
perfect_stats_num2_mean1 = {}
perfect_stats_num2_mean1.update(perfect_stats_num1_mean1)
perfect_stats_num2_mean1['totnum'] =2

num_fakedata = 1000
idx = np.linspace(0,2*np.pi,num_fakedata)
zero_signal = np.zeros(num_fakedata)
sin_signal = np.sin(idx)
cos_signal = np.cos(idx)
noise = np.random.normal(loc=0, scale=0.01,size=num_fakedata)
nanmask = np.ones(num_fakedata)
nanmask[100:300] = np.nan

@pytest.mark.parametrize('data, ref_data, lowlim, highlim, min_num_valid, weights, expected,raises', [
    (zero_signal,zero_signal,None,None,1,None,{
        'totnum': 1000.0,
         'num_valid': 1000.0,
         'refdata_mean': 0.0,
         'refdata_std': 0,
         'data_mean': 0.0,
         'data_std': 0,
         'weighted': False,
         'rms': 0.0,
         'R': np.nan,
         'R_spearman': np.nan,
         'R_kendall': np.nan,
         'nmb': 0,
         'mnmb': np.nan,
         'fge': np.nan
         }, does_not_raise_exception()),
    (zero_signal,noise,None,None,1,None,{
        'totnum': 1000.0,
         'num_valid': 1000.0,
         'refdata_mean': 0.0,
         'refdata_std': 0,
         'data_mean': 0.0,
         'data_std': 0,
         'weighted': False,
         'rms': 0.0,
         'R': np.nan,
         'R_spearman': np.nan,
         'R_kendall': np.nan,
         'nmb': -1,
         'mnmb': -2,
         'fge': 2
         }, does_not_raise_exception()),
    ([1],[1],None,None,1,None,perfect_stats_num1_mean1, does_not_raise_exception()),
    ([1],[1, np.nan],None,None,1,None,perfect_stats_num1_mean1, pytest.raises(IndexError)),
    ([1, np.nan],[1, np.nan],None,None,1,None,perfect_stats_num2_mean1, does_not_raise_exception()),
    (sin_signal,sin_signal,None,None,1,None, {
        'totnum': 1000.0,
         'num_valid': 1000.0,
         'refdata_mean': 0.0,
         'refdata_std': 0.71,
         'data_mean': 0.0,
         'data_std': 0.71,
         'weighted': False,
         'rms': 0.0,
         'R': 1.0,
         'R_spearman': 1.0,
         'R_kendall': 1.0,
         'nmb': 0,
         'mnmb': np.nan,
         'fge': np.nan
         },
     does_not_raise_exception()),

    ])
def test_calc_statistics(data, ref_data, lowlim, highlim, min_num_valid,
                         weights, expected, raises):
    with raises:
        stats = mu.calc_statistics(data, ref_data, lowlim, highlim, min_num_valid,
                                   weights)
        assert isinstance(stats, dict)
        assert len(stats) == len(expected)
        for key, val in expected.items():
            assert key in stats
            if isinstance(val, str):
                assert stats[key] == val
            else:
                npt.assert_allclose(stats[key], val, atol=0.02, rtol=0.01)


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
# =============================================================================
#
#     import matplotlib.pyplot as plt
#
#     plt.close('all')
#     fig, ax = plt.subplots(1,1,figsize=(18,10))
#     ax.plot(sin_signal, '--', label='sin')
#     ax.plot(sin_signal+noise, '--', label='sin+noise')
#
#     ax.legend()
#
#
# =============================================================================
