from __future__ import annotations
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes
from xarray import DataArray

from pyaerocom.exceptions import (
    CoordinateError,
    DataUnitError,
    MetaDataError,
    VarNotAvailableError,
)
from pyaerocom.units import UnitConversionError
from pyaerocom.io import ReadEarlinet
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from tests.conftest import TEST_RTOL
from tests.fixtures.stations import FAKE_STATION_DATA
from pyaerocom.utils import dicts_equal


def get_earlinet_data(var_name):
    data = ReadEarlinet("Earlinet-test").read(vars_to_retrieve=var_name)
    stats = data.to_station_data_all()["stats"]
    assert len(stats) == 1
    return stats[0]


stat1 = FAKE_STATION_DATA["station_data1"]
stat2 = FAKE_STATION_DATA["station_data2"]


def test_StationData_copy():
    cp = stat1.copy()
    assert dicts_equal(stat1, cp)


stat3 = stat2.copy()
stat3["concno2"] = np.ones(10)
stat3["var_info"]["concno2"] = dict(unit="ug m-3")
stat3["concso4"] = np.ones(10)
stat3["var_info"]["concso4"] = dict(units="1")
stat3["ts_type"] = None
stat3["station_coords"]["latitude"] = "blaaa"
stat4 = stat2.copy()
stat4["longitude"] = "42"

ec_earlinet = get_earlinet_data("ec355aer")


def test_StationData_default_vert_grid():
    grid = stat1.default_vert_grid
    assert grid.mean() == 7375  # m
    step = np.unique(np.diff(grid))
    assert len(step) == 1
    assert step[0] == 250


def test_StationData_vars_available():
    assert stat1.vars_available == ["ec550aer", "od550aer"]


def test_StationData_has_var():
    assert stat1.has_var("od550aer")
    assert stat2.has_var("conco3")
    assert not stat2.has_var("abs550aer")

    copy = stat2.copy()
    copy["abs550aer"] = np.ones(10)
    assert copy.has_var("abs550aer")


def test_StationData_get_unit():
    assert stat1.get_unit("ec550aer") == "m-1"


@pytest.mark.parametrize(
    "stat,var_name,error",
    [
        pytest.param(
            stat1,
            "concco",
            "Could not access variable metadata dict for concco.",
            id="no metadata",
        ),
        pytest.param(
            stat3,
            "concno2",
            "Failed to access units attribute for variable concno2. "
            'Corresponding var_info dict contains attr. "unit", which is deprecated, please check corresponding reading routine. ',
            id="wrong metadata",
        ),
    ],
)
def test_StationData_get_unit_error(stat: StationData, var_name: str, error: str):
    with pytest.raises(MetaDataError) as e:
        stat.get_unit(var_name)
    assert str(e.value) == error


def test_StationData_units():
    assert stat1.units == {"ec550aer": "m-1", "od550aer": "1"}


def test_StationData_check_var_unit_aerocom():
    stat = stat1.copy()
    assert stat.get_unit("ec550aer") == "m-1"

    stat.check_var_unit_aerocom("ec550aer")
    assert stat.get_unit("ec550aer") == "1/km"


