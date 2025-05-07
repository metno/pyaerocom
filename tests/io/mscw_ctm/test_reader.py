from __future__ import annotations

import os
import re
from pathlib import Path

from pyaerocom.units import Unit
import pytest
import xarray as xr

import pyaerocom.exceptions as exc
from pyaerocom import get_variable
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.mscw_ctm.reader import ReadEMEP, ReadMscwCtm
from tests.conftest import TEST_RTOL
from tests.fixtures.mscw_ctm import create_fake_MSCWCtm_data


@pytest.fixture()
def reader() -> ReadMscwCtm:
    """empty EMEP MSCW-CTM reader"""
    return ReadMscwCtm()


@pytest.fixture()
def data_dir(path_emep: dict[str, str]) -> str:
    """path to EMEP test data"""
    return path_emep["data_dir"]


def test_ReadMscwCtm__get_year_from_nc(data_dir: str):
    yr = ReadMscwCtm._get_year_from_nc(os.path.join(data_dir, "Base_fullrun.nc"))
    assert yr == 2017
    yr = ReadMscwCtm._get_year_from_nc(os.path.join(data_dir, "Base_day.nc"))
    assert yr == 2017
    yr = ReadMscwCtm._get_year_from_nc(os.path.join(data_dir, "Base_month.nc"))
    assert yr == 2017


def test_ReadMscwCtm__init__(data_dir: str):
    reader = ReadMscwCtm("EMEP_2017", data_dir)
    assert getattr(reader, "data_id") == "EMEP_2017"
    assert getattr(reader, "_data_dir") == data_dir


def test_ReadMscwCtm__init___error():
    data_dir = "not_a_real_path"
    with pytest.raises(FileNotFoundError) as e:
        ReadMscwCtm(None, data_dir)
    assert str(e.value) == data_dir


def test_ReadMscwCtm_data_dir(data_dir: str):
    reader = ReadMscwCtm()
    reader._data_dir = data_dir
    assert Path(reader._data_dir) == Path(data_dir)


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
        reader._data_dir = value
    assert str(e.value) == error


def test__ReadMscwCtm__check_files_in_data_dir(data_dir: str):
    reader = ReadMscwCtm()
    matches = reader._check_files_in_data_dir(data_dir)
    assert len(matches) == 3


def test__ReadMscwCtm__check_files_in_data_dir_error():
    reader = ReadMscwCtm()
    with pytest.raises(FileNotFoundError):
        reader._check_files_in_data_dir("/tmp")


def test_ReadMscwCtm_ts_type():
    reader = ReadMscwCtm()
    assert reader._ts_type == "daily"


def test_ReadMscwCtm_var_map():
    var_map = ReadMscwCtm().var_map
    assert isinstance(var_map, dict)


@pytest.mark.parametrize(
    "var_name, ts_type", [("vmro3", "daily"), ("vmro3", None), ("concpmgt25", "daily")]
)
def test_ReadMscwCtm_read_var(var_name: str, ts_type: str, data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)
    data = reader.read_var(var_name, ts_type)
    assert isinstance(data, GriddedData)
    if ts_type is not None:
        assert data.ts_type == ts_type
    assert data.ts_type is not None
    assert data.ts_type == reader._ts_type


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
    var_name: str, ts_type: str, exception: type[Exception], error: str, data_dir: str
):
    reader = ReadMscwCtm(data_dir=data_dir)
    with pytest.raises(exception) as e:
        reader.read_var(var_name, ts_type)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "var_name, ts_type",
    [
        ("concpmgt25", "daily"),
        ("concpmgt25", "monthly"),
    ],
)
def test_ReadMscwCtm__compute_var(var_name, ts_type, data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)
    data, proj_info = reader._compute_var(var_name, ts_type)
    assert isinstance(data, xr.DataArray)


def test_ReadMscwCtm__compute_var_error(data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)
    with pytest.raises(KeyError):
        reader._compute_var("blaaa", "daily")


