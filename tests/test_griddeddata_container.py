import iris
import pytest
from copy import deepcopy

from pyaerocom.griddeddata_container import GriddedDataContainer, GriddedDataContainerException
from pyaerocom import GriddedData


def test___init__():
    data_id = "test_id"
    data = GriddedDataContainer(data_id)
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
        "EMEP_split",
    ],
)
def test__initiate(cities_data, model):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    gd = cities_data[model][0]
    mg._initiate(gd)

    assert mg.proj_info == gd.proj_info
    assert mg.start == gd.start


@pytest.mark.parametrize(
    "model",
    [
        "uEMEP",
        "EMEP",
    ],
)
def test_add_griddeddata(cities_data, model):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    for gd in cities_data[model]:
        mg.add_griddeddata(gd)

    assert len(mg.children) == len(cities_data[model])


def test_get_xyranges(cities_data):
    correct_xs = [[3462625, 3495375], [3908625, 3935875]]
    correct_ys = [[2462125, 2486375], [2516625, 2541375]]
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    for gd in cities_data["uEMEP"]:
        mg.add_griddeddata(gd)

    xs, ys = mg.get_xyranges()

    for ls, c_ls in zip(sorted(xs), sorted(correct_xs)):
        for _l, c_l in zip(ls, c_ls):
            assert abs(_l - c_l) < 1e-5

    for ls, c_ls in zip(sorted(ys), sorted(correct_ys)):
        for _l, c_l in zip(ls, c_ls):
            assert abs(_l - c_l) < 1e-5


def test_regrid(cities_data):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    for gd in cities_data["EMEP"]:
        mg.add_griddeddata(gd)

    lat_res = 0.001
    lon_res = 0.001

    for child in mg.children:
        assert child.lat_res != lat_res
        assert child.lon_res != lon_res

    mg.regrid(lat_res_deg=lat_res, lon_res_deg=lon_res)

    for child in mg.children:
        assert child.lat_res == pytest.approx(lat_res, rel=1e-6)
        assert child.lon_res == pytest.approx(lon_res, rel=1e-6)


def test_get_tiles(cities_data):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    for gd in cities_data["uEMEP"]:
        mg.add_griddeddata(gd)

    tiles, xranges, yranges = mg.get_tiles()

    assert len(tiles) == 2
    assert len(tiles) == len(xranges)
    assert len(xranges) == len(yranges)


# Tests for error handling


def test_regrid_fail_due_to_projection(cities_data):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    for gd in cities_data["uEMEP"]:
        mg.add_griddeddata(gd)

    lat_res = 0.001
    lon_res = 0.001

    with pytest.raises(
        GriddedDataContainerException,
        match="Could not regrid, since the data is projected. Please use data with latlon instead",
    ):
        mg.regrid(lat_res_deg=lat_res, lon_res_deg=lon_res)


def test_add_griddeddata_different_model(cities_data):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    emep = cities_data["EMEP"][0]
    uemep = cities_data["uEMEP"][0]

    mg.add_griddeddata(emep)

    with pytest.raises(
        GriddedDataContainerException,
        match="Proj info from added griddeddata and existing proj info do not have the same type*",
    ):
        mg.add_griddeddata(uemep)


@pytest.mark.parametrize(
    "attribute,attr_value",
    [
        ["var_name", "concpm10"],
        ["ts_type", "daily"],
        ["units", "1"],
    ],
)
def test_add_griddeddata_errors(cities_data, attribute, attr_value):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    emep = cities_data["EMEP"][0]
    emep2 = deepcopy(cities_data["EMEP"][1])

    setattr(emep2, attribute, attr_value)

    mg.add_griddeddata(emep)

    with pytest.raises(
        GriddedDataContainerException,
        match=f"{attribute} of added griddeddata*",
    ):
        mg.add_griddeddata(emep2)


@pytest.mark.skip(reason="lat_res currently not working for fine resolution test data")
def test_only_one_child(cities_data):
    data_id = "test_id"
    mg = GriddedDataContainer(data_id)

    mg.add_griddeddata(cities_data["uEMEP"][0])

    lat_res = mg.lat_res

    assert float(lat_res) == pytest.approx(0.00032, rel=0.01)

    mg.add_griddeddata(cities_data["uEMEP"][1])
    with pytest.raises(
        NotImplementedError,
        match="lat_res is not implemented for cases*",
    ):
        lat_res = mg.lat_res


def test_only_one_child_properties(fake_model_data_with_altitude):
    data_id = "test_id_onechild"
    mg = GriddedDataContainer(data_id)

    mg.add_griddeddata(fake_model_data_with_altitude)

    longitude = mg.longitude
    latitude = mg.latitude

    assert longitude.shape == (20,)
    assert latitude.shape == (10,)
    altitude = mg.altitude
    altitude_points = mg.altitude.points
    assert altitude.shape == altitude_points.shape == (10000,)

    data_layer = (
        mg.extract(
            iris.Constraint(coord_values={"altitude": lambda cell: 20000 < cell.point < 30000})
        )
        .collapsed("altitude", iris.analysis.MEAN)
        .copy()
    )
    altitude_points = altitude_points[altitude_points > 20000]
    altitude_points = altitude_points[altitude_points < 30000]
    assert data_layer.altitude_points[0] == pytest.approx(altitude_points.mean(), rel=1e-6)
