from __future__ import annotations

import numpy as np
import pytest

from pyaerocom.combine_vardata_ungridded import (
    _check_input_data_ids_and_vars,
    _combine_2_sites,
    _map_same_stations,
    combine_vardata_ungridded,
)
from tests.fixtures.aeronet import aeronetsdav3lev2_subset as SDA_DATA
from tests.fixtures.aeronet import aeronetsunv3lev2_subset as SUN_DATA

TESTSTAT = "Mauna_Loa"
SUN_ID = "AeronetSunV3L2Subset.daily"
SDA_ID = "AeronetSDAV3L2Subset.daily"
OD450FUN = f"{SUN_ID};od550aer*(450/550)**(-{SUN_ID};ang4487aer)"
FMFFUN = f"fmf550aer=({SDA_ID};od550lt1aer/{SUN_ID};od550aer)*100"


@pytest.fixture(scope="module")
def stats_sun_aod(SUN_DATA):
    return SUN_DATA.to_station_data_all("od550aer")


@pytest.fixture(scope="module")
def stats_sun_ang(SUN_DATA):
    return SUN_DATA.to_station_data_all("ang4487aer")


@pytest.fixture(scope="module")
def stats_sda_aod(SDA_DATA):
    return SDA_DATA.to_station_data_all("od550aer")


@pytest.fixture(scope="module")
def stats_sda_fineaod(SDA_DATA):
    return SDA_DATA.to_station_data_all("od550lt1aer")


@pytest.mark.parametrize(
    "var1,var2,kwargs,numst,mean_first",
    [
        ("od550aer", "ang4487aer", {}, 18, {"od550aer": 0.50155, "ang4487aer": 0.25738}),
        (
            "od550aer",
            "ang4487aer",
            {
                "merge_how": "eval",
                "merge_eval_fun": OD450FUN,
                "var_name_out": "od450aer",
                "var_unit_out": "1",
            },
            18,
            {"od550aer": 0.50155, "ang4487aer": 0.25738, "od450aer": 0.51902},
        ),
    ],
)
def test_combine_vardata_ungridded_single_ungridded(
    SUN_DATA, var1, var2, kwargs, numst, mean_first
):
    input_data = [(SUN_DATA, SUN_ID, var1), (SUN_DATA, SUN_ID, var2)]
    stats = combine_vardata_ungridded(input_data, **kwargs)

    assert len(stats) == numst
    first = stats[0]
    for variable, value in mean_first.items():
        assert variable in first
        assert np.nanmean(first[variable]) == pytest.approx(value, rel=1e-4)


@pytest.mark.parametrize(
    "var1,var2,kwargs,exception,error",
    [
        ("od550aer", "od550aer", {}, ValueError, "nothing to combine"),
        (
            "od550aer",
            "ang4487aer",
            dict(merge_how="mean"),
            NotImplementedError,
            "Averaging of site data is only supported if input variables are the same",
        ),
    ],
)
def test_combine_vardata_ungridded_single_ungridded_error(
    SUN_DATA, var1, var2, kwargs, exception, error
):
    input_data = [(SUN_DATA, SUN_ID, var1), (SUN_DATA, SUN_ID, var2)]
    with pytest.raises(exception) as e:
        combine_vardata_ungridded(input_data, **kwargs)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "merge_how,merge_eval_fun,var_name_out,data_id_out,var_unit_out",
    [
        pytest.param("combine", None, None, None, None, id="combine"),
        pytest.param("eval", FMFFUN, "fmf550aer", None, "%", id="eval fmf550aer"),
        pytest.param("eval", FMFFUN, None, "Bla", "%", id="eval Bla"),
    ],
)
def test__combine_2_sites_different_vars(
    stats_sun_aod,
    stats_sda_fineaod,
    merge_how: str,
    merge_eval_fun: str | None,
    var_name_out: str | None,
    data_id_out: str | None,
    var_unit_out: str | None,
):
    site_idx1 = stats_sun_aod["station_name"].index(TESTSTAT)
    stat1 = stats_sun_aod["stats"][site_idx1]
    var1 = "od550aer"

    site_idx2 = stats_sda_fineaod["station_name"].index(TESTSTAT)
    stat2 = stats_sda_fineaod["stats"][site_idx2]
    var2 = "od550lt1aer"

    new = _combine_2_sites(
        stat1,
        var1,
        stat2,
        var2,
        merge_how=merge_how,
        merge_eval_fun=merge_eval_fun,
        match_stats_tol_km=1,
        var_name_out=var_name_out,
        data_id_out=data_id_out,
        var_unit_out=var_unit_out,
        resample_how="mean",
        min_num_obs=None,
        prefer=f"{SUN_ID};{var1}",
        merge_info_vars={},
        add_meta_keys=None,
    )

    assert var1 in new
    assert var2 in new
    assert len(new[var1]) == len(new[var2])
    assert np.nanmean(new[var1]) == pytest.approx(np.nanmean(stat1[var1]), rel=1e-9)
    assert np.nanmean(new[var2]) == pytest.approx(np.nanmean(stat2[var2]), rel=1e-9)

    if merge_how != "eval":
        return

    if data_id_out is None:
        data_id_out = f"{stat1.data_id};{stat2.data_id}"
    assert new.data_id == data_id_out

    if var_name_out is None:
        assert merge_eval_fun is not None
        var_name_out = merge_eval_fun
        var_name_out = var_name_out.replace(f"{stat1.data_id};", "")
        var_name_out = var_name_out.replace(f"{stat2.data_id};", "")
    assert var_name_out in new

    assert new["var_info"][var_name_out]["units"] == var_unit_out


