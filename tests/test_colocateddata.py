import os

import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from matplotlib.axes import Axes

from pyaerocom import ColocatedData
from pyaerocom.exceptions import DataCoverageError, DataDimensionError

from .conftest import CHECK_PATHS, TESTDATADIR

EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS["coldata_tm5_aeronet"])


@pytest.mark.parametrize(
    "data,kwargs",
    [
        (EXAMPLE_FILE, {}),
        (str(EXAMPLE_FILE), {}),
        (np.ones((2, 3, 4)), {}),
    ],
)
def test_ColocatedData__init__(data, kwargs):
    cd = ColocatedData(data=data, **kwargs)
    assert isinstance(cd.data, xr.DataArray)


@pytest.mark.parametrize(
    "data,kwargs,exception",
    [
        (None, {}, AttributeError),
        ("Blaaaaa", {}, IOError),
        (np.ones(3), {}, DataDimensionError),
        ({}, {}, ValueError),
    ],
)
def test_ColocatedData__init___error(data, kwargs, exception):
    with pytest.raises(exception):
        ColocatedData(data=data, **kwargs).data


@pytest.mark.parametrize("data", [xr.DataArray()])
def test_ColocatedData_data(data):
    col = ColocatedData()
    col.data = data
    assert col.data is data


@pytest.mark.parametrize("data", ["Blaaa"])
def test_ColocatedData_data_error(data):
    col = ColocatedData()
    with pytest.raises(ValueError):
        col.data = data


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_data_source(coldata, which):
    cd = coldata[which]
    ds = cd.data_source
    assert isinstance(ds, xr.DataArray)
    assert len(ds) == 2


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_data_source_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.data_source


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_var_name(coldata, which):
    cd = coldata[which]
    val = cd.var_name
    assert isinstance(val, list)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_var_name_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.var_name


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_latitude(coldata, which):
    cd = coldata[which]
    val = cd.latitude
    assert isinstance(val, xr.DataArray)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_latitude_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.latitude


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_longitude(coldata, which):
    cd = coldata[which]
    val = cd.longitude
    assert isinstance(val, xr.DataArray)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_longitude_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.longitude


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_time(coldata, which):
    cd = coldata[which]
    val = cd.time
    assert isinstance(val, xr.DataArray)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_time_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        val = cd.time


@pytest.mark.parametrize(
    "which,value",
    [
        ("tm5_aeronet", (-43.2, 43.9)),
        ("fake_4d", (30, 50)),
    ],
)
def test_ColocatedData_lat_range(coldata, which, value):
    cd = coldata[which]
    val = cd.lat_range
    assert len(val) == 2
    npt.assert_allclose(val, value, rtol=1e-1)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_lat_range_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.lat_range


@pytest.mark.parametrize(
    "which,value",
    [
        ("tm5_aeronet", (-65.3, 121.5)),
        ("fake_4d", (10, 20)),
    ],
)
def test_ColocatedData_lon_range(coldata, which, value):
    cd = coldata[which]
    val = cd.lon_range
    assert len(val) == 2
    npt.assert_allclose(val, value, rtol=1e-1)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_lon_range_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(AttributeError):
        cd.lon_range


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_ts_type(coldata, which):
    cd = coldata[which]
    val = cd.ts_type
    assert isinstance(val, str)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_ts_type_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(ValueError):
        cd.ts_type


@pytest.mark.parametrize("which", ["tm5_aeronet"])
def test_ColocatedData_units(coldata, which):
    cd = coldata[which]
    val = cd.units
    assert isinstance(val, list)
    assert [isinstance(x, str) for x in val]


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_units_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(KeyError):
        cd.units


@pytest.mark.parametrize(
    "which,result",
    [
        ("fake_4d", 6),
        ("fake_5d", 4),
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
    ],
)
def test_ColocatedData_num_coords(coldata, which, result):
    cd = coldata[which]
    output = cd.num_coords
    assert output == result


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_num_coords_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(DataDimensionError):
        cd.num_coords


