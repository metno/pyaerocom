from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Type

import cf_units
import numpy as np
import pytest
import xarray as xr

import pyaerocom.exceptions as exc
from pyaerocom import get_variable
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.read_mscw_ctm import ReadEMEP, ReadMscwCtm

from .._conftest_helpers import _create_fake_MSCWCtm_data
from ..conftest import EMEP_DIR, data_unavail

VAR_MAP = {
    "abs550aer": "AAOD_550nm",
    "abs550bc": "AAOD_EC_550nm",
    "absc550aer": "AbsCoeff",
    "absc550dryaer": "AbsCoeff",
    "ac550aer": "AbsCoef_surf",
    "drybc": "DDEP_EC_m2Grid",
    "drydust": "DDEP_DUST_m2Grid",
    "drynh4": "DDEP_NH4_f_m2Grid",
    "dryno3": "DDEP_TNO3_m2Grid",
    "dryoa": "DDEP_OM25_m2Grid",
    "dryso2": "DDEP_SO2_m2Grid",
    "dryso4": "DDEP_SO4_m2Grid",
    "dryss": "DDEP_SS_m2Grid",
    "ec550aer": "EXT_550nm",
    "ec550dryaer": "EXTdry_550nm",
    "emidust": "DUST_flux",
    "emisnox": "Emis_mgm2_nox",
    "emisox": "Emis_mgm2_sox",
    "loadbc": "COLUMN_EC_kmax",
    "loaddust": "COLUMN_DUST_kmax",
    "loadnh4": "COLUMN_NH4_F_kmax",
    "loadno3": "COLUMN_TNO3_kmax",
    "loadoa": "COLUMN_OM25_kmax",
    "loadso2": "COLUMN_SO2_kmax",
    "loadso4": "COLUMN_SO4_kmax",
    "loadss": "COLUMN_SS_kmax",
    "mmrbc": "D3_mmr_EC",
    "mmrdust": "D3_mmr_DUST",
    "mmrnh4": "D3_mmr_NH4_F",
    "mmrno3": "D3_mmr_TNO3",
    "mmroa": "D3_mmr_OM25",
    "mmrso2": "D3_mmr_SO2",
    "mmrso4": "D3_mmr_SO4",
    "mmrss": "D3_mmr_SS",
    "od350aer": "AOD_350nm",
    "od440aer": "AOD_440nm",
    "od550aer": "AOD_550nm",
    "od550bc": "AOD_EC_550nm",
    "od550dust": "AOD_DUST_550nm",
    "od550lt1aer": "AOD_PMFINE_550nm",
    "od550nh4": "AOD_NH4_F_550nm",
    "od550no3": "AOD_TNO3_550nm",
    "od550oa": "AOD_OC_550nm",
    "od550so4": "AOD_SO4_550nm",
    "od550ss": "AOD_SS_550nm",
    "od870aer": "AOD_870nm",
    "concaeroh2o": "SURF_PM25water",
    "concbcc": "SURF_ug_ECCOARSE",
    "concbcf": "SURF_ug_ECFINE",
    "concdust": "SURF_ug_DUST",
    "conchno3": "SURF_ug_HNO3",
    "concnh3": "SURF_ug_NH3",
    "concnh4": "SURF_ug_NH4_F",
    "concno2": "SURF_ug_NO2",
    "concno3c": "SURF_ug_NO3_C",
    "concno3f": "SURF_ug_NO3_F",
    "concno": "SURF_ug_NO",
    "conco3": "SURF_ug_O3",
    "concoac": "SURF_ug_PM_OMCOARSE",
    "concoaf": "SURF_ug_PM_OM25",
    "concpm10": "SURF_ug_PM10_rh50",
    "concpm25": "SURF_ug_PM25_rh50",
    "concrdn": "SURF_ugN_RDN",
    "concso2": "SURF_ug_SO2",
    "concso4": "SURF_ug_SO4",
    "concss": "SURF_ug_SS",
    "concssf": "SURF_ug_SEASALT_F",
    "concCocpm25": "SURF_ugC_PM_OM25",
    "vmro32m": "SURF_2MO3",
    "vmro3max": "SURF_MAXO3",
    "vmro3": "SURF_ppb_O3",
    "vmrco": "SURF_ppb_CO",
    "vmrc2h6": "SURF_ppb_C2H6",
    "vmrc2h4": "SURF_ppb_C2H4",
    "vmrhcho": "SURF_ppb_HCHO",
    "vmrglyoxal": "SURF_ppb_GLYOX",
    "vmrisop": "SURF_ppb_C5H8",
    "wetbc": "WDEP_EC",
    "wetdust": "WDEP_DUST",
    "wetnh4": "WDEP_NH4_f",
    "wetno3": "WDEP_TNO3",
    "wetoa": "WDEP_OM25",
    "wetoxn": "WDEP_OXN",
    "wetrdn": "WDEP_RDN",
    "wetso2": "WDEP_SO2",
    "wetso4": "WDEP_SO4",
    "wetoxs": "WDEP_SOX",
    "wetss": "WDEP_SS",
    "z3d": "Z_MID",
    "prmm": "WDEP_PREC",
    "concecpm25": "SURF_ug_ECFINE",
    "concssc": "SURF_ug_SEASALT_C",
    "dryoxn": "DDEP_OXN_m2Grid",
    "dryoxs": "DDEP_SOX_m2Grid",
    "dryrdn": "DDEP_RDN_m2Grid",
}


