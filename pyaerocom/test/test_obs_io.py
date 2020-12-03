#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:13:58 2020

@author: jonasg
"""

import pytest
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom import obs_io as testmod

AuxInfoUngriddedTypes = dict(
    data_id = str,
    vars_supported = list,
    aux_merge_how = dict,
    aux_requires = dict,
    aux_funs = dict,
    aux_units = dict)

AUX_EXAMPLE = dict(
        data_id='AERONET',
        vars_supported=['fmf550aer', 'od550lt1aer'],
        aux_merge_how={
            'fmf550aer' : 'eval',
            'od550lt1aer' : 'combine'},
        aux_requires = {
            'fmf550aer' : {
                'AeronetSDAV3Lev2.daily' : 'od550lt1aer',
                'AeronetSunV3Lev2.daily' : 'od550aer'
                },
            'od550lt1aer' : {
                'AeronetSDAV3Lev2.daily' : 'od550lt1aer',
                'AeronetSunV3Lev2.daily' : 'od550aer'
                }},
        aux_funs = {
            'fmf550aer' :
                '(AeronetSDAV3Lev2.daily;od550lt1aer/AeronetSunV3Lev2.daily;od550aer)*100'
        },
        aux_units = {'fmf550aer' : '%'}
    )
def test_OBS_WAVELENGTH_TOL_NM():
    assert testmod.OBS_WAVELENGTH_TOL_NM == 10.0

def test_OBS_ALLOW_ALT_WAVELENGTHS():
    assert testmod.OBS_ALLOW_ALT_WAVELENGTHS == True

def test_ObsVarCombi():
    assert str(testmod.ObsVarCombi('bla', 'blub')) == 'bla;blub'

def test_AuxInfoUngridded_MAX_VARS_PER_METHOD():
    assert testmod.AuxInfoUngridded.MAX_VARS_PER_METHOD == 2

def test_AuxInfoUngridded_to_dict():
    info = testmod.AuxInfoUngridded(**AUX_EXAMPLE)
    assert info.to_dict() == AUX_EXAMPLE

from copy import deepcopy
EX_WRONG1 = deepcopy(AUX_EXAMPLE)
EX_WRONG1['aux_funs'] = None

EX_WRONG2 = deepcopy(AUX_EXAMPLE)
EX_WRONG2['vars_supported'] = dict(a=1)

EX_WRONG3 = deepcopy(AUX_EXAMPLE)
EX_WRONG3['vars_supported'].append('blablub')

EX_WRONG3p5 = deepcopy(EX_WRONG3)
EX_WRONG3p5['aux_merge_how']['blablub'] = 'eval'

EX_WRONG4 = deepcopy(EX_WRONG3p5)
EX_WRONG4['aux_requires']['blablub'] = 42

EX_WRONG5 = deepcopy(EX_WRONG4)
EX_WRONG5['aux_requires']['blablub'] = {'abc' : '42'}

EX_WRONG6 = deepcopy(EX_WRONG5)
EX_WRONG6['aux_requires']['blablub']['def'] = '43'

EX_NOTWRONG1 = deepcopy(EX_WRONG6)
EX_NOTWRONG1['aux_funs']['blablub'] = 'abc;42+def;43'

EX_NOTWRONG2 = deepcopy(EX_NOTWRONG1)
EX_NOTWRONG2['aux_units']['blablub'] = '1'

@pytest.mark.parametrize('argdict,expectation', [
    (AUX_EXAMPLE, does_not_raise_exception()),
    (EX_WRONG1, pytest.raises(ValueError)),
    (EX_WRONG2, pytest.raises(ValueError)),
    (EX_WRONG3, pytest.raises(ValueError)),
    (EX_WRONG3p5, pytest.raises(ValueError)),
    (EX_WRONG4, pytest.raises(ValueError)),
    (EX_WRONG5, pytest.raises(ValueError)),
    (EX_WRONG6, pytest.raises(ValueError)),
    (EX_NOTWRONG1, does_not_raise_exception()),
    (EX_NOTWRONG2, does_not_raise_exception())
    ])
def test_AuxInfoUngridded___init__(argdict, expectation):
    with expectation:
        info = testmod.AuxInfoUngridded(**argdict)
        for key, dtype in AuxInfoUngriddedTypes.items():
            assert isinstance(info.__dict__[key], dtype)

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)