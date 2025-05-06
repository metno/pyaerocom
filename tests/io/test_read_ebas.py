from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
import pytest

from pyaerocom import const
from pyaerocom.aux_var_helpers import (
    compute_ac550dryaer,
    compute_ang4470dryaer_from_dry_scat,
    compute_sc440dryaer,
    compute_sc550dryaer,
    compute_sc700dryaer,
)
from pyaerocom.exceptions import (
    DataCoverageError,
    MetaDataError,
    NotInFileError,
    TemporalResolutionError,
    VariableDefinitionError,
    VarNotAvailableError,
)
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.read_ebas import ReadEbas, ReadEbasOptions
from pyaerocom.stationdata import StationData
from pyaerocom.ungridded_data_metadata import UngriddedDataMetadata


@pytest.fixture(scope="module")
def reader() -> ReadEbas:
    return ReadEbas("EBASSubset")


def test_DATA_ID(reader: ReadEbas):
    assert reader.data_id == "EBASSubset"


def test_FILE_SUBDIR_NAME(reader: ReadEbas):
    assert reader.FILE_SUBDIR_NAME == "data"


def test_SQL_DB_NAME(reader: ReadEbas):
    # Name of sqlite database file
    assert reader.SQL_DB_NAME == "ebas_file_index.sqlite3"


def test_SUPPORTED_DATASETS(reader: ReadEbas):
    assert reader.SUPPORTED_DATASETS == ["EBASMC", "EBASSubset"]


def test_CACHE_SQLITE_FILE(reader: ReadEbas):
    assert reader.CACHE_SQLITE_FILE == ["EBASMC"]


def test_TS_TYPE(reader: ReadEbas):
    assert reader.TS_TYPE == "undefined"


def test_MERGE_STATIONS(reader: ReadEbas):
    assert reader.MERGE_STATIONS == {
        "Birkenes": "Birkenes II",
        "Rörvik": "Råö",
        "Vavihill": "Hallahus",
        "Virolahti II": "Virolahti III",
    }


def test_DEFAULT_VARS(reader: ReadEbas):
    assert reader.DEFAULT_VARS == reader.PROVIDES_VARIABLES


def test_TS_TYPE_CODES(reader: ReadEbas):
    assert reader.TS_TYPE_CODES == {
        "1mn": "minutely",
        "1h": "hourly",
        "1d": "daily",
        "1w": "weekly",
        "1mo": "monthly",
        "mn": "minutely",
        "h": "hourly",
        "d": "daily",
        "w": "weekly",
        "mo": "monthly",
    }


def test_AUX_REQUIRES(reader: ReadEbas):
    AUX_REQUIRES = dict(
        sc550dryaer=["sc550aer", "scrh"],
        sc440dryaer=["sc440aer", "scrh"],
        sc700dryaer=["sc700aer", "scrh"],
        ac550dryaer=["ac550aer", "acrh"],
        ang4470dryaer=["sc440dryaer", "sc700dryaer"],
    )
    for var_name, requires in AUX_REQUIRES.items():
        assert var_name in reader.AUX_REQUIRES
        assert requires == reader.AUX_REQUIRES[var_name]


def test_AUX_USE_META(reader: ReadEbas):
    AUX_USE_META = dict(
        sc550dryaer="sc550aer",
        sc440dryaer="sc440aer",
        sc700dryaer="sc700aer",
        ac550dryaer="ac550aer",
    )
    for var, ovar in AUX_USE_META.items():
        assert var in reader.AUX_USE_META
        assert reader.AUX_USE_META[var] == ovar


def test_AUX_FUNS(reader: ReadEbas):
    AUX_FUNS = dict(
        sc440dryaer=compute_sc440dryaer,
        sc550dryaer=compute_sc550dryaer,
        sc700dryaer=compute_sc700dryaer,
        ac550dryaer=compute_ac550dryaer,
        ang4470dryaer=compute_ang4470dryaer_from_dry_scat,
    )
    for var, func in AUX_FUNS.items():
        assert var in reader.AUX_FUNS
        assert reader.AUX_FUNS[var] == func


def test_ASSUME_AE_SHIFT_WVL(reader: ReadEbas):
    assert reader.ASSUME_AE_SHIFT_WVL == 1.0


def test_ASSUME_AAE_SHIFT_WVL(reader: ReadEbas):
    assert reader.ASSUME_AAE_SHIFT_WVL == 1.0