@pytest.fixture(scope="module")
def reader():
    return ReadMscwCtm()


def test_ReadMscwCtm__init__():
    reader = ReadMscwCtm("EMEP_2017", EMEP_DIR)
    assert getattr(reader, "data_id") == "EMEP_2017"
    assert getattr(reader, "data_dir") == EMEP_DIR


def test_ReadMscwCtm__init___error():
    data_dir = "not_a_real_path"
    with pytest.raises(FileNotFoundError) as e:
        ReadMscwCtm(None, data_dir)
    assert str(e.value) == data_dir


def test_ReadMscwCtm_data_dir():
    reader = ReadMscwCtm(EMEP_DIR)
    reader.data_dir = EMEP_DIR
    assert Path(reader.data_dir) == Path(EMEP_DIR)


@pytest.mark.parametrize(
    "value,exception,error",
    [
        (None, ValueError, "Data dir None needs to be a dictionary or a file"),
        ("not_a_real_path", FileNotFoundError, "not_a_real_path"),
    ],
)
def test_ReadMscwCtm_data_dir_error(value, exception, error: str):
    reader = ReadMscwCtm(value)
    with pytest.raises(exception) as e:
        reader.data_dir = value
    assert str(e.value) == error


def test__ReadMscwCtm__check_files_in_data_dir():
    reader = ReadMscwCtm()
    value = EMEP_DIR
    mask, matches = reader._check_files_in_data_dir(value)
    assert mask == "Base_*.nc"
    assert len(matches) == 3


def test__ReadMscwCtm__check_files_in_data_dir_error():
    reader = ReadMscwCtm()
    with pytest.raises(FileNotFoundError):
        reader._check_files_in_data_dir("/tmp")


def test_ReadMscwCtm_ts_type():
    reader = ReadMscwCtm()
    assert reader.ts_type == "daily"


def test_ReadMscwCtm_var_map():
    var_map = ReadMscwCtm().var_map
    assert isinstance(var_map, dict)
    assert var_map == VAR_MAP


@data_unavail
@pytest.mark.parametrize(
    "var_name, ts_type", [("vmro3", "daily"), ("vmro3", None), ("concpmgt25", "daily")]
)
def test_ReadMscwCtm_read_var(var_name: str, ts_type: str):
    reader = ReadMscwCtm(data_dir=EMEP_DIR)
    data = reader.read_var(var_name, ts_type)
    assert isinstance(data, GriddedData)
    if ts_type is not None:
        assert data.ts_type == ts_type
    assert data.ts_type is not None
    assert data.ts_type == reader.ts_type


