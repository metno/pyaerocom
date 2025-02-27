import iris
import numpy as np
import pandas as pd
import pytest
from cf_units import Unit

from pyaerocom import GriddedData, const, helpers
from pyaerocom.colocation.colocated_data import ColocatedData
from pyaerocom.colocation.colocation_utils import (
    _colocate_site_data_helper,
    _colocate_site_data_helper_timecol,
    _regrid_gridded,
    colocate_gridded_gridded,
    colocate_gridded_ungridded,
)
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import UnresolvableTimeDefinitionError
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from tests.conftest import TEST_RTOL, need_iris_32
from tests.fixtures.stations import create_fake_station_data


def test__regrid_gridded(data_tm5):
    one_way = _regrid_gridded(data_tm5, "areaweighted", 5)
    another_way = _regrid_gridded(data_tm5, "areaweighted", dict(lon_res_deg=5, lat_res_deg=5))

    assert one_way.shape == another_way.shape


S1 = create_fake_station_data(
    "concpm10",
    {"concpm10": {"units": "ug m-3"}},
    10,
    "2010-01-01",
    "2010-12-31",
    "d",
    {"ts_type": "daily"},
)

S1["concpm10"][10:20] = np.nan

S2 = create_fake_station_data(
    "concpm10",
    {"concpm10": {"units": "ug m-3"}},
    10,
    "2010-01-01",
    "2010-12-31",
    "d",
    {"ts_type": "daily"},
)

S3 = create_fake_station_data(
    "concpm10",
    {"concpm10": {"units": "ug m-3"}},
    10,
    "2010-01-01",
    "2010-12-31",
    "13d",
    {"ts_type": "13daily"},
)
S3["concpm10"][1] = np.nan
S3["concpm10"][3] = np.nan

S4 = create_fake_station_data(
    "concpm10",
    {"concpm10": {"units": "ug m-3"}},
    10,
    "2010-01-03",
    "2011-12-31",
    "d",
    {"ts_type": "daily"},
)

S4["concpm10"][0:5] = range(5)


@pytest.mark.parametrize(
    "stat_data,stat_data_ref,var,var_ref,ts_type,resample_how,min_num_obs, use_climatology_ref,num_valid",
    [
        (
            S4,
            S3,
            "concpm10",
            "concpm10",
            "monthly",
            "mean",
            {"monthly": {"daily": 25}},
            False,
            10,
        ),
        (
            S3,
            S4,
            "concpm10",
            "concpm10",
            "monthly",
            "mean",
            {"monthly": {"daily": 25}},
            False,
            24,
        ),
        (S1, S2, "concpm10", "concpm10", "monthly", "mean", 25, {}, 12),
        (S2, S1, "concpm10", "concpm10", "monthly", "mean", 25, {}, 11),
    ],
)
def test__colocate_site_data_helper_timecol(
    stat_data,
    stat_data_ref,
    var,
    var_ref,
    ts_type,
    resample_how,
    min_num_obs,
    use_climatology_ref,
    num_valid,
):
    result = _colocate_site_data_helper_timecol(
        stat_data,
        stat_data_ref,
        var,
        var_ref,
        ts_type,
        resample_how,
        min_num_obs,
        use_climatology_ref,
    )

    assert isinstance(result, pd.DataFrame)
    assert result.data.isnull().sum() == result.ref.isnull().sum()
    assert len(result) - result.data.isnull().sum() == num_valid


def test__colocate_site_data_helper(aeronetsunv3lev2_subset):
    var = "od550aer"
    stat1 = aeronetsunv3lev2_subset.to_station_data(3, var)
    stat2 = aeronetsunv3lev2_subset.to_station_data(4, var)
    df = _colocate_site_data_helper(stat1, stat2, var, var, "daily", None, None, False)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 9483
    assert df["data"].mean() == pytest.approx(0.31171085422102346, rel=TEST_RTOL)
    assert df["ref"].mean() == pytest.approx(0.07752743643132792, rel=TEST_RTOL)


def test_colocate_gridded_ungridded_new_var(data_tm5, aeronetsunv3lev2_subset):
    data = data_tm5.copy()
    data.var_name = "od550bc"
    coldata = colocate_gridded_ungridded(data, aeronetsunv3lev2_subset, var_ref="od550aer")

    assert coldata.metadata["var_name"] == ["od550aer", "od550bc"]


