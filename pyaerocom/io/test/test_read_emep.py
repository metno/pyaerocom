import pytest
from pyaerocom.conftest import lustre_unavail, testdata_unavail
from pyaerocom.io.read_emep import ReadEMEP
from pyaerocom.griddeddata import GriddedData

def test_read_emep():
    r = ReadEMEP()
    assert r.data_id == None
    assert r.vars_provided == None
    assert r.filepath == None

@lustre_unavail
def test_read_emep_data():
    path = '/lustre/storeB/project/fou/kl/emep/ModelRuns/2020_AerocomHIST/2010_GLOB1_2010met/Base_month.nc'

    r = ReadEMEP()

    r.filepath = path
    vars_provided = r.vars_provided
    assert isinstance(vars_provided, list)

    data = r.read_var('dryso4', ts_type='monthly')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'

    # Read auxilliary variable
    # TODO: run these two similiar tests parameterized
    data = r.read_var('depso4', ts_type='monthly')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'
    assert data.metadata['computed'] == True

    data = r.read_var('od550aer', ts_type='monthly')
    assert data.units == '1'

@lustre_unavail
@testdata_unavail
def test_read_emep_colocate():
    pass

def test_preprocess_units():
    units = ''
    assert ReadEMEP().preprocess_units(units) == '1'

    units = 'mgS/m2'
    catch_error = False
    try:
        ReadEMEP().preprocess_units(units)
    except NotImplementedError as e:
        catch_error = True
    assert catch_error == True