@data_unavail
@pytest.mark.parametrize(
    "var_name, ts_type, exception, error",
    [
        (
            "blaaa",
            "daily",
            exc.VariableDefinitionError,
            "Error (VarCollection): input variable blaaa is not supported",
        ),
        ("od550gt1aer", "daily", exc.VarNotAvailableError, "od550gt1aer"),
    ],
)
def test_ReadMscwCtm_read_var_error(
    var_name: str, ts_type: str, exception: Type[Exception], error: str
):
    reader = ReadMscwCtm(data_dir=EMEP_DIR)
    with pytest.raises(exception) as e:
        reader.read_var(var_name, ts_type)
    assert str(e.value) == error


@data_unavail
@pytest.mark.parametrize(
    "var_name, ts_type",
    [
        ("concpmgt25", "daily"),
        ("concpmgt25", "monthly"),
    ],
)
def test_ReadMscwCtm__compute_var(var_name, ts_type):
    reader = ReadMscwCtm(data_dir=EMEP_DIR)
    data = reader._compute_var(var_name, ts_type)
    assert isinstance(data, xr.DataArray)


@data_unavail
def test_ReadMscwCtm__compute_var_error():
    reader = ReadMscwCtm(data_dir=EMEP_DIR)
    with pytest.raises(KeyError):
        reader._compute_var("blaaa", "daily")


@data_unavail
def test_ReadMscwCtm_data(path_emep):
    path = EMEP_DIR
    reader = ReadMscwCtm(data_dir=path)

    vars_provided = reader.vars_provided
    assert isinstance(vars_provided, list)
    assert "vmro3" in vars_provided

    data = reader.read_var("vmro3", ts_type="daily")
    assert isinstance(data, GriddedData)
    assert data.time.long_name == "time"
    assert data.time.standard_name == "time"
    assert data.ts_type == "daily"

    data = reader.read_var("vmro3")
    assert isinstance(data, GriddedData)
    assert data.time.long_name == "time"
    assert data.time.standard_name == "time"
    assert data.ts_type == "daily"


@data_unavail
def test_ReadMscwCtm_directory(path_emep):
    data_dir = EMEP_DIR
    reader = ReadMscwCtm(data_dir=data_dir)
    assert reader.data_dir == data_dir
    vars_provided = reader.vars_provided
    assert "vmro3" in vars_provided
    assert "concpm10" in vars_provided
    assert "concno2" in vars_provided
    paths = reader.filepaths
    assert len(paths) == 3


@pytest.mark.parametrize(
    "filename,ts_type",
    [
        ("Base_hour.nc", "hourly"),
        ("Base_month.nc", "monthly"),
        ("Base_day.nc", "daily"),
        ("Base_fullrun", "yearly"),
    ],
)
def test_ReadMscwCtm_ts_type_from_filename(reader, filename, ts_type):
    assert reader.ts_type_from_filename(filename) == ts_type


def test_ReadMscwCtm_ts_type_from_filename_error(reader):
    with pytest.raises(ValueError) as e:
        reader.ts_type_from_filename("blaaa")
    assert str(e.value) == "Failed to retrieve ts_type from filename blaaa"


@pytest.mark.parametrize(
    "filename,ts_type",
    [
        ("Base_hour.nc", "hourly"),
        ("Base_month.nc", "monthly"),
        ("Base_day.nc", "daily"),
        ("Base_fullrun.nc", "yearly"),
    ],
)
def test_ReadMscwCtm_filename_from_ts_type(reader, filename, ts_type):
    reader._file_mask = reader.FILE_MASKS[0]
    assert reader.filename_from_ts_type(ts_type) == filename


def test_ReadMscwCtm_filename_from_ts_type_error(reader):
    reader._file_mask = reader.FILE_MASKS[0]
    with pytest.raises(ValueError) as e:
        reader.filename_from_ts_type("blaaa")
    assert str(e.value) == "failed to infer filename from input ts_type=blaaa"