@pytest.mark.parametrize(
    "stat,var_name,exception,error",
    [
        pytest.param(
            stat1.copy(),
            "concco",
            MetaDataError,
            "Could not access variable metadata dict for concco.",
            id="var not found",
        ),
        pytest.param(
            stat3.copy(),
            "concso4",
            UnitConversionError,
            "failed to convert unit from 1 to ug m-3",
            id="can not convert",
        ),
    ],
)
def test_StationData_check_var_unit_aerocom_error(
    stat: StationData, var_name: str, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        stat.check_var_unit_aerocom(var_name)
    assert str(e.value) == error


def test_StationData_check_unit():
    stat1._check_unit("ec550aer", "m-1")


def test_StationData_check_unit_error():
    with pytest.raises(DataUnitError) as e:
        stat1._check_unit("ec550aer", None)
    assert str(e.value) == "Invalid unit m-1 (expected 1/km)"


def test_StationData_convert_unit():
    stat2 = deepcopy(stat1)
    stat2.convert_unit("ec550aer", "1/Gm")

    assert stat2["ec550aer"][0] / stat1["ec550aer"][0] == pytest.approx(
        stat2.data_err["ec550aer"][0] / stat1.data_err["ec550aer"][0]
    )


def test_StationData_convert_unit_error():
    with pytest.raises(UnitConversionError) as e:
        stat3.convert_unit("concso4", "kg m-3")
    assert str(e.value) == "failed to convert unit from 1 to kg m-3"


def test_StationData_dist_other():
    dist = stat1.dist_other(stat2)
    assert dist == pytest.approx(1.11, abs=0.1)


@pytest.mark.parametrize(
    "stat,other,tol_km,result",
    [
        (stat1, stat1, None, True),
        (stat1, stat2, 1, False),
        (stat1, stat2, 2, True),
    ],
)
def test_StationData_same_coords(
    stat: StationData, other: StationData, tol_km: float | None, result: bool
):
    assert stat.same_coords(other, tol_km) == result


@pytest.mark.parametrize(
    "stat,force_single_value,dtype",
    [
        (StationData(), False, None),
        (stat1, False, None),
        (stat1, True, float),
        (stat2, True, float),
        (
            StationData(station_coords=dict(latitude=42, longitude=42, altitude=42)),
            False,
            None,
        ),
    ],
)
def test_StationData_get_station_coords(
    stat: StationData, force_single_value: bool, dtype: type | None
):
    coords = stat.get_station_coords(force_single_value=force_single_value)
    assert isinstance(coords, dict)
    if dtype is not None:
        for val in coords.values():
            assert isinstance(val, dtype)


@pytest.mark.parametrize(
    "stat,exception,error",
    [
        pytest.param(
            stat3,
            MetaDataError,
            "Station coordinate latitude must be numeric. Got: blaaa",
            id="wrong station coordinate",
        ),
        pytest.param(
            stat4,
            AttributeError,
            "Invalid value encountered for coord longitude, need float, int, list or ndarray, got <class 'str'>",
            id="wrong station latitude",
        ),
        pytest.param(
            StationData(latitude=[42, 44, 32], longitude=42, altitude=42),
            ValueError,
            "meas point coordinate arrays of latitude vary too much to reduce them to a single coordinate. "
            "Order of difference in latitude is 12 and maximum allowed is 0.05.",
            id="tolerance",
        ),
    ],
)
def test_StationData_get_station_coords_error(
    stat: StationData, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        stat.get_station_coords(force_single_value=True)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "add_none_vals,add_meta_keys,num",
    [
        (False, None, 14),
        (False, "blaaa", 14),
        (False, ["random_key1", "random_key2"], 16),
        (False, ["random_key4"], 15),
        (True, ["random_key4"], 23),
    ],
)
@pytest.mark.parametrize("stat,force_single_value,quality_check", [(stat1, True, True)])
def test_StationData_get_meta(
    stat: StationData,
    force_single_value: bool,
    quality_check: bool,
    add_none_vals: bool,
    add_meta_keys: list[str],
    num: int,
):
    meta = stat.copy().get_meta(
        force_single_value, quality_check, add_none_vals, add_meta_keys=add_meta_keys
    )
    assert isinstance(meta, dict)
    assert len(meta) == num


def test_StationData_get_meta_error():
    with pytest.raises(MetaDataError) as e:
        stat1.copy().get_meta(add_none_vals=False, add_meta_keys=["random_key3"])
    assert str(e.value) == "Inconsistencies in meta parameter random_key3"


@pytest.mark.parametrize("key", ["station_name", "framework", "longitude"])
@pytest.mark.parametrize("stat", [stat1.copy()])
def test_StationData__check_meta_item(stat: StationData, key: str):
    stat._check_meta_item(key)


@pytest.mark.parametrize(
    "other,coord_tol_km,inplace,add_meta_keys",
    [
        (stat1, 0.1, True, None),
        (stat2, 50, True, None),
        (stat2, 50, True, ["random_key1"]),
        (stat2, 50, False, ["random_key1"]),
    ],
)
@pytest.mark.parametrize("stat,check_coords,raise_on_error", [(stat1.copy(), True, True)])
def test_StationData_merge_meta_same_station(
    stat: StationData,
    other: StationData,
    coord_tol_km: float,
    check_coords: bool,
    inplace: bool,
    add_meta_keys: list[str],
    raise_on_error: bool,
):
    _stat = stat.merge_meta_same_station(
        other, coord_tol_km, check_coords, inplace, add_meta_keys, raise_on_error
    )
    assert isinstance(_stat, StationData)
    assert (_stat is stat) == inplace


def test_StationData_merge_meta_same_station_error():
    with pytest.raises(CoordinateError, match="differ by more than 0.001 km."):
        stat1.merge_meta_same_station(
            stat2,
            coord_tol_km=0.001,
            check_coords=True,
            inplace=False,
            raise_on_error=True,
        )


@pytest.mark.parametrize("stat", [stat1.copy(), stat2.copy()])
@pytest.mark.parametrize("other", [stat1, stat2])
def test_StationData_merge_varinfo(stat: StationData, other: StationData):
    assert stat.merge_varinfo(other, "ec550aer") is stat


@pytest.mark.parametrize("stat,other", [(stat1.copy(), stat2), (stat2.copy(), stat1)])
def test_StationData_merge_varinfo_error(stat: StationData, other: StationData):
    with pytest.raises(MetaDataError) as e:
        stat.merge_varinfo(other, "conco3")
    assert str(e.value) == "No variable meta information available for conco3"


@pytest.mark.parametrize(
    "stat,var_name,result",
    [
        (stat1, "od550aer", False),
        (stat2, "od550aer", False),
    ],
)
def test_StationData_check_if_3d(stat: StationData, var_name: str, result: bool):
    assert stat.check_if_3d(var_name) == result


def test_StationData__check_ts_types_for_merge():
    assert stat1.copy()._check_ts_types_for_merge(stat2, "ec550aer") == "monthly"


@pytest.mark.parametrize(
    "low,high,mean",
    [
        (None, None, 1),
        (10, 20, np.nan),
    ],
)
@pytest.mark.parametrize("stat,var_name,check_unit", [(stat1.copy(), "od550aer", True)])
@pytest.mark.filterwarnings("ignore:Mean of empty slice:RuntimeWarning")
def test_StationData_remove_outliers(
    stat: StationData,
    var_name: str,
    low: float | None,
    high: float | None,
    check_unit: bool,
    mean: float,
):
    stat.remove_outliers(var_name, low, high, check_unit)
    avg = np.nanmean(stat[var_name])
    assert avg == pytest.approx(mean, rel=TEST_RTOL, nan_ok=True)


def test_StationData_calc_climatology(aeronetsunv3lev2_subset: UngriddedData):
    site = aeronetsunv3lev2_subset.to_station_data(6, vars_to_convert="od550aer")
    clim = site.calc_climatology("od550aer", clim_freq="daily")
    assert clim is not site
    assert isinstance(clim, StationData)
    mean = np.nanmean(clim.od550aer)  # type:ignore[attr-defined]
    assert mean == pytest.approx(0.44, abs=0.01)


def test_StationData_remove_variable():
    stat = stat1.copy()

    var = "ec550aer"
    assert var in stat
    assert var in stat.var_info

    stat.remove_variable(var)
    assert var not in stat
    assert var not in stat.var_info


def test_StationData_remove_variable_error():
    with pytest.raises(VarNotAvailableError) as e:
        stat1.remove_variable("concco")
    assert str(e.value) == "No such variable in StationData: concco"


def test_StationData_select_altitude_DataArray():
    selection = ec_earlinet.select_altitude("ec355aer", (1000, 2000))
    assert isinstance(selection, DataArray) or isinstance(selection, pd.Series)
    assert selection.shape == (16,)


def test_StationData_select_altitude_DataArray_error():
    with pytest.raises(NotImplementedError) as e:
        ec_earlinet.select_altitude("ec355aer", 1000)
    assert str(e.value) == "So far only a range (low, high) is supported for altitude extraction."


def test_StationData_select_altitude_Series():
    series = stat1.select_altitude("od550aer", (100, 301))
    assert isinstance(series, pd.Series)


@pytest.mark.parametrize(
    "stat,altitudes,exception,error",
    [
        (stat1, (100, 101), ValueError, "no data in specified altitude range"),
        (stat2, (100, 1000), AttributeError, "need 1D altitude array"),
    ],
)
def test_StationData_select_altitude_Series_error(
    stat: StationData,
    altitudes: tuple[int, int],
    exception: type[Exception],
    error: str,
):
    with pytest.raises(exception) as e:
        stat.select_altitude("od550aer", altitudes)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "stat,var_name,kwargs",
    [
        (stat1, "od550aer", dict()),
    ],
)
def test_StationData_to_timeseries(stat: StationData, var_name: str, kwargs: dict):
    series = stat.to_timeseries(var_name, **kwargs)
    assert isinstance(series, pd.Series)


def test_StationData_plot_timeseries():
    ax = stat1.plot_timeseries(var_name="od550aer")
    assert isinstance(ax, Axes)


def test_StationData___str__():
    assert isinstance(str(stat1), str)
