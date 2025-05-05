import string
from pathlib import Path

import numpy as np
import pytest

from pyaerocom import UngriddedData, ungriddeddata
from pyaerocom.exceptions import DataCoverageError, VariableDefinitionError
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from tests.fixtures.stations import FAKE_STATION_DATA


@pytest.fixture(scope="module")
def ungridded_empty():
    return UngriddedData()


def test_init_shape(ungridded_empty):
    assert ungridded_empty.shape == (10000000, 12)


def test_init_add_cols():
    d1 = UngriddedData(num_points=2, add_cols=["bla", "blub"])
    assert d1.shape == (2, 14)


def test_add_chunk(ungridded_empty):
    ungridded_empty.add_chunk(111002)
    assert ungridded_empty.shape == (20000000, 12)


def test_coordinate_access():
    d = UngriddedData()

    stat_names = list(string.ascii_lowercase)
    lons = np.arange(len(stat_names))
    lats = np.arange(len(stat_names)) - 90
    alts = np.arange(len(stat_names)) * 13

    for i, n in enumerate(stat_names):
        d.metadata[i] = dict(
            data_id="testcase",
            station_name=n,
            latitude=lats[i],
            longitude=lons[i],
            altitude=alts[i],
        )

    assert d.station_name == stat_names
    assert all(d.latitude == lats)
    assert all(d.longitude == lons)
    assert all(d.altitude == alts)

    with pytest.raises(DataCoverageError):
        d.to_station_data("a")

    c = d.station_coordinates
    assert c["station_name"] == stat_names
    assert all(c["latitude"] == lats)
    assert all(c["longitude"] == lons)
    assert all(c["altitude"] == alts)


def test_check_index_aeronet_subset(aeronetsunv3lev2_subset):
    aeronetsunv3lev2_subset._check_index()


@pytest.mark.dependency
def test_check_set_country(aeronetsunv3lev2_subset):
    idx, countries = aeronetsunv3lev2_subset._check_set_country()
    assert len(idx) == len(aeronetsunv3lev2_subset.metadata)
    assert len(countries) == len(idx)
    assert countries == [
        "Italy",
        "Japan",
        "Mali",
        "Brazil",
        "American Samoa",
        "Fr. S. and Antarctic Lands",
        "Republic of Korea",
        "France",
        "Portugal",
        "France",
        "Barbados",
        "United Kingdom",
        "Bolivia",
        "United States",
        "Fr. Polynesia",
        "China",
        "Taiwan",
        "Algeria",
        "Netherlands",
        "Greece",
        "Belgium",
        "Argentina",
    ]
    idx, countries = aeronetsunv3lev2_subset._check_set_country()
    assert idx == []
    assert countries == []


@pytest.mark.dependency(depends=["test_check_set_country"])
def test_countries_available(aeronetsunv3lev2_subset):
    assert aeronetsunv3lev2_subset.countries_available == [
        "Algeria",
        "American Samoa",
        "Argentina",
        "Barbados",
        "Belgium",
        "Bolivia",
        "Brazil",
        "China",
        "Fr. Polynesia",
        "Fr. S. and Antarctic Lands",
        "France",
        "Greece",
        "Italy",
        "Japan",
        "Mali",
        "Netherlands",
        "Portugal",
        "Republic of Korea",
        "Taiwan",
        "United Kingdom",
        "United States",
    ]


@pytest.mark.dependency(depends=["test_check_set_country"])
@pytest.mark.parametrize(
    "region_id,check_mask,check_country_meta,num_meta",
    [("Italy", True, True, 1), ("EUROPE", True, True, 7), ("OCN", True, True, 8)],
)
def test_filter_region(
    aeronetsunv3lev2_subset, region_id, check_mask, check_country_meta, num_meta
):
    subset = aeronetsunv3lev2_subset.filter_region(
        region_id, check_mask=check_mask, check_country_meta=check_country_meta
    )

    assert len(subset.metadata) == num_meta


# sites in aeronet data