def test_ReadMscwCtm_years_avail():
    reader = ReadMscwCtm(data_dir=EMEP_DIR)
    assert reader.years_avail == ["2017"]


def test_ReadMscwCtm_preprocess_units():
    units = ""
    prefix = "AOD"
    assert ReadMscwCtm().preprocess_units(units, prefix) == "1"


def test_ReadMscwCtm_open_file():
    reader = ReadMscwCtm()
    with pytest.raises(AttributeError):
        reader.open_file()
    reader.data_dir = EMEP_DIR
    data = reader.open_file()
    assert isinstance(data["2017"], xr.Dataset)
    assert reader._filedata is data


@pytest.mark.parametrize(
    "var_name, value",
    [
        ("od550gt1aer", False),
        ("absc550aer", True),
        ("concpm10", True),
        ("sconcpm10", True),
    ],
)
def test_ReadMscwCtm_has_var(reader, var_name, value):
    assert reader.has_var(var_name) == value


def test_ReadMscwCtm_has_var_error(reader):
    with pytest.raises(exc.VariableDefinitionError) as e:
        reader.has_var("blaa")
    assert str(e.value) == "Error (VarCollection): input variable blaa is not supported"


def test_ReadMscwCtm_filepath(reader):
    path = Path(EMEP_DIR) / "Base_month.nc"
    reader.filepath = str(path)
    assert Path(reader.filepath) == path


@pytest.mark.parametrize(
    "value, exception, error",
    [
        (None, TypeError, "needs to be a string"),
        ("", FileNotFoundError, ""),
        (
            "/tmp",
            FileNotFoundError,
            "No valid model files could be found in / for any of the supported file masks: ['Base_*.nc']",
        ),
    ],
)
def test_ReadMscwCtm_filepath_error(reader, value, exception, error):
    with pytest.raises(exception) as e:
        reader.filepath = value
    assert str(e.value) == error


def test_ReadMscwCtm__str__():
    assert str(ReadMscwCtm()) == "ReadMscwCtm"


def test_ReadMscwCtm__repr__():
    assert repr(ReadMscwCtm()) == "ReadMscwCtm"


def test_ReadEMEP__init__():
    assert isinstance(ReadEMEP(), ReadMscwCtm)


def emep_data_path(tmp_path: Path, freq: str | list[str], vars_and_units: dict[str, str]) -> Path:

    reader = ReadMscwCtm()
    varmap = reader.var_map

    root = tmp_path / "emep"
    frequencies = freq if isinstance(freq, list) else [freq]
    for freq in frequencies:
        ds = xr.Dataset()
        for var_name, units in vars_and_units.items():
            var_name = varmap[var_name]
            ds[var_name] = _create_fake_MSCWCtm_data(tst=reader.FREQ_CODES[freq])
            ds[var_name].attrs.update(units=units, var_name=var_name)

        for year in ["2017", "2018", "2019", "2015", "2018", "2013"]:
            path = root / str(year) / f"Base_{freq}.nc"
            path.parent.mkdir(exist_ok=True, parents=True)
            ds.to_netcdf(path)
    return root


@pytest.fixture
def data_path(tmp_path: Path, freq: str | list[str], vars_and_units: dict[str, str]) -> Path:
    return emep_data_path(tmp_path, freq, vars_and_units)


def test_ReadMscwCtm_aux_var_defs():
    req = ReadMscwCtm.AUX_REQUIRES
    funs = ReadMscwCtm.AUX_FUNS
    assert len(req) == len(funs)
    assert all([x in funs.keys() for x in req])


M_N = 14.006
M_O = 15.999
M_H = 1.007
M_HNO3 = M_H + M_N + M_O * 3
M_NO3 = M_N + M_O * 3


