import pytest

from pyaerocom.multigriddeddata import MultiGriddedData, MultiGriddedDataException
from pyaerocom import GriddedData
from tests.fixtures.multigriddeddata import path_emep, path_uemep, cities_data


def test___init__():
    data_id = "test_id"
    data = MultiGriddedData(data_id)
    assert data.data_id == data_id


def test_fixture(cities_data):
    for model in ["uEMEP", "EMEP"]:
        data = cities_data[model]
        for city in data:
            assert isinstance(city, GriddedData)


@pytest.mark.parametrize(
    "model",
    [
        "uEMEP",
        "EMEP",
    ],
)
def test__initiate(cities_data, model):
    data_id = "test_id"
    mg = MultiGriddedData(data_id)

    gd = cities_data[model][0]
    mg._initiate(gd)

    assert mg.proj_info == gd.proj_info
    assert mg.start == gd.start
    assert mg.latitude == gd.latitude


@pytest.mark.parametrize(
    "model",
    [
        "uEMEP",
        "EMEP",
    ],
)
def test_add_griddeddata(cities_data, model):
    data_id = "test_id"
    mg = MultiGriddedData(data_id)

    for gd in cities_data[model]:
        mg.add_griddeddata(gd)

    assert len(mg.children) == len(cities_data[model])


def test_get_latlon_ranges(cities_data):

    correct_lats = [[51.05, 52.95], [51.05, 52.95]]
    correct_lons = [[4.05, 5.95], [12.05, 13.95]]
    data_id = "test_id"
    mg = MultiGriddedData(data_id)

    for gd in cities_data["EMEP"]:
        mg.add_griddeddata(gd)

    lats, lons = mg.get_latlon_ranges()

    
    for ls, c_ls in zip(sorted(lats), sorted(correct_lats)):
        for l, c_l in zip(ls, c_ls):
            assert abs(l-c_l) < 1e-5

    for ls, c_ls in zip(sorted(lons), sorted(correct_lons)):
        for l, c_l in zip(ls, c_ls):
            assert abs(l-c_l) < 1e-5


# Tests for error handling

def test_add_griddeddata_error(cities_data):
    data_id = "test_id"
    mg = MultiGriddedData(data_id)

    emep = cities_data["EMEP"][0]
    uemep = cities_data["uEMEP"][0]
    
    mg.add_griddeddata(emep)

    with pytest.raises(MultiGriddedDataException, match="Proj info from added griddeddata and existing proj info do not have the same type*") as e:
        mg.add_griddeddata(uemep)