ALL_SITES = [
    "AAOT",
    "ARIAKE_TOWER",
    "Agoufou",
    "Alta_Floresta",
    "American_Samoa",
    "Amsterdam_Island",
    "Anmyon",
    "Avignon",
    "Azores",
    "BORDEAUX",
    "Barbados",
    "Blyth_NOAH",
    "La_Paz",
    "Mauna_Loa",
    "Tahiti",
    "Taihu",
    "Taipei_CWB",
    "Tamanrasset_INM",
    "The_Hague",
    "Thessaloniki",
    "Thornton_C-power",
    "Trelew",
]


@pytest.mark.parametrize(
    "args,sitenames",
    [
        ({"station_name": ["Tr*", "Mauna*"]}, ["Trelew", "Mauna_Loa"]),
        (
            {"station_name": ["Tr*", "Mauna*"], "negate": "station_name"},
            [x for x in ALL_SITES if x not in ["Trelew", "Mauna_Loa"]],
        ),
        (
            {"altitude": [0, 1000], "negate": "altitude"},
            ["La_Paz", "Mauna_Loa", "Tamanrasset_INM"],
        ),
        ({"station_name": "Tr*"}, ["Trelew"]),
        (
            {"station_name": "Tr*", "negate": "station_name"},
            [x for x in ALL_SITES if not x == "Trelew"],
        ),
    ],
)
def test_filter_by_meta(aeronetsunv3lev2_subset, args, sitenames):
    data = aeronetsunv3lev2_subset
    subset = data.filter_by_meta(**args)
    sites = [x["station_name"] for x in subset.metadata.values()]
    stats = sorted(list(dict.fromkeys(sites)))
    assert sorted(sitenames) == stats


def test_cache_reload(aeronetsunv3lev2_subset: UngriddedData, tmp_path: Path):
    path = tmp_path / "ungridded_aeronet_subset.pkl"
    file = aeronetsunv3lev2_subset.save_as(file_name=path.name, save_dir=path.parent)
    assert Path(file) == path
    assert path.exists()
    data = UngriddedDataContainer.from_cache(data_dir=path.parent, file_name=path.name)
    assert data.shape == aeronetsunv3lev2_subset.shape


def test_from_single_station_data():
    stat = FAKE_STATION_DATA["station_data1"]
    d = ungriddeddata.UngriddedData.from_station_data(stat)
    data0 = stat.ec550aer
    data1 = d.all_datapoints_var("ec550aer")
    assert data0 == pytest.approx(data1, abs=1e-20)


def test_last_meta_idx(aeronetsunv3lev2_subset: UngriddedData):
    assert isinstance(aeronetsunv3lev2_subset.last_meta_idx, np.ndarray | np.generic)


def test_has_flag_data(aeronetsunv3lev2_subset: UngriddedData):
    assert isinstance(aeronetsunv3lev2_subset.has_flag_data, np.bool_ | bool)


def test_is_filtered(aeronetsunv3lev2_subset: UngriddedData):
    assert isinstance(aeronetsunv3lev2_subset.is_filtered, np.bool_ | bool)


def test_available_meta_keys(aeronetsunv3lev2_subset: UngriddedData):
    assert isinstance(aeronetsunv3lev2_subset.available_meta_keys, list)
    assert all(isinstance(key, str) for key in aeronetsunv3lev2_subset.available_meta_keys)


def test_nonunique_station_names(aeronetsunv3lev2_subset: UngriddedData):
    assert isinstance(aeronetsunv3lev2_subset.nonunique_station_names, list)


def test_set_flags_nan_error(aeronetsunv3lev2_subset: UngriddedData):
    data = aeronetsunv3lev2_subset.copy()
    with pytest.raises(AttributeError):
        data = data.data.set_flags_nan(inplace=True)


def test_remove_outliers(aeronetsunv3lev2_subset: UngriddedData):
    data = aeronetsunv3lev2_subset.copy()
    assert not data.filter_hist
    new = data.remove_outliers(var_name="od550aer", low=0, high=0)
    assert new.filter_hist


def test_extract_var(aeronetsunv3lev2_subset: UngriddedData):
    data = aeronetsunv3lev2_subset.copy()
    od = data.extract_var("od550aer")
    assert not data.is_filtered
    assert od.is_filtered
    assert od.shape[0] < data.shape[0]


def test_extract_var_error(aeronetsunv3lev2_subset: UngriddedData):
    data = aeronetsunv3lev2_subset.copy()
    with pytest.raises(VariableDefinitionError):
        data.extract_var("nope")