@pytest.mark.parametrize(
    "addargs,ts_type,shape,obsmean,modmean",
    [
        (
            dict(
                filter_name=f"{ALL_REGION_NAME}-noMOUNTAINS",
                min_num_obs=const.OBS_MIN_NUM_RESAMPLE,
            ),
            "monthly",
            (2, 12, 8),
            0.315930,
            0.275671,
        ),
        (
            dict(filter_name=f"{ALL_REGION_NAME}-noMOUNTAINS"),
            "monthly",
            (2, 12, 8),
            0.316924,
            0.275671,
        ),
        (
            dict(
                filter_name=f"{ALL_REGION_NAME}-wMOUNTAINS",
                min_num_obs=const.OBS_MIN_NUM_RESAMPLE,
            ),
            "monthly",
            (2, 12, 11),
            0.269707,
            0.243861,
        ),
        pytest.param(
            dict(
                filter_name=f"{ALL_REGION_NAME}-noMOUNTAINS",
                regrid_res_deg=30,
                min_num_obs=const.OBS_MIN_NUM_RESAMPLE,
            ),
            "monthly",
            (2, 12, 8),
            0.31593,
            # 0.1797,
            0.169897,
            marks=[need_iris_32],
        ),
        (
            dict(filter_name=f"{ALL_REGION_NAME}-noMOUNTAINS", ts_type="yearly"),
            "yearly",
            (2, 1, 8),
            0.417676,
            0.275671,
        ),
    ],
)
def test_colocate_gridded_ungridded(
    data_tm5, aeronetsunv3lev2_subset, addargs, ts_type, shape, obsmean, modmean
):
    coldata = colocate_gridded_ungridded(data_tm5, aeronetsunv3lev2_subset, **addargs)

    assert isinstance(coldata, ColocatedData)
    assert coldata.ts_type == ts_type
    assert coldata.shape == shape

    assert np.nanmean(coldata.data.data[0]) == pytest.approx(obsmean, rel=TEST_RTOL)
    assert np.nanmean(coldata.data.data[1]) == pytest.approx(modmean, rel=TEST_RTOL)


def test_colocate_gridded_ungridded_wstationtype(data_tm5, aeronetsunv3lev2_subset):
    fake_type = ["faketype"] * len(aeronetsunv3lev2_subset.station_name)
    for i, n in enumerate(fake_type):
        aeronetsunv3lev2_subset.metadata[i].update({"station_type": n})
    coldata = colocate_gridded_ungridded(
        data_tm5, aeronetsunv3lev2_subset, add_meta_keys=["station_type"]
    )
    assert all(typ == "faketype" for typ in coldata.coords["station_type"].values.tolist())


def test_colocate_gridded_ungridded_nonglobal(aeronetsunv3lev2_subset):
    times = [1, 2]
    time_unit = Unit("days since 2010-1-1 0:0:0")
    cubes = iris.cube.CubeList()

    for time in times:
        time_coord = iris.coords.DimCoord(time, units=time_unit, standard_name="time")
        cube = helpers.make_dummy_cube_latlon(
            lat_res_deg=1,
            lon_res_deg=1,
            lat_range=[30.05, 81.95],
            lon_range=[-29.5, 89.95],
        )
        cube.add_aux_coord(time_coord)
        cubes.append(cube)
    time_cube = cubes.merge_cube()
    gridded = GriddedData(time_cube)
    gridded.var_name = "od550aer"
    gridded.units = Unit("1")

    coldata = colocate_gridded_ungridded(gridded, aeronetsunv3lev2_subset, colocate_time=False)
    assert isinstance(coldata, ColocatedData)
    assert coldata.shape == (2, 2, 2)


def test_colocate_gridded_gridded_same_new_var(data_tm5):
    data = data_tm5.copy()
    data.var_name = "Blaaa"
    coldata = colocate_gridded_gridded(data, data_tm5)

    assert coldata.metadata["var_name"] == ["od550aer", "Blaaa"]


def test_colocate_gridded_gridded_same(data_tm5):
    coldata = colocate_gridded_gridded(data_tm5, data_tm5)

    assert isinstance(coldata, ColocatedData)
    stats = coldata.calc_statistics()
    # check mean value
    assert stats["data_mean"] == pytest.approx(0.09825691)
    # check that mean value is same as in input GriddedData object
    assert stats["data_mean"] == pytest.approx(data_tm5.mean(areaweighted=False))
    assert stats["refdata_mean"] == stats["data_mean"]
    assert stats["nmb"] == 0
    assert stats["mnmb"] == 0
    assert stats["R"] == pytest.approx(1, rel=1e-6)
    assert stats["R_spearman"] == pytest.approx(1, rel=1e-6)


@pytest.mark.xfail(raises=UnresolvableTimeDefinitionError)
def test_read_emep_colocate_emep_tm5(data_tm5, path_emep):
    reader = ReadMscwCtm(data_dir=path_emep["data_dir"])
    data_emep = reader.read_var("concpm10", ts_type="monthly")

    # Change units and year to match TM5 data
    data_emep.change_base_year(2010)
    data_emep.units = "1"

    col = colocate_gridded_gridded(data_emep, data_tm5)
    assert isinstance(col, ColocatedData)
