#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level I/O utility methods for pyaerocom
"""
import pytest

from pyaerocom.conftest import lustre_unavail
from pyaerocom.io import utils
from pyaerocom.io.read_ebas import ReadEbas
from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3

def name(obj):
    return obj.__name__

TESTDATA = [
    ('EBASMC', ReadEbas),
    ('AeronetSunV3Lev2.daily', ReadAeronetSunV3),
    ('AeronetSDAV3Lev2.daily', ReadAeronetSdaV3),
    ('AeronetInvV3Lev2.daily', ReadAeronetInvV3),
    ('GAWTADsubsetAasEtAl', ReadAasEtal)
]
@pytest.mark.parametrize(('obs_id,reader'), TESTDATA)
def test_get_ungridded_reader(obs_id, reader):
    assert name(utils.get_ungridded_reader(obs_id)) == name(reader)

@lustre_unavail
def test_browse_database():
    assert 'TM5-met2010_AP3-CTRL2019' in utils.browse_database('*TM5*CTRL*')

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
