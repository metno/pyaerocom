#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:28:03 2020

@author: jonasg
"""
import pytest
import numpy as np
from collections import OrderedDict
from pyaerocom.conftest import (does_not_raise_exception, EBAS_FILEDIR,
                                EBAS_FILES, loaded_nasa_ames_example)
from pyaerocom.conftest import loaded_nasa_ames_example as filedata

from pyaerocom.io import ebas_nasa_ames as ena

@pytest.fixture(scope='module')
def head():
    return ena.NasaAmesHeader

@pytest.mark.parametrize('raw_data,raises,valid', [
    (np.asarray([0]), does_not_raise_exception(), np.asarray([True])),
    (np.asarray([0.66]), does_not_raise_exception(), np.asarray([True])),
    (np.asarray([0.456]), does_not_raise_exception(), np.asarray([False])),
    (np.asarray([0.999]), does_not_raise_exception(), np.asarray([False])),
    (np.asarray([0.999100]), does_not_raise_exception(), np.asarray([True])),
    (np.asarray([0.999100456]), does_not_raise_exception(), np.asarray([True])),
    ])
def test_EbasFlagCol(raw_data,raises,valid):
    with raises:
        fc = ena.EbasFlagCol(raw_data)
        assert fc.valid == valid

@pytest.mark.parametrize('raw_data,decoded', [
    (np.asarray([0]), np.asarray([[0, 0, 0]])),
    (np.asarray([0.10045666]), np.asarray([[100, 456, 660]])),
    (np.asarray([0.10045666, 0]), np.asarray([[100, 456, 660],[0, 0, 0]])),
    (np.asarray([0.10045666, 0.12]), np.asarray([[100, 456, 660],[120, 0, 0]])),
    (np.asarray([0.10045666, 0.1234]), np.asarray([[100, 456, 660],[123, 400, 0]])),
    ])
def test_EbasFlagCol_decoded(raw_data, decoded):
    fc = ena.EbasFlagCol(raw_data, False)
    assert fc._decoded is None
    dc = fc.decoded
    assert fc._decoded is dc
    assert decoded.ndim == 2
    assert (dc == decoded).all()

def test_NasaAmesHeader_NUM_FIXLINES(head):
    assert head._NUM_FIXLINES == 13

def test_NasaAmesHeader_CONV_STR(head):
    assert head.CONV_STR('bla ') == 'bla'

def test_NasaAmesHeader_CONV_PI(head):
    assert head.CONV_PI('bla;blub') == 'bla; blub'

def test_EbasNasaAmesFile_instance(filedata):
    assert isinstance(filedata, ena.NasaAmesHeader)
    assert isinstance(filedata, ena.EbasNasaAmesFile)

HEAD_FIX = OrderedDict([
    ('num_head_lines', 93), ('num_head_fmt', 1001),
    ('data_originator', 'Brem, Benjamin; Baltensperger, Urs'),
    ('sponsor_organisation', 'CH02L, Paul Scherrer Institut, PSI, Laboratory of Atmospheric Chemistry (LAC), OFLB, , 5232, Villigen PSI, Switzerland'),
    ('submitter', 'Brem, Benjamin'),
    ('project_association', 'ACTRIS CREATE EMEP GAW-WDCA'),
    ('vol_num', 1), ('vol_totnum', 1),
    ('ref_date', np.datetime64('2019-01-01T00:00:00')),
    ('revision_date', np.datetime64('2020-05-26T00:00:00')),
    ('freq', 0.041667),
    ('descr_time_unit', 'days from file reference point'),
    ('num_cols_dependent', 23),
    ('mul_factors', [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),
    ('vals_invalid', [999.999999, 9999.99, 999.99, 9999.99, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 99.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 999.99999999, 9.999999]),
    ('descr_first_col', 'end_time of measurement, days from the file reference point')])

def test_EbasNasaAmesFile_head_fix(filedata):
    assert isinstance(filedata.head_fix, OrderedDict)
    for key, val in filedata.head_fix.items():
        assert key in HEAD_FIX
        assert val == HEAD_FIX[key]

    with pytest.raises(AttributeError):
        filedata.head_fix = 'Blaaaaaaaaaaaaaaa'

def test_EbasNasaAmesFile_data(filedata):
    assert isinstance(filedata.data, np.ndarray)
    assert filedata.data.ndim == 2

def test_EbasNasaAmesFile_shape(filedata):
    assert filedata.shape == (8760, 24)

def test_EbasNasaAmesFile_col_num(filedata):
    assert filedata.col_num == 24

def test_EbasNasaAmesFile_col_names(filedata):
    names = filedata.col_names
    assert names == ['starttime', 'endtime', 'pressure', 'relative_humidity',
                     'temperature', 'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_backscattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'aerosol_light_scattering_coefficient',
                     'numflag']


def test_EbasNasaAmesFile_get_time_gaps_meas(filedata):
    gaps = filedata.get_time_gaps_meas()
    assert len(gaps) == 8759
    assert np.unique(gaps).sum() == 0

def test_EbasNasaAmesFile_get_dt_meas(filedata):
    dt = filedata.get_dt_meas()
    assert len(dt) == 8759
    assert list(np.unique(dt)) == [3599.0, 3600.0, 3601.0]

@pytest.mark.parametrize('update', [
    {'bla' : 42}, {'vol_num': 42}
    ])
def test_EbasNasaAmesFile_update(filedata, update):
    meta_before = {}
    meta_before.update(**filedata._meta)
    head_before = {}
    head_before.update(**filedata._head_fix)
    filedata.update(**update)
    for key, val in update.items():
        if key in head_before:
            assert filedata._head_fix[key] == val
        else:
            assert filedata._meta[key] == val
    filedata._head_fix = head_before
    filedata._meta = meta_before

def test_EbasNasaAmesFile___str__(filedata):
    assert isinstance(filedata.__str__(), str)

@pytest.mark.parametrize('colnum,raises,value', [
    (0, pytest.raises(KeyError), None),
    (5, does_not_raise_exception(), 450),
    (8, does_not_raise_exception(), 550),
    ])
def test_EbasColDef_get_wavelength_nm(filedata, colnum, raises, value):
    coldef = filedata.var_defs[colnum]
    assert isinstance(coldef, ena.EbasColDef)
    with raises:
        assert coldef.get_wavelength_nm() == value

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
