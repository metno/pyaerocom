from pathlib import Path
import string

import numpy as np
import pytest

from pyaerocom import ungriddeddata
from pyaerocom.exceptions import DataCoverageError, VariableDefinitionError
from pyaerocom.ungridded_data_container import UngriddedDataContainer
from pyaerocom.ungriddeddata_structured import UngriddedDataStructured
from tests.fixtures.stations import FAKE_STATION_DATA


@pytest.fixture(scope="module")
def ungridded_empty():
    return UngriddedDataStructured()


@pytest.fixture(scope="function")
def aeronetsunv3lev2_subset_uds(aeronetsunv3lev2_subset):
    uds = UngriddedDataStructured()
    # convert ungriddeddata to ungriddeddata_structured by merging
    uds.merge(aeronetsunv3lev2_subset, new_obj=False)
    assert not uds.is_empty
    return uds


def test_ungridded_new():
    ud = UngriddedDataStructured(num_points=1000)
    assert ud._dra._capacity == 1000
    assert len(ud._dra._array["meta_id"]) == 1000
    assert len(ud._dra.data["meta_id"]) == 0


def test_coordinate_access():
    d = UngriddedDataStructured()

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
def test_filter_by_meta(aeronetsunv3lev2_subset_uds, args, sitenames):
    data = aeronetsunv3lev2_subset_uds
    assert isinstance(data, UngriddedDataStructured)
    assert data.get_data_revision("AeronetSunV3L2Subset.daily") == "n/d"
    subset = data.filter_by_meta(**args)
    assert subset.get_data_revision("AeronetSunV3L2Subset.daily") == "n/d"
    sites = [x["station_name"] for x in subset.metadata.values()]
    stats = sorted(list(dict.fromkeys(sites)))
    assert sorted(sitenames) == stats


def test_ebas_revision(data_scat_jungfraujoch: UngriddedDataContainer):
    assert isinstance(data_scat_jungfraujoch, UngriddedDataStructured)
    assert data_scat_jungfraujoch.get_data_revision("EBASSubset") == "20220101"


def test_cache_reload(data_scat_jungfraujoch: UngriddedDataContainer, tmp_path: Path):
    path = tmp_path / "ungridded_scat_jungfraujoch.pkl"
    file = data_scat_jungfraujoch.save_as(file_name=path.name, save_dir=path.parent)
    assert Path(file) == path
    assert path.exists()
    data = UngriddedDataContainer.from_cache(data_dir=path.parent, file_name=path.name)
    assert data.shape == data_scat_jungfraujoch.shape


def test_check_unit(data_scat_jungfraujoch):
    data_scat_jungfraujoch.check_unit("sc550aer", unit="1/Mm")
    from pyaerocom.exceptions import MetaDataError

    with pytest.raises(MetaDataError):
        data_scat_jungfraujoch.check_unit("sc550aer", unit="m-1")


def test_from_single_station_data():
    stat = FAKE_STATION_DATA["station_data1"]
    d = ungriddeddata.UngriddedData.from_station_data(stat)
    data0 = stat.ec550aer
    data1 = d.all_datapoints_var("ec550aer")
    assert data0 == pytest.approx(data1, abs=1e-20)


def test_has_flag_data(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    assert isinstance(aeronetsunv3lev2_subset_uds.has_flag_data, np.bool_ | bool)


def test_is_filtered(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    assert isinstance(aeronetsunv3lev2_subset_uds.is_filtered, np.bool_ | bool)


def test_available_meta_keys(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    assert isinstance(aeronetsunv3lev2_subset_uds.available_meta_keys, list)
    assert all(isinstance(key, str) for key in aeronetsunv3lev2_subset_uds.available_meta_keys)


def test_nonunique_station_names(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    assert isinstance(aeronetsunv3lev2_subset_uds.nonunique_station_names, list)


def test_set_flags_nan_error(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    data = aeronetsunv3lev2_subset_uds.copy()
    with pytest.raises(AttributeError):
        data = data.data.set_flags_nan(inplace=True)


def test_remove_outliers(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    data = aeronetsunv3lev2_subset_uds.copy()
    assert not data.filter_hist
    new = data.remove_outliers(var_name="od550aer", low=0, high=0)
    assert new.filter_hist


def test_extract_var(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    data = aeronetsunv3lev2_subset_uds.copy()
    od = data.extract_var("od550aer")
    assert not data.is_filtered
    assert od.is_filtered
    assert od.shape[0] < data.shape[0]


def test_extract_var_error(aeronetsunv3lev2_subset_uds: UngriddedDataStructured):
    data = aeronetsunv3lev2_subset_uds.copy()
    with pytest.raises(VariableDefinitionError):
        data.extract_var("nope")