@pytest.mark.parametrize(
    "which,result",
    [
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_num_coords_with_data(coldata, which, result):
    cd = coldata[which]
    output = cd.num_coords_with_data
    assert output == result


@pytest.mark.parametrize("which", ["fake_5d", "fake_nodims"])
def test_ColocatedData_num_coords_with_data_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(DataDimensionError):
        cd.num_coords_with_data


@pytest.mark.parametrize(
    "which,num_coords",
    [
        ("tm5_aeronet", 8),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_get_coords_valid_obs(coldata, which, num_coords):
    cd = coldata[which]
    val = cd.get_coords_valid_obs()
    assert isinstance(val, list)
    assert len(val) == 2
    assert len(val[0]) == len(val[1]) == num_coords


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_get_coords_valid_obs_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(ValueError):
        cd.get_coords_valid_obs()


@pytest.mark.parametrize(
    "which,args,chk",
    [
        ("fake_5d", {}, {"num_coords_with_data": np.nan, "num_coords_tot": 4, "totnum": 36}),
        ("tm5_aeronet", {}, {"nmb": -0.129, "R": 0.853}),
        # has random numbers in it so nmb, R check is risky with rtol=1e-2
        ("fake_3d", {}, {"num_coords_with_data": 4}),
        ("fake_4d", {}, {"nmb": 0}),
        ("fake_4d", {"use_area_weights": True}, {"nmb": 0}),
    ],
)
def test_ColocatedData_calc_statistics(coldata, which, args, chk):
    cd = coldata[which]
    output = cd.calc_statistics(**args)
    assert isinstance(output, dict)
    for key, val in chk.items():
        assert key in output
        res = output[key]
        if isinstance(res, str):
            assert res == val
        else:
            npt.assert_allclose(res, val, rtol=1e-2)


@pytest.mark.parametrize("which", ["fake_nodims"])
def test_ColocatedData_calc_statistics_error(coldata, which):
    cd = coldata[which]
    with pytest.raises(DataDimensionError):
        cd.calc_statistics()


@pytest.mark.parametrize(
    "which,args,chk",
    [
        ("fake_5d", {}, {}),
        ("tm5_aeronet", {}, {"nmb": -0.065, "R": 0.679}),
        ("fake_3d", {}, {}),
        ("fake_4d", {}, {"nmb": 0}),
        ("tm5_aeronet", {"aggr": "median"}, {"nmb": -0.0136, "R": 0.851}),
    ],
)
def test_ColocatedData_calc_temporal_statistics(coldata, which, args, chk):
    cd = coldata[which]
    output = cd.calc_temporal_statistics(**args)
    assert isinstance(output, dict)
    for key, val in chk.items():
        assert key in output
        res = output[key]
        if isinstance(res, str):
            assert res == val
        else:
            npt.assert_allclose(res, val, rtol=1e-2)


@pytest.mark.parametrize(
    "which,args,exception",
    [
        ("fake_nodims", {}, DataDimensionError),
        ("tm5_aeronet", {"aggr": "max"}, ValueError),
    ],
)
def test_ColocatedData_calc_temporal_statistics_error(coldata, which, args, exception):
    cd = coldata[which]
    with pytest.raises(exception):
        cd.calc_temporal_statistics(**args)


@pytest.mark.parametrize(
    "which,args,chk",
    [
        ("tm5_aeronet", {}, {"nmb": -0.304, "R": 0.893}),
        ("fake_3d", {}, {}),
        ("fake_4d", {}, {"nmb": 0}),
        ("fake_4d", {"use_area_weights": True}, {"nmb": 0}),
        ("tm5_aeronet", {"aggr": "median"}, {"nmb": -0.42, "R": 0.81}),
    ],
)
def test_ColocatedData_calc_spatial_statistics(coldata, which, args, chk):
    cd = coldata[which]
    output = cd.calc_spatial_statistics(**args)
    assert isinstance(output, dict)
    for key, val in chk.items():
        assert key in output
        res = output[key]
        if isinstance(res, str):
            assert res == val
        else:
            npt.assert_allclose(res, val, rtol=1e-2)


@pytest.mark.parametrize(
    "which,args,exception",
    [
        ("fake_nodims", {}, DataDimensionError),
        ("tm5_aeronet", {"aggr": "max"}, ValueError),
    ],
)
def test_ColocatedData_calc_spatial_statistics_error(coldata, which, args, exception):
    cd = coldata[which]
    with pytest.raises(exception):
        cd.calc_spatial_statistics(**args)


@pytest.mark.parametrize(
    "which,args",
    [
        ("fake_5d", {}),
        ("fake_nodims", {}),
        ("tm5_aeronet", {}),
        ("fake_3d", {}),
        ("fake_4d", {}),
    ],
)
def test_ColocatedData_plot_scatter(coldata, which, args):
    cd = coldata[which]
    output = cd.plot_scatter(**args)
    assert isinstance(output, Axes)


def test_meta_access_filename():
    name = "od550bc_ang4487aer_MOD-AEROCOM-MEDIAN_REF-42AeronET_20000101_20201231_monthly_WORLD-noMOUNTAINS.nc"

    meta = {
        "model_var": "od550bc",
        "obs_var": "ang4487aer",
        "model_name": "AEROCOM-MEDIAN",
        "obs_name": "42AeronET",
        "start": "20000101",
        "stop": "20201231",
        "ts_type": "monthly",
        "filter_name": "WORLD-noMOUNTAINS",
    }

    _meta = ColocatedData.get_meta_from_filename(name)
    assert _meta == meta


def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(EXAMPLE_FILE)
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded


@pytest.mark.parametrize(
    "input_args,latrange,lonrange,numst",
    [
        ({"region_id": "RBU"}, (29.45, 66.26), (22, -170), 2),  # crosses lon=180 border
        ({"region_id": "WORLD"}, (-90, 90), (-180, 180), 8),
        ({"region_id": "NHEMISPHERE"}, (0, 90), (-180, 180), 5),
        ({"region_id": "EUROPE"}, (40, 72), (-10, 40), 2),
        ({"region_id": "OCN"}, (-90, 90), (-180, 180), 8),
    ],
)
def test_apply_latlon_filter(coldata_tm5_aeronet, input_args, latrange, lonrange, numst):
    filtered = coldata_tm5_aeronet.apply_latlon_filter(**input_args)

    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert len(filtered.data.station_name.data) == numst
    if numst > 0:
        assert lats.min() > latrange[0]
        assert lats.max() < latrange[1]
        if lonrange[0] < lonrange[1]:
            assert lons.min() > lonrange[0]
            assert lons.max() < lonrange[1]
        else:
            assert -180 < lons.min() < lonrange[1] or lonrange[0] < lons.min() < 180
            assert -180 < lons.max() < lonrange[1] or lonrange[0] < lons.max() < 180


@pytest.mark.parametrize(
    "input_args",
    [
        {"region_id": "PAN"},  # crosses lon=180 border
        {"region_id": "NAM"},  # crosses lon=180 border
    ],
)
def test_apply_latlon_filter_error(coldata_tm5_aeronet, input_args):
    with pytest.raises(DataCoverageError):
        coldata_tm5_aeronet.apply_latlon_filter(**input_args)


@pytest.mark.parametrize(
    "which,input_args,latrange,lonrange,numst",
    [
        ("fake_4d", {"region_id": "EUROPE"}, (40, 72), (-10, 40), 4),
        ("tm5_aeronet", {"region_id": "NHEMISPHERE"}, (0, 90), (-180, 180), 5),
        ("tm5_aeronet", {"region_id": "EUROPE"}, (40, 72), (-10, 40), 2),
        ("tm5_aeronet", {"region_id": "OCN"}, (-59.95, 66.25), (-132.55, 119.95), 1),
        (
            "tm5_aeronet",
            {"region_id": "Brazil", "check_country_meta": True},
            (-59.95, 66.25),
            (-132.55, 119.95),
            1,
        ),
    ],
)
def test_ColocatedData_filter_region(coldata, which, input_args, latrange, lonrange, numst):
    cd = coldata[which]
    if "check_country_meta" in input_args:
        cd = cd.copy()
        cd.check_set_countries()

    filtered = cd.filter_region(**input_args)
    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert lats.min() >= latrange[0]
    assert lats.max() <= latrange[1]
    assert lons.min() >= lonrange[0]
    assert lons.max() <= lonrange[1]
    assert filtered.num_coords == numst


@pytest.mark.parametrize(
    "which,input_args", [("fake_4d", {"region_id": "France", "check_country_meta": True})]
)
def test_ColocatedData_filter_region_error(coldata, which, input_args):
    cd = coldata[which]
    with pytest.raises(DataDimensionError):
        if "check_country_meta" in input_args:
            cd = cd.copy()
            cd.check_set_countries()
        cd.filter_region(**input_args)


@pytest.mark.parametrize(
    "which,filename",
    [
        (
            "tm5_aeronet",
            "od550aer_od550aer_MOD-TM5_AP3-CTRL2016_REF-AeronetSunV3L2Subset.daily_20100115_20101215_monthly_WORLD-noMOUNTAINS.nc",
        ),
        (
            "fake_3d_hr",
            "vmro3_vmro3_MOD-fakemod_REF-fakeobs_20180110_20180117_hourly_WORLD-wMOUNTAINS.nc",
        ),
        (
            "fake_3d",
            "concpm10_concpm10_MOD-fakemod_REF-fakeobs_20000115_20191215_monthly_WORLD-wMOUNTAINS.nc",
        ),
    ],
)
def test_ColocatedData_to_netcdf(coldata, tempdir, which, filename):
    cd = coldata[which]
    fp = cd.to_netcdf(tempdir)
    assert os.path.exists(fp)
    assert os.path.basename(fp) == filename


@pytest.mark.parametrize(
    "filename",
    [
        "od550aer_od550aer_MOD-TM5_AP3-CTRL2016_REF-AeronetSunV3L2Subset.daily_20100115_20101215_monthly_WORLD-noMOUNTAINS.nc",
        "vmro3_vmro3_MOD-fakemod_REF-fakeobs_20180110_20180117_hourly_WORLD-wMOUNTAINS.nc",
        "concpm10_concpm10_MOD-fakemod_REF-fakeobs_20000115_20191215_monthly_WORLD-wMOUNTAINS.nc",
    ],
)
def test_ColocatedData_read_netcdf(tempdir, filename):
    fp = os.path.join(tempdir, filename)
    assert os.path.exists(fp)
    cd = ColocatedData().read_netcdf(fp)
    assert isinstance(cd, ColocatedData)


@pytest.mark.parametrize(
    "which,args,mean",
    [
        ("tm5_aeronet", dict(to_ts_type="yearly"), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", min_num_obs=14), np.nan),
        ("tm5_aeronet", dict(to_ts_type="yearly", settings_from_meta=True), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", colocate_time=True), 0.363),
    ],
)
def test_ColocatedData_resample_time(coldata, which, args, mean):
    cd = coldata[which]
    cd1 = cd.resample_time(**args)
    avg = cd1.data.mean().data
    if np.isnan(mean):
        assert np.isnan(avg)
    else:
        npt.assert_allclose(avg, mean, atol=1e-3)

    if "inplace" in args:
        assert cd1 is cd
    else:
        assert cd1 is not cd