VALID_DATA_IDS = (
    (SUN_DATA, SUN_ID, "od550aer"),
    (SUN_DATA, SUN_ID, "ang4487aer"),
)


@pytest.mark.parametrize(
    "args,exception,error",
    [
        pytest.param(
            ["Bla"],
            NotImplementedError,
            "Currently, only (and exactly) 2 datasets can be combined...",
            id="only one dataset",
        ),
        pytest.param(
            "Bla",
            ValueError,
            "Input data_ids_and_vars must be tuple or list",
            id="invalid input type",
        ),
        pytest.param(
            (42, VALID_DATA_IDS[1]),
            ValueError,
            "Each entry in data_ids_and_vars must be tuple or list",
            id="invalid dataset description type",
        ),
        pytest.param(
            (VALID_DATA_IDS[0], None),
            ValueError,
            "Each entry in data_ids_and_vars must be tuple or list",
            id="invalid dataset description type",
        ),
        pytest.param(
            [tuple(), VALID_DATA_IDS[1]],
            ValueError,
            "Each entry in data_ids_and_vars needs to contain exactly 3 items.",
            id="incomplete dataset description",
        ),
        pytest.param(
            [VALID_DATA_IDS[0], tuple()],
            ValueError,
            "Each entry in data_ids_and_vars needs to contain exactly 3 items.",
            id="incomplete dataset description",
        ),
        (
            [(SDA_DATA, SUN_ID, None), VALID_DATA_IDS[1]],
            ValueError,
            "2nd and 3rd entries (data_id, var_name) in item need to be str",
        ),
        (
            [VALID_DATA_IDS[0], (SDA_DATA, None, "ang4487aer")],
            ValueError,
            "2nd and 3rd entries (data_id, var_name) in item need to be str",
        ),
    ],
)
def test___check_input_data_ids_and_vars_error(args, exception, error):
    with pytest.raises(exception) as e:
        _check_input_data_ids_and_vars(args)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "match_stats_how,match_stats_tol_km",
    [
        ("station_name", 1),
        ("closest", 0.1),
        ("closest", 1),
        ("closest", 30),
    ],
)
def test__map_same_stations_samedata(stats_sun_aod, match_stats_how, match_stats_tol_km):
    index_short, index_long, statnames_short, statnames_long = _map_same_stations(
        stats_sun_aod, stats_sun_aod, match_stats_how, match_stats_tol_km
    )
    assert index_short == index_long
    assert statnames_short == statnames_long


@pytest.mark.parametrize(
    "match_stats_how,match_stats_tol_km,num_matches,diff_idx",
    [
        ("station_name", 1, 13, 5),
        ("closest", 0.1, 13, 5),
        ("closest", 1, 13, 5),
        ("closest", 30, 13, 5),
    ],
)
def test__map_same_stations(
    stats_sun_aod, stats_sda_aod, match_stats_how, match_stats_tol_km, num_matches, diff_idx
):
    index_short, index_long, statnames_short, statnames_long = _map_same_stations(
        stats_sun_aod, stats_sda_aod, match_stats_how, match_stats_tol_km
    )
    assert len(index_short) == len(index_long) == num_matches
    assert len(statnames_short) == len(statnames_long) == num_matches
    assert sum(short - long for short, long in zip(index_short, index_long)) == diff_idx


@pytest.mark.parametrize(
    "merge_how,merge_eval_fun,var_name_out,data_id_out,var_unit_out",
    [
        pytest.param("combine", None, None, None, None, id="combine"),
        pytest.param("mean", None, None, None, None, id="mean"),
        pytest.param(
            "eval",
            f"od550aer=({SUN_ID};od550aer+{SUN_ID};od550aer)/2",
            "Bla",
            "Blub",
            "1",
            id="eval expensive AOD",
        ),
    ],
)
def test__combine_2_sites_same_site(
    stats_sun_aod,
    merge_how: str,
    merge_eval_fun: str | None,
    var_name_out: str | None,
    data_id_out: str | None,
    var_unit_out: str | None,
):
    site_idx = stats_sun_aod["station_name"].index(TESTSTAT)
    stat = stats_sun_aod["stats"][site_idx]
    var = "od550aer"

    new = _combine_2_sites(
        stat,
        var,
        stat,
        var,
        merge_how=merge_how,
        merge_eval_fun=merge_eval_fun,
        match_stats_tol_km=1,
        var_name_out=var_name_out,
        data_id_out=data_id_out,
        var_unit_out=var_unit_out,
        resample_how="mean",
        min_num_obs=None,
        prefer=f"{SUN_ID};{var}",
        merge_info_vars={},
        add_meta_keys=None,
    )

    if var_name_out is None:
        var_name_out = var
    assert var_name_out in new
    assert var_name_out in new.var_info
    assert len(new[var_name_out]) == len(stat[var].dropna())
    assert new.get_var_ts_type(var_name_out) == stat.get_var_ts_type(var)

    if data_id_out is None:
        data_id_out = SUN_ID
    assert new.data_id == data_id_out

    if var_unit_out is None:
        var_unit_out = stat.get_unit(var)
    assert new.get_unit(var_name_out) == var_unit_out