def test_IGNORE_FILES(reader: ReadEbas):
    assert reader.IGNORE_FILES == [
        "CA0420G.20100101000000.20190125102503.filter_absorption_photometer.aerosol_absorption_coefficient.aerosol.1y.1h.CA01L_Magee_AE31_ALT.CA01L_aethalometer.lev2.nas",
        "DK0022R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_22.DK01L_IC.lev2.nas",
        "DK0012R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_12.DK01L_IC.lev2.nas",
        "DK0008R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_08.DK01L_IC.lev2.nas",
        "DK0005R.20180101070000.20191014000000.bulk_sampler..precip.1y.15d.DK01L_bs_05.DK01L_IC.lev2.nas",
    ]


def test_opts(reader: ReadEbas):
    DEFAULTS = dict(
        prefer_statistics=["arithmetic mean", "median"],
        ignore_statistics=["percentile:15.87", "percentile:84.13"],
        wavelength_tol_nm=50,
        shift_wavelengths=True,
        assume_default_ae_if_unavail=True,
        check_correct_MAAP_wrong_wvl=False,
        eval_flags=True,
        keep_aux_vars=False,
        convert_units=True,
        try_convert_vmr_conc=True,
        ensure_correct_freq=False,
        freq_from_start_stop_meas=True,
        freq_min_cov=0.0,
    )
    opts = reader._opts
    assert isinstance(opts, dict)
    assert "default" in opts
    assert isinstance(opts["default"], ReadEbasOptions)
    assert len(DEFAULTS) == len(opts["default"])
    for opt, val in opts["default"].items():
        assert opt in DEFAULTS
        assert val == DEFAULTS[opt]


def test_data_id(reader: ReadEbas):
    assert reader.data_id == "EBASSubset"


def test_file_dir(reader: ReadEbas):
    assert reader._file_dir is None

    with pytest.raises(FileNotFoundError):
        reader.file_dir = 42

    path = Path(reader.file_dir)
    assert path.name == "data"
    assert path.exists()
    assert path.is_dir()

    reader.file_dir = str(path)  # sets private attr _file_dir
    assert reader._file_dir == reader.file_dir == str(path)


def test_FILE_REQUEST_OPTS(reader: ReadEbas):
    assert reader.FILE_REQUEST_OPTS == [
        "variables",
        "start_date",
        "stop_date",
        "station_names",
        "matrices",
        "altitude_range",
        "lon_range",
        "lat_range",
        "instrument_types",
        "statistics",
        "datalevel",
    ]


def test__FILEMASK(reader: ReadEbas):
    with pytest.raises(AttributeError) as e:
        reader._FILEMASK
    assert str(e.value) == (
        "Irrelevant for EBAS implementation, since SQL database is used for finding valid files"
    )


def test_NAN_VAL(reader: ReadEbas):
    with pytest.raises(AttributeError) as e:
        reader.NAN_VAL
    assert (
        str(e.value)
        == "Irrelevant for EBAS implementation: Info about invalid measurements is extracted from header of NASA Ames files for each variable individually "
    )


