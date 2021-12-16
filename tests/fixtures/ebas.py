import pytest
import simplejson

from pyaerocom.access_testdata import AccessTestData
from pyaerocom.io.ebas_file_index import EbasFileIndex
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.io.read_ebas import ReadEbas

TESTDATADIR = AccessTestData().testdatadir


EBAS_FILEDIR = TESTDATADIR / "obsdata/EBASMultiColumn/data"

ebas_info_file = TESTDATADIR / "scripts/ebas_files.json"
assert ebas_info_file.exists()
EBAS_FILES = simplejson.loads(ebas_info_file.read_text())
for sites in EBAS_FILES.values():
    for files in sites.values():
        for file in files:
            assert (EBAS_FILEDIR / file).exists()

EBAS_ISSUE_FILES = {
    # conco3 tower - 3 different measurement heights
    "o3_tower": "CZ0003R.20150101000000.20181107114213.uv_abs.ozone.air.1y.1h..CZ06L_uv_abs.lev2.nas",
    # conco3 - Neg. meas periods
    "o3_neg_dt": "NZ0003G.20090110030000.20181130115605.uv_abs.ozone.air.9h.1h.US06L_Thermo_49C_LAU.US06L_AM.lev2.nas",
    # conco3 - Most common meas period is 150s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    "o3_tstype": "LT0015R.20080101000000.20081231000000.uv_abs.ozone.air.15d.1h.LT01L_uv_abs_15.LT01L_uv_abs..nas",
    # concpm10 - could not resolve unique data column for concpm10 (EBAS varname: ['pm10_mass'])
    "pm10_colsel": "ID1013R.20180101000000.20200102000000.beta_gauge_particulate_sampler.pm10_mass.pm10.1y.1h.ID01L_MetOne_BAM1020..lev2.nas",
    # concpm10 Aliartos - Most common meas period is 172800s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    "pm10_tstype": "GR0001R.20060119000000.20080120000000.b-attenuation.pm10_mass.pm10.11mo.1w.GR01L_b_att_01.GR01L_b-attenuation..nas",
}


@pytest.fixture(scope="module")
def ebas() -> EbasFileIndex:

    EBAS_SQLite_DB = EBAS_FILEDIR.parent / "ebas_file_index.sqlite3"
    assert EBAS_SQLite_DB.exists()
    return EbasFileIndex(EBAS_SQLite_DB)


@pytest.fixture(scope="session")
def data_scat_jungfraujoch():
    reader = ReadEbas("EBASSubset")
    return reader.read("sc550aer", station_names="Jungfrau*")


@pytest.fixture(scope="session")
def data_scat_jungfraujoch_full():
    reader = ReadEbas()
    return reader.read("sc550aer", station_names="Jungfrau*")


@pytest.fixture(scope="session")
def loaded_nasa_ames_example() -> EbasNasaAmesFile:

    fname = EBAS_FILES["sc550dryaer"]["Jungfraujoch"][0]
    path = TESTDATADIR / f"obsdata/EBASMultiColumn/data/{fname}"
    return EbasNasaAmesFile(path)
