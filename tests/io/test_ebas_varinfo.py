from __future__ import annotations

from configparser import ConfigParser

import pytest

from pyaerocom.io.ebas_file_index import EbasSQLRequest
from pyaerocom.io.ebas_varinfo import EbasVarInfo

TESTDATA = [
    ("DEFAULT", None, None, None, None, None, 1),
    (
        "sc550aer",
        ["aerosol_light_scattering_coefficient"],
        ["aerosol", "pm10"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "sc440aer",
        ["aerosol_light_scattering_coefficient"],
        ["aerosol", "pm10"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "sc700aer",
        ["aerosol_light_scattering_coefficient"],
        ["aerosol", "pm10"],
        None,
        None,
        None,
        1.0,
    ),
    ("sc550dryaer", None, None, None, None, ["sc550aer", "scrh"], 1),
    ("sc440dryaer", None, None, None, None, ["sc440aer", "scrh"], 1),
    ("sc700dryaer", None, None, None, None, ["sc700aer", "scrh"], 1),
    (
        "sc550lt1aer",
        ["aerosol_light_scattering_coefficient"],
        ["pm25", "pm1"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "bsc550aer",
        ["aerosol_light_backscattering_coefficient"],
        ["aerosol", "pm10", "pm25"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "ac550aer",
        ["aerosol_absorption_coefficient"],
        ["aerosol", "pm10"],
        ["filter_absorption_photometer"],
        None,
        None,
        1.0,
    ),
    (
        "ac550dryaer",
        None,
        None,
        ["filter_absorption_photometer"],
        None,
        ["ac550aer", "acrh"],
        1,
    ),
    (
        "ac550lt1aer",
        ["aerosol_absorption_coefficient"],
        ["pm25", "pm1"],
        ["filter_absorption_photometer"],
        None,
        None,
        1.0,
    ),
    (
        "bsc550dryaer",
        ["aerosol_light_backscattering_coefficient"],
        ["pm10", "pm25", "pm1", "aerosol"],
        ["nephelometer"],
        None,
        None,
        1.0,
    ),
    (
        "scrh",
        ["relative_humidity"],
        ["instrument", "aerosol", "met", "pm10", "pm25", "pm1"],
        None,
        None,
        None,
        1,
    ),
    (
        "acrh",
        ["relative_humidity"],
        ["instrument", "aerosol", "met", "pm10", "pm25", "pm1"],
        None,
        None,
        None,
        1,
    ),
    (
        "concso4",
        ["sulphate_corrected", "sulphate_total"],
        ["aerosol", "pm10", "pm25"],
        None,
        None,
        None,
        1,
    ),
    ("concso2", ["sulphur_dioxide"], ["air"], None, None, None, 1.0),
    ("concpm10", ["pm10_mass"], ["pm10"], None, None, None, 1.0),
    ("concpm25", ["pm25_mass"], ["pm25"], None, None, None, 1.0),
    (
        "concso4t",
        ["sulphate_total"],
        ["aerosol", "pm10", "pm25"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "concso4c",
        ["sulphate_corrected"],
        ["aerosol", "pm10", "pm25"],
        None,
        None,
        None,
        1.0,
    ),
    (
        "concbc",
        ["elemental_carbon"],
        ["pm25", "pm10", "pm1", "aerosol"],
        [
            "denuder",
            "ecoc_monitor",
            "filter_1pack",
            "filter_2pack",
            "high_vol_sampler",
            "impactor",
            "low_vol_sampler",
            "lvs_denuder_single",
            "lvs_denuder_tandem",
            "lvs_QBQ",
            "lvs_single",
            "lvs_single_twin",
            "lvs_teflon",
        ],
        ["arithmetic mean", "median"],
        None,
        1.0,
    ),
    (
        "conceqbc",
        ["equivalent_black_carbon"],
        ["aerosol", "pm1", "pm10", "pm25"],
        ["filter_absorption_photometer"],
        None,
        None,
        1,
    ),
    (
        "conctc",
        ["total_carbon"],
        ["pm25", "pm10", "aerosol"],
        None,
        ["arithmetic mean", "median"],
        None,
        1.0,
    ),
    (
        "concoa",
        ["organic_carbon"],
        ["pm25", "pm10", "aerosol", "pm1"],
        None,
        ["arithmetic mean", "median"],
        None,
        1.4,
    ),
    (
        "concoc",
        ["organic_carbon"],
        ["pm25", "pm10", "aerosol", "pm1"],
        None,
        ["arithmetic mean", "median"],
        None,
        1,
    ),
    (
        "concss",
        ["sodium"],
        ["pm10", "aerosol", "pm25", "pm1", "air"],
        None,
        None,
        None,
        3.27,
    ),
    ("concnh3", ["ammonia"], ["air"], None, None, None, 1.0),
    ("concno3", ["nitrate"], ["pm10", "aerosol", "pm25"], None, None, None, 1.0),
    ("concnh4", ["ammonium"], ["pm10", "aerosol", "pm25"], None, None, None, 1.0),
    ("concNhno3", ["nitric_acid"], ["air"], None, None, None, 1.0),
    (
        "concNtno3",
        ["sum_nitric_acid_and_nitrate"],
        ["air+aerosol"],
        None,
        None,
        None,
        1.0,
    ),
    ("concno2", ["nitrogen_dioxide"], ["air"], None, None, None, 1.0),
    ("conco3", ["ozone"], ["air"], None, None, None, 1),
    ("concco", ["carbon_monoxide"], ["air"], None, None, None, 1.0),
    (
        "concprcpoxs",
        ["sulphate_corrected", "sulphate_total"],
        ["precip"],
        None,
        None,
        None,
        1.0,
    ),
    ("concprcpoxn", ["nitrate"], ["precip"], None, None, None, 1.0),
    ("concprcprdn", ["ammonium"], ["precip"], None, None, None, 1.0),
    ("wetoxs", None, None, None, None, ["concprcpoxs"], 1),
    ("wetoxn", None, None, None, None, ["concprcpoxn"], 1),
    ("wetrdn", None, None, None, None, ["concprcprdn"], 1),
    ("wetoxsc", None, None, None, None, ["concprcpoxsc"], 1),
    ("wetoxst", None, None, None, None, ["concprcpoxst"], 1),
    ("wetna", None, None, None, None, ["concprcpna"], 1),
    ("proxydryoxs", None, None, None, None, ["concprcpoxs"], 1),
    ("proxydryoxn", None, None, None, None, ["concprcpoxn"], 1),
    ("proxydryrdn", None, None, None, None, ["concprcprdn"], 1),
    ("proxydryo3", None, None, None, None, ["vmro3"], 1),
    ("wetno3", None, None, None, None, ["concprcpno3"], 1),
    ("wetnh4", None, None, None, None, ["concprcpnh4"], 1),
    ("wetso4", None, None, None, None, ["concprcpso4"], 1),
    (
        "prmm",
        ["precipitation_amount_off", "precipitation_amount"],
        ["precip"],
        None,
        None,
        None,
        1.0,
    ),
]


def test_init_empty():
    with pytest.raises(TypeError) as e:
        EbasVarInfo()
    assert "missing 1 required positional argument" in str(e.value)


def test_open_config():
    assert isinstance(EbasVarInfo.open_config(), ConfigParser)


def test_var_name_aerocom():
    assert EbasVarInfo("sconcno3").var_name_aerocom == "concno3"


@pytest.fixture
def info(var_name: str | None) -> EbasVarInfo:
    if var_name is None:
        info = EbasVarInfo("concpm10")
        info.component = None
        return info
    return EbasVarInfo(var_name)


@pytest.mark.parametrize(
    "var_name,component,matrix,instrument,statistics,requires,scale_factor", TESTDATA
)
def test_varinfo(
    info: EbasVarInfo, component, matrix, instrument, statistics, requires, scale_factor
):
    assert info.component == component
    assert info.matrix == matrix
    assert info.instrument == instrument
    print(info.statistics, statistics, info.statistics == statistics)
    assert info.statistics == statistics
    assert info.requires == requires
    assert info.scale_factor == scale_factor


def test_to_dict():
    info = EbasVarInfo("concpm10")
    dic = info.to_dict()
    assert isinstance(dic, dict)
    for key, val in dic.items():
        assert getattr(info, key) == val


@pytest.mark.parametrize(
    "var_name,constraints",
    [
        ("concpm10", {}),
        ("concpm10", {"bla": 42}),
        # ToDo: the following example should actually be checked and maybe raise an Exception already here
        # (i.e. start_date is a valid constraint but 42 is not allowed as input)
        ("concpm10", {"start_date": 42}),
    ],
)
def test_make_sql_request(info: EbasVarInfo, constraints: dict):
    request = info.make_sql_request(**constraints)
    assert isinstance(request, EbasSQLRequest)


@pytest.mark.parametrize(
    "var_name,exception,error",
    [
        (
            None,
            AttributeError,
            "At least one component (Ebas variable name) must be specified",
        ),
        (
            "sc700dryaer",
            ValueError,
            "This variable sc700dryaer requires other variables for reading",
        ),
        (
            "sc550dryaer",
            ValueError,
            "This variable sc550dryaer requires other variables for reading",
        ),
    ],
)
def test_make_sql_request_error(info: EbasVarInfo, exception: type[Exception], error: str):
    with pytest.raises(exception) as e:
        info.make_sql_request()
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "var_name,num",
    [
        ("concpm10", 1),
        ("sc700dryaer", 2),
        ("sc550dryaer", 2),
        ("sc440dryaer", 2),
    ],
)
def test_make_sql_requests(info: EbasVarInfo, num: int):
    requests = info.make_sql_requests()
    assert isinstance(requests, dict)
    assert len(requests) == num
    assert all(isinstance(req, EbasSQLRequest) for req in requests.values())


def test___str__():
    var_info_str = str(EbasVarInfo("concpm10"))
    assert var_info_str.startswith("\nPyaerocom EbasVarInfo")
    assert "var_name: concpm10" in var_info_str