def test_ReadMscwCtm_data(data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)

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


def test_ReadMscwCtm_directory(data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)
    assert reader._data_dir == data_dir
    vars_provided = reader.vars_provided
    assert "vmro3" in vars_provided
    assert "concpm10" in vars_provided
    assert "concno2" in vars_provided
    paths = reader._filepaths
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
    assert reader._ts_type_from_filename(filename) == ts_type


def test_ReadMscwCtm_ts_type_from_filename_error(reader):
    with pytest.raises(ValueError) as e:
        reader._ts_type_from_filename("blaaa")
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
    assert reader._filename_from_ts_type(ts_type) == filename


def test_ReadMscwCtm_filename_from_ts_type_error(reader):
    with pytest.raises(ValueError) as e:
        reader._filename_from_ts_type("blaaa")
    assert str(e.value) == "unknown ts_type=blaaa"


def test_ReadMscwCtm_years_avail(data_dir: str):
    reader = ReadMscwCtm(data_dir=data_dir)
    assert reader.years_avail == ["2017"]


def test_ReadMscwCtm_preprocess_units():
    units = ""
    prefix = "AOD"
    assert ReadMscwCtm()._preprocess_units(units, prefix) == "1"


def test_ReadMscwCtm_open_file(data_dir: str):
    reader = ReadMscwCtm()
    with pytest.raises(AttributeError):
        reader._open_file()
    reader._data_dir = data_dir
    data = reader._open_file()
    assert isinstance(data, xr.Dataset)
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
    with pytest.raises(exc.VariableDefinitionError, match="input variable blaa is not supported"):
        reader.has_var("blaa")


def test_ReadMscwCtm__str__():
    assert str(ReadMscwCtm()) == "ReadMscwCtm"


def test_ReadMscwCtm__repr__():
    assert repr(ReadMscwCtm()) == "ReadMscwCtm"


def test_ReadEMEP__init__():
    with pytest.warns(DeprecationWarning, match="use ReadMscwCtm instead"):
        assert isinstance(ReadEMEP(), ReadMscwCtm)


def emep_data_path(tmp_path: Path, freq: str | list[str], vars_and_units: dict[str, str]) -> Path:
    reader = ReadMscwCtm()
    varmap = reader.var_map

    root = tmp_path / "emep"
    frequencies = freq if isinstance(freq, list) else [freq]
    for freq in frequencies:
        for year in ["2017", "2018", "2019", "2015", "2018", "2013"]:
            ds = xr.Dataset()
            for var_name, units in vars_and_units.items():
                var_name = varmap[var_name]
                ds[var_name] = create_fake_MSCWCtm_data(year=year, tst=reader.FREQ_CODES[freq])
                ds[var_name].attrs.update(units=units, var_name=var_name)

            path = root / str(year) / f"Base_{freq}.nc"
            path.parent.mkdir(exist_ok=True, parents=True)
            ds.to_netcdf(path)
    return root


