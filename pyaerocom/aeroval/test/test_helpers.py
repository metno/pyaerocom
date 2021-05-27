#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:13:05 2020

@author: jonasg
"""
import pytest

from pyaerocom.aeroval import obsentry as h
from pyaerocom.conftest import does_not_raise_exception

@pytest.mark.parametrize('input_args,expectation', [
    pytest.param(dict(), pytest.raises(ValueError)),
    # the following input for obs_vars is converted into a
    # list in the setup class
    pytest.param(dict(obs_id='Bla',
                      obs_vars='od550aer',
                      obs_vert_type='Column'), does_not_raise_exception()),
    pytest.param(dict(obs_id='Bla',
                      obs_vars='od550aer',
                      obs_vert_type='Slant-Column'), pytest.raises(ValueError)),

    ])
def test_ObsEntry(input_args,expectation):
    with expectation:
        cfg = h.ObsEntry(**input_args)
        for key, val in input_args.items():
            if key=='obs_vars' and isinstance(val, str):
                val = [val]
            assert cfg[key] == val

def test_ObsEntry_keys():
    cfg = h.ObsEntry(obs_id='Bla', obs_vars='Blub', obs_vert_type='Column')
    keys = ['obs_id', 'obs_type', 'obs_vars', 'obs_ts_type_read',
            'obs_vert_type', 'obs_aux_requires', 'instr_vert_loc',
            'is_superobs', 'only_superobs', 'read_opts_ungridded']
    assert len(keys) == len(cfg)
    assert [x in cfg for x in keys]

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
