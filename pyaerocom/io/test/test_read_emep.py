import pytest
from pyaerocom.conftest import lustre_unavail
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.griddeddata import GriddedData

def test_read_emep():
    r = ReadEMEP()
    assert r.data_id == None
    assert r.vars_provided == None
    assert self.filepath == None

@lustre_unavail
def test_read_emep_data():
    path = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_AerocomHIST/2010_GLOB1_2010met/Base_month.nc'

    r = ReadEMEP()

    r.filepath = path
    vars_provided = r.vars_provided
    assert isinstance(vars_provided, list)

    data = r.read_var('dryso4', ts_type='monthly')
    assert isinstance(data, GriddedData)