def test_PROVIDES_VARIABLES(reader: ReadEbas):
    PROVIDES_VARIABLES = {
        "DEFAULT",
        "concebc",
        "concca",
        "concmg",
        "conck",
        "sc550aer",
        "sc440aer",
        "sc700aer",
        "sc550dryaer",
        "sc440dryaer",
        "sc700dryaer",
        "sc550lt1aer",
        "bsc550aer",
        "ac550aer",
        "ac550dryaer",
        "ac550lt1aer",
        "bsc550dryaer",
        "scrh",
        "acrh",
        "ts",
        "concso4",
        "SO4ugSm3",
        "concso4pm10",
        "concso4pm25",
        "concso4pm1",
        "concso2",
        "vmrso2",
        "concpm10",
        "concpm25",
        "concpm1",
        "concso4t",
        "concso4c",
        "concbc",
        "conceqbc",
        "concCec",
        "concCecpm25",
        "conctc",
        "concoa",
        "concoc",
        "concCoc",
        "concCocpm25",
        "concss",
        "concsspm10",
        "concsspm25",
        "concnh3",
        "concNnh3",
        "concno3",
        "concNno3pm10",
        "concNno3pm25",
        "concNno3pm1",
        "concno3pm10",
        "concno3pm25",
        "concno3pm1",
        "concnh4",
        "concNnh4",
        "concNhno3",
        "concNtno3",
        "concNtnh",
        "concno",
        "concno2",
        "concNno2",
        "conchcho",
        "conco3",
        "concco",
        "vmro3",
        "vmro3max",
        "vmrco",
        "vmrno2",
        "vmrno",
        "vmrisop",
        "vmrhcho",
        "vmrglyoxal",
        "vmrc2h6",
        "vmrc2h4",
        "concglyoxal",
        "concprcpoxs",
        "concprcpoxn",
        "concprcprdn",
        "wetoxs",
        "wetrdn",
        "wetoxn",
        "pr",
        "prmm",
        "concnh4pm10",
        "concnh4pm25",
        "concnh4pm1",
        "concCocpm10",
        "concNno",
        "concCecpm10",
        "concSso2",
        "vmrnh3",
        "proxydryoxn",
        "proxywetpm25",
        "concss25",
        "concprcpno3",
        "concprcpso4",
        "concCoc25",
        "concom25",
        "concom1",
        "concprcpnh4",
        "concsscoarse",
        "proxydryhno3",
        "proxydryhono",
        "proxydryn2o5",
        "proxydrynh3",
        "proxydrynh4",
        "proxydryno2",
        "proxydryno2no2",
        "proxydryno3c",
        "proxydryno3f",
        "proxydryo3",
        "proxydryoxs",
        "proxydryss",
        "proxydryna",
        "proxydrypm10",
        "proxydrypm25",
        "proxydryrdn",
        "proxydryso2",
        "proxydryso4",
        "proxywethno3",
        "proxywethono",
        "proxywetn2o5",
        "proxywetnh3",
        "proxywetnh4",
        "proxywetno2",
        "proxywetno2no2",
        "proxywetno3c",
        "proxywetno3f",
        "proxyweto3",
        "proxywetoxn",
        "proxywetoxs",
        "proxywetpm10",
        "proxywetrdn",
        "proxywetso2",
        "proxywetso4",
        "vmrhno3",
        "vmrtp",
        "wetnh4",
        "wetno3",
        "wetso4",
        "wetna",
        "concprcpoxst",
        "wetoxsc",
        "concprcpoxsc",
        "wetoxst",
        "concprcpna",
        "wetso4pr",
        "wetrdnpr",
        "wetoxspr",
    }

    assert set(reader.PROVIDES_VARIABLES) == (PROVIDES_VARIABLES)


def test_sqlite_database_file(reader: ReadEbas):
    file = reader.sqlite_database_file
    assert Path(file).exists()
    assert file.endswith("ebas_file_index.sqlite3")


@pytest.mark.parametrize(
    "vars_to_retrieve,constraints",
    [
        ("vmrno", {}),
        ("sc550aer", {}),
        ("sc550dryaer", {}),
        ("sc550dryaer", {"station_names": "Jungfraujoch"}),
        ("ac550aer", {}),
        ("concpm10", {}),
        ("conco3", {}),
        (["sc550aer", "ac550aer", "concpm10", "conco3"], {}),
        (["sc550aer", "ac550aer", "concpm10", "conco3"], {"station_names": "*Kose*"}),
    ],
)
def test_get_file_list(
    reader: ReadEbas, vars_to_retrieve: list[str] | str, constraints: dict[str, str]
):
    files = reader.get_file_list(vars_to_retrieve, **constraints)
    assert isinstance(files, list)
    assert files


def test_get_file_list_error(reader: ReadEbas):
    with pytest.raises(FileNotFoundError) as e:
        reader.get_file_list("vmrno", station_names="xkcd")
    assert (
        str(e.value)
        == "No files could be found for ['vmrno'] and reading constraints {'station_names': 'xkcd'}."
    )


def test__merge_lists(reader: ReadEbas):
    vars_to_retrieve = ["sc550aer", "ac550aer"]
    files = reader.get_file_list(vars_to_retrieve)
    assert list(reader._lists_orig) == vars_to_retrieve
    assert reader._merge_lists(reader._lists_orig) == files


def test__find_station_matches(reader: ReadEbas):
    assert reader._find_station_matches("*fraujo*") == ["Jungfraujoch"]


@pytest.mark.parametrize(
    "val,exception,error",
    [
        pytest.param(
            "Bla",
            FileNotFoundError,
            "No EBAS data files could be found for stations Bla",
            id="station not found",
        ),
        pytest.param(
            42,
            ValueError,
            "Need list or string...",
            id="wrong pattern type",
        ),
    ],
)
def test__find_station_matches_error(
    reader: ReadEbas, val: Literal["Bla", 42], exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        reader._find_station_matches(val)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "vars_to_retrieve,result",
    [
        (None, None),
        (["sconco3"], ["conco3"]),
    ],
)
def test__precheck_vars_to_retrieve(
    reader: ReadEbas, vars_to_retrieve: list[str] | None, result: list[str] | None
):
    if result is None:
        result = reader.PROVIDES_VARIABLES
    assert reader._precheck_vars_to_retrieve(vars_to_retrieve) == result