@pytest.mark.parametrize(
    "vars_and_units,freq,add_read,chk_mean",
    [
        ({"wetoxs": "mg S m-2"}, "day", None, {"wetoxs": 1}),
        ({"prmm": "mm"}, "hour", None, {"prmm": 24}),
        ({"prmm": "mm d-1"}, "hour", None, {"prmm": 1}),
        ({"concpm10": "ug m-3"}, "day", None, {"concpm10": 1}),
        ({"concpm10": "ug m-3"}, "hour", None, None),
        (
            {"concno3c": "ug m-3", "concno3f": "ug m-3"},
            "day",
            ["concno3"],
            {"concno3c": 1, "concno3f": 1, "concno3": 2},
        ),
        (
            {"concno3c": "ug m-3", "concno3f": "ug m-3", "conchno3": "ug m-3"},
            "day",
            ["concNtno3"],
            {
                "concno3c": 1,
                "concno3f": 1,
                "conchno3": 1,
                "concNtno3": 2 * M_N / M_NO3 + M_N / M_HNO3,
            },
        ),
        ({"wetoxs": "mg S m-2 d-1"}, "day", None, {"wetoxs": 1}),
        ({"wetoxs": "Tg S m-2 d-1"}, "day", None, {"wetoxs": 1e15}),
    ],
)
def test_read_emep_dummy_data(
    data_path: Path,
    vars_and_units: dict[str, str],
    freq: str,
    add_read: list[str] | None,
    chk_mean: dict[str, float],
):
    reader = ReadMscwCtm(data_dir=str(data_path / "2017"))
    tst = reader.FREQ_CODES[freq]
    objs = {}
    for var in vars_and_units:
        data = reader.read_var(var, ts_type=tst)
        objs[var] = data
        assert isinstance(data, GriddedData)
        aerocom_unit = cf_units.Unit(get_variable(var).units)
        assert cf_units.Unit(data.units) == aerocom_unit
        assert data.ts_type == tst
    if isinstance(add_read, list):
        for var in add_read:
            data = reader.read_var(var, ts_type=tst)
            objs[var] = data
    if isinstance(chk_mean, dict):
        for var, mean in chk_mean.items():
            np.testing.assert_allclose(objs[var].cube.data.mean(), mean, atol=0.1)


def test_read_emep_dummy_data_error(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "day", vars_and_units={"concno3c": "ug m-3"})
    reader = ReadMscwCtm(data_dir=str(data_path / "2017"))
    with pytest.raises(exc.VarNotAvailableError) as e:
        reader.read_var("concno3", ts_type="daily")
    assert str(e.value) == "concno3f (SURF_ug_NO3_F) not available in Base_day.nc"


