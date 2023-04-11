from __future__ import annotations

from itertools import chain
from pathlib import Path

import pytest
import simplejson

from pyaerocom.io.ebas_file_index import EbasFileIndex
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.io.read_ebas import ReadEbas

from .data_access import DataForTests

EBAS_FILEDIR = DataForTests("obsdata/EBASMultiColumn/data").path
ebas_info_file = DataForTests("scripts/ebas_files.json").path
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
    # sc550dryaer Jungfraujoch - only first file
    "Jungfraujoch": EBAS_FILES["sc550dryaer"]["Jungfraujoch"][0],
}


@pytest.fixture
def ebas_issue_files(issue_files: str) -> Path:
    """file path for `EBAS_ISSUE_FILES[issue_files]`"""
    return EBAS_FILEDIR / EBAS_ISSUE_FILES[issue_files]


def get_ebas_filelist(var_name: str) -> list[Path]:
    """all file paths for `var_name`"""
    paths: list[Path] = [
        EBAS_FILEDIR / file for files in EBAS_FILES[var_name].values() for file in files
    ]
    assert all(path.exists() for path in paths)
    return paths


@pytest.fixture
def ebas_files(file_vars: list[str] | str | None) -> list[Path] | None:
    if file_vars is None:
        return None
    if isinstance(file_vars, str):
        return get_ebas_filelist(file_vars)

    paths = (get_ebas_filelist(var_name) for var_name in file_vars)
    return list(chain.from_iterable(paths))


@pytest.fixture(scope="module")
def ebas() -> EbasFileIndex:
    """ebas file index for test DB"""
    EBAS_SQLite_DB = EBAS_FILEDIR.parent / "ebas_file_index.sqlite3"
    assert EBAS_SQLite_DB.exists()
    return EbasFileIndex(EBAS_SQLite_DB)


@pytest.fixture(scope="session")
def data_scat_jungfraujoch():
    """subset of sc550aer obs from Jungfraujoch"""
    reader = ReadEbas("EBASSubset")
    return reader.read("sc550aer", station_names="Jungfrau*")


@pytest.fixture(scope="session")
def data_scat_jungfraujoch_full():
    """all sc550aer obs from Jungfraujoch"""
    reader = ReadEbas()
    return reader.read("sc550aer", station_names="Jungfrau*")


@pytest.fixture(scope="session")
def loaded_nasa_ames_example() -> EbasNasaAmesFile:
    """loaded sc550dryaer Jungfraujoch file"""
    path = EBAS_FILEDIR / EBAS_ISSUE_FILES["Jungfraujoch"]
    assert path.exists()
    return EbasNasaAmesFile(path)