@pytest.fixture
def data_path(tmp_path: Path, freq: str | list[str], vars_and_units: dict[str, str]) -> Path:
    """emep test data on a temporary path"""
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
            {"concoxn": "ug m-3"},
            "day",
            ["concNtno3"],
            {
                "concoxn": 1,
                "concNtno3": M_N / (M_N + 3 * M_O),
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
        aerocom_unit = Unit(get_variable(var).units)
        assert Unit(data.units) == aerocom_unit
        assert data.ts_type == tst
    if isinstance(add_read, list):
        for var in add_read:
            data = reader.read_var(var, ts_type=tst)
            objs[var] = data
    if isinstance(chk_mean, dict):
        for var, mean in chk_mean.items():
            assert objs[var].cube.data.mean() == pytest.approx(mean, abs=0.1, rel=TEST_RTOL)


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

    filepaths = reader._filepaths

    cleaned_paths = reader._clean_filepaths(filepaths, years, tst)
    # assert len(cleaned_paths) == len(years)

    found = []
    for path in cleaned_paths:
        assert path in filepaths
        match = re.search(r".*(20\d\d).*", Path(path).parent.name)
        assert match is not None
        year = int(match.group(1))
        found.append(year)

    assert set(found) == set(years)


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
    filepaths = reader._filepaths
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
    filepaths = reader._filepaths
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
        filepaths = reader._filepaths
        wrong_path = Path(filepaths[0]).with_name(f"Base_{wrong_tst}.nc")
        reader._get_tst_from_file(str(wrong_path))

    assert " does not match file_pattern " in str(e.value)


def test_read_emep_LF_tst(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "month", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    with pytest.raises(ValueError) as e:
        filepaths = reader._filepaths
        wrong_path = Path(filepaths[0]).with_name("Base_LF_month.nc")
        reader._get_tst_from_file(str(wrong_path))

    assert " does not match file_pattern " in str(e.value)


@pytest.mark.xfail
def test_read_emep_year_defined_twice(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "day", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    filepaths = reader._filepaths
    wrong_path = Path(filepaths[0]).with_name("Base_day.nc")
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
    assert len(reader._filepaths) == num
    assert all(freq in Path(file).stem for file in reader._filepaths)

    tst = reader.FREQ_CODES[freq]
    data = reader.read_var("prmm", ts_type=tst)
    assert data.ts_type == tst


def test_read_emep_multiple_dirs_hour_error(tmp_path: Path):
    data_path = emep_data_path(tmp_path, "hour", vars_and_units={"prmm": "mm"})
    reader = ReadMscwCtm(data_dir=str(data_path))
    with pytest.raises(ValueError) as e:
        reader.read_var("prmm", ts_type="hourly")
    assert "can not be hourly when using multiple years" in str(e.value)


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
        reader._search_all_files()

    with pytest.raises(AttributeError):
        reader._filepaths

    reader._data_dir = str(data_path / year)

    reader._search_all_files()
    assert len(reader._filepaths) == num


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

    reader._data_dir = str(data_path / year)
    ts_types = reader.ts_types
    assert len(ts_types) == len(freq)


def test_add_aux_compute(tmp_path: Path):
    data_path = emep_data_path(
        tmp_path, "day", vars_and_units={"concno3c": "ug m-3", "concno3f": "ug m-3"}
    )
    reader = ReadMscwCtm(data_dir=str(data_path / "2017"))

    def calc_concno3(concno3c, concno3f):
        concno3 = concno3c.copy(deep=True) + concno3f.copy(deep=True)
        concno3.attrs["units"] = "ug m-3"
        return concno3

    new_var_name = "concno3"
    vars_required = ["concno3c", "concno3f"]
    func = calc_concno3

    reader.add_aux_compute(new_var_name, vars_required=vars_required, fun=func)

    assert reader.has_var(new_var_name)

    data = reader.read_var(new_var_name, "daily")

    assert data.var_name == new_var_name


def test_emep_vars():
    new_var_name = "concno3"
    new_mapping = "SURF_ug_NO3_C"

    reader = ReadMscwCtm(emep_vars={new_var_name: new_mapping})

    assert new_var_name in reader.var_map
    assert reader.var_map[new_var_name] == new_mapping


def test_reader_regexp(tmp_path: Path):
    path = tmp_path / "2022"
    path.mkdir()
    # Create files that should be matched by regexp.
    for i in range(10):
        (path / f"file_{i}.nc").touch()

    # Create files that should NOT be matched by regexp.
    for i in range(10):
        (path / f"blah_{i}.nc").touch()

    reader = ReadMscwCtm("test", data_dir=str(path), file_pattern=r"^file_\d\.nc$")

    reader._search_all_files()

    assert len(reader._private.filepaths) == 10