@pytest.mark.parametrize(
    "year,years,freq",
    [
        ("", [2013, 2015, 2017, 2018, 2019], "day"),
        ("2017", [2017], "month"),
        ("2019", [2019], "hour"),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_read_emep_clean_filepaths(data_path: Path, year, years: list[int], freq: str):
    reader = ReadMscwCtm(data_dir=str(data_path / year))
    tst = reader.FREQ_CODES[freq]

    filepaths = reader.filepaths

    cleaned_paths = reader._clean_filepaths(filepaths, years, tst)
    assert len(cleaned_paths) == len(years)

    found = []
    for path in cleaned_paths:
        assert path in filepaths

        year = re.search(r".*(20\d\d).*", Path(path).parent.name).group(1)
        found.append(int(year))

    assert found == sorted(years)


@pytest.mark.parametrize(
    "years,freq,error",
    [
        ([2013, 2015, 2017, 2018, 2019, 2012], "month", "A different amount of years "),
        ([2013, 2016, 2017], "day", "The year "),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_read_emep_clean_filepaths_error(data_path: Path, years, freq: str, error: str):
    reader = ReadMscwCtm(data_dir=str(data_path))
    tst = reader.FREQ_CODES[freq]
    filepaths = reader.filepaths
    with pytest.raises(ValueError) as e:
        reader._clean_filepaths(filepaths, years, tst)

    assert error in str(e.value)


@pytest.mark.parametrize(
    "freq,wrong_name",
    [
        ("day", "Base_day.nc"),
        ("month", "Base_month.nc"),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_read_emep_wrong_filenames(data_path: Path, freq: str, wrong_name: str):
    reader = ReadMscwCtm(data_dir=str(data_path))
    tst = reader.FREQ_CODES[freq]
    filepaths = reader.filepaths
    years = reader._get_yrs_from_filepaths()
    cleaned_paths = reader._clean_filepaths(filepaths, years, tst)

    wrong_path = Path(filepaths[0]).with_name(wrong_name)
    filepaths[0] = str(wrong_path)
    new_years = reader._get_yrs_from_filepaths()
    new_cleaned_paths = reader._clean_filepaths(filepaths, new_years, tst)

    assert len(years) == len(new_years)
    assert len(cleaned_paths) == len(new_cleaned_paths)


@pytest.mark.parametrize(
    "freq,wrong_tst",
    [
        ("month", "minute"),
        ("day", "daily"),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_read_emep_wrong_tst(data_path: Path, wrong_tst: str):
    reader = ReadMscwCtm(data_dir=str(data_path))
    with pytest.raises(ValueError) as e:
        filepaths = reader.filepaths
        wrong_path = Path(filepaths[0]).with_name(f"Base_{wrong_tst}.nc")
        reader._get_tst_from_file(str(wrong_path))

    assert str(e.value) == f"The ts_type {wrong_tst} is not supported"


def test_read_emep_LF_tst(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "month", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    filepaths = reader.filepaths
    wrong_path = Path(filepaths[0]).with_name(f"Base_LF_month.nc")

    assert reader._get_tst_from_file(str(wrong_path)) is None


def test_read_emep_year_defined_twice(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "day", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    filepaths = reader.filepaths
    wrong_path = Path(filepaths[0]).with_name(f"Base_day.nc")
    filepaths.append(str(wrong_path))
    new_yrs = reader._get_yrs_from_filepaths()
    with pytest.raises(ValueError) as e:
        reader._clean_filepaths(filepaths, new_yrs, "daily")
    assert "is already found:" in str(e.value)


@pytest.mark.parametrize(
    "year,freq,num",
    [
        ("", "day", 5),
        ("2017", "month", 1),
        ("2019", "hour", 1),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_read_emep_multiple_dirs(data_path: Path, year: str, freq: str, num: int):
    reader = ReadMscwCtm(data_dir=str(data_path / year))
    assert len(reader.filepaths) == num
    assert all(freq in Path(file).stem for file in reader.filepaths)

    tst = reader.FREQ_CODES[freq]
    data = reader.read_var("prmm", ts_type=tst)
    assert data.ts_type == tst


def test_read_emep_multiple_dirs_hour_error(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "hour", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    with pytest.raises(ValueError) as e:
        reader.read_var("prmm", ts_type="hourly")
    assert str(e.value) == "ts_type hourly can not be hourly when using multiple years"


@pytest.mark.parametrize(
    "year,freq,num",
    [
        ("", "day", 5),
        ("2017", "month", 1),
        ("2019", "hour", 1),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_search_all_files(data_path: Path, year: str, num: int):
    reader = ReadMscwCtm()
    with pytest.raises(AttributeError):
        reader.search_all_files()

    with pytest.raises(AttributeError):
        reader.filepaths

    reader._data_dir = str(data_path / year)

    reader.search_all_files()
    assert len(reader.filepaths) == num


@pytest.mark.parametrize(
    "year,freq,",
    [
        ("", ["day"]),
        ("", ["day", "hour"]),
        ("2017", ["month"]),
        ("2019", ["hour", "day", "month"]),
    ],
)
@pytest.mark.parametrize("vars_and_units", [{"prmm": "mm"}])
def test_ts_types(data_path: Path, year: str, freq: list[str]):
    reader = ReadMscwCtm()
    with pytest.raises(AttributeError):
        reader.ts_types

    reader.data_dir = str(data_path / year)
    ts_types = reader.ts_types
    assert len(ts_types) == len(freq)