def test_get_ebas_var(reader: ReadEbas):
    var_name = "sc550aer"
    info = reader.get_ebas_var(var_name)
    assert isinstance(info, EbasVarInfo)
    assert var_name in reader._loaded_ebas_vars


@pytest.mark.parametrize(
    "var_name,exception,error",
    [
        pytest.param(
            "blaaablub",
            VariableDefinitionError,
            "Error (VarCollection): input variable blaaablub is not supported",
            id="VariableDefinitionError",
        ),
        pytest.param(
            "abs550aer",
            VarNotAvailableError,
            "Variable abs550aer is not available in EBAS interface",
            id="VarNotAvailableError",
        ),
    ],
)
def test_get_ebas_var_error(
    reader: ReadEbas, var_name: str, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        reader.get_ebas_var(var_name)
    assert str(e.value) == error


def test__get_var_cols(reader: ReadEbas, loaded_nasa_ames_example: EbasNasaAmesFile):
    info = EbasVarInfo("sc550aer")
    cols = reader._get_var_cols(info, loaded_nasa_ames_example)
    assert cols == [14, 17, 20]


@pytest.mark.parametrize(
    "var,error",
    [
        ("ac550aer", "Variable ac550aer could not be found in file"),
        ("sc550dryaer", ""),
    ],
)
def test__get_var_cols_error(
    reader: ReadEbas, loaded_nasa_ames_example: EbasNasaAmesFile, var: str, error: str
):
    info = EbasVarInfo(var)
    with pytest.raises(NotInFileError) as e:
        reader._get_var_cols(info, loaded_nasa_ames_example)
    assert str(e.value) == error


def test_find_var_cols(reader: ReadEbas, loaded_nasa_ames_example: EbasNasaAmesFile):
    vars_to_read = ["sc550aer", "scrh", "ts"]
    columns = reader.find_var_cols(vars_to_read, loaded_nasa_ames_example)
    assert columns["sc550aer"] == 17
    assert columns["scrh"] == 3
    assert columns["ts"] == 4


@pytest.mark.parametrize(
    "ts_type,tol_percent,num_flagged",
    [
        ("hourly", 5, 0),
        ("daily", 5, 8760),
        ("hourly", 0, 5840),
    ],
)
def test__flag_incorrect_frequencies(
    monkeypatch: pytest.MonkeyPatch,
    reader: ReadEbas,
    loaded_nasa_ames_example: EbasNasaAmesFile,
    ts_type: str,
    tol_percent: int,
    num_flagged: int,
):
    station = StationData()
    station.start_meas = loaded_nasa_ames_example.start_meas
    station.stop_meas = loaded_nasa_ames_example.stop_meas
    station.var_info["bla"] = dict(units="1")
    station.bla = np.ones_like(loaded_nasa_ames_example.start_meas)
    station.ts_type = ts_type

    monkeypatch.setattr("pyaerocom.TsType.TOL_SECS_PERCENT", tol_percent)
    reader._flag_incorrect_frequencies(station)

    assert "bla" in station.data_flagged
    flagged = station.data_flagged["bla"]
    assert flagged.sum() == num_flagged


conco3_tower_var_info = {
    "conco3": {
        "name": "ozone",
        "units": "ug m-3",
        "tower_inlet_height": "50.0 m",
        "measurement_height": "50.0 m",
        "instrument_name": "uv_abs_kre_0050",
        "volume_std._temperature": "293.15 K",
        "volume_std._pressure": "1013.25 hPa",
        "detection_limit": "1.995 ug/m3",
        "comment": "Data converted on import into EBAS from 'nmol/mol' to 'ug/m3' at standard conditions (293.15 K, 1013.25 hPa), conversion factor 1.99534. Variable metadata detection limit converted.",
        "matrix": "air",
        "statistics": "arithmetic mean",
        "ts_type": "hourly",
    }
}
vmro3_tower_var_info = {
    "vmro3": {
        "name": "ozone",
        "units": "nmol mol-1",
        "tower_inlet_height": "50.0 m",
        "measurement_height": "50.0 m",
        "instrument_name": "uv_abs_kre_0050",
        "detection_limit": "1.0 nmol/mol",
        "comment": "Data converted on import into EBAS from 'nmol/mol' to 'ug/m3' at standard conditions (293.15 K, 1013.25 hPa), conversion factor 1.99534. Variable metadata detection limit converted.",
        "matrix": "air",
        "statistics": "arithmetic mean",
        "ts_type": "hourly",
    }
}


@pytest.mark.parametrize(
    "issue_files,vars_to_retrieve,check",
    [
        ("o3_tower", "vmro3", dict(var_info=vmro3_tower_var_info)),
        ("o3_tower", "conco3", dict(var_info=conco3_tower_var_info)),
        ("pm10_tstype", "concpm10", dict(ts_type="2daily")),
        ("Jungfraujoch", ["sc550aer"], dict(station_name="Jungfraujoch")),
    ],
)
def test_read_file(reader: ReadEbas, ebas_issue_files: Path, vars_to_retrieve: str, check: dict):
    data = reader.read_file(ebas_issue_files, vars_to_retrieve)
    assert isinstance(data, StationData)
    for key, val in check.items():
        if isinstance(val, dict):
            for subkey, subval in val.items():
                for subsubkey, subsubval in subval.items():
                    if subsubkey == "comment":
                        assert data[key][subkey][subsubkey].startswith(subsubval)
                    else:
                        assert data[key][subkey][subsubkey] == subsubval
        else:
            assert data[key] == val


@pytest.mark.parametrize(
    "issue_files,vars_to_retrieve,exception,error",
    [
        pytest.param(
            "pm10_colsel",
            "concpm10",
            ValueError,
            "failed to identify unique data column",
            id="repeated column",
        ),
        pytest.param(
            "o3_neg_dt",
            "conco3",
            TemporalResolutionError,
            "Nasa Ames file contains neg. meas periods...",
            id="negative period",
        ),
        pytest.param(
            "o3_tstype",
            "conco3",
            TemporalResolutionError,
            "Failed to derive correct sampling frequency in LT0015R.",
            id="wrong freq",
        ),
    ],
)
def test_read_file_error(
    reader: ReadEbas,
    ebas_issue_files: Path,
    vars_to_retrieve: str,
    exception: type[Exception],
    error: str,
):
    with pytest.raises(exception) as e:
        reader.read_file(ebas_issue_files, vars_to_retrieve)
    assert str(e.value).startswith(error)


def test__try_get_pt_conversion(reader: ReadEbas):
    fname = (
        "CH0001G.19910101000000.20181029122358.uv_abs.ozone.air.1y.1h.CH01L_TEI94C_1.CH01L_O3..nas"
    )
    path = Path(reader.file_dir) / fname
    assert path.exists()

    data = EbasNasaAmesFile(path)
    with pytest.raises(MetaDataError):
        reader._try_get_pt_conversion(data.meta)

    p, T = reader._try_get_pt_conversion(data.var_defs[2])
    assert p == 65300  # Pa
    assert T == 265.15  # K


@pytest.mark.parametrize(
    "vars_to_retrieve,file_vars,num_meta,num_stats",
    [
        ("concno2", "concno2", 2, 2),
        ("vmrno2", "vmrno2", 2, 2),
        ("vmrno2", ["vmrno2", "concno2"], 4, 4),
        ("conco3", "conco3", 4, 4),
        ("vmro3", "conco3", 4, 4),
        ("concpm10", "concpm10", 4, 4),
        ("sc550aer", None, 5, 4),
        ("sc550dryaer", "sc550dryaer", 5, 4),
        ("ac550aer", "ac550aer", 4, 4),
    ],
)
def test_read(
    reader: ReadEbas,
    vars_to_retrieve: list[str] | str,
    ebas_files: list[Path] | None,
    num_meta: int,
    num_stats: int,
):
    data = reader.read(vars_to_retrieve, files=ebas_files)
    assert isinstance(data, UngriddedDataMetadata)
    assert len(data.metadata) == num_meta
    assert len(data.unique_station_names) == num_stats

    if isinstance(vars_to_retrieve, str):
        vars_to_retrieve = [vars_to_retrieve]
    for var in vars_to_retrieve:
        for meta in data.metadata.values():
            assert meta["var_info"][var]["units"] == const.VARS[var].units


@pytest.mark.parametrize("file_vars", ["sc550dryaer"])
def test_read_error(reader: ReadEbas, ebas_files: list[Path]):
    with pytest.raises(DataCoverageError) as e:
        reader.read("ac550aer", files=ebas_files)
    assert str(e.value) == "UngriddedData object appears to be empty"
