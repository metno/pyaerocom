import numpy as np
import pytest
import xarray as xr

from pyaerocom.aeroval import EvalSetup  # , ExperimentProcessor
from pyaerocom.aeroval.fairmode_statistics import SPECIES
from pyaerocom.scripts.cams2_83.engine import CAMS2_83_Engine
from tests.fixtures.collocated_data import COLDATA


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test__calc_forecast_target_MQI_vectorized(eval_config: dict):
    example_coldata = COLDATA["tm5_aeronet"]()

    var_name = "concno2"

    # rename variable to pretend it's a fairmode species
    example_coldata.data = example_coldata.data.assign_attrs(var_name=[var_name, var_name])

    # create dummy persistence model coldata
    example_persistence_coldata = example_coldata

    start = example_persistence_coldata.data["time"].values[0] - np.timedelta64(1, "D")
    end = example_persistence_coldata.data["time"].values[-1]
    example_persistence_coldata.data = example_persistence_coldata.data.reindex(
        {"time": xr.date_range(start, end, freq="h")}
    )

    # set dummy values so that mod_vals will be all 2, obs_vals and p_mod_vals all 1
    # this means that mqi = 1/rmse_persistence and the expected value is just 1.0 / uncertainty_p_obs_val
    p_mod_val = obs_val = 1
    mod_val = 2
    factor = SPECIES[var_name]["alpha"] ** 2 * SPECIES[var_name]["RV"] ** 2
    uncertainty_p_obs_val = SPECIES[var_name]["UrRV"] * np.sqrt(
        (1 - SPECIES[var_name]["alpha"] ** 2) * p_mod_val**2 + factor
    )
    expected_val = 1.0 / uncertainty_p_obs_val

    example_coldata.data[1] = example_coldata.data[1].where(False, mod_val)
    example_coldata.data[0] = example_coldata.data[0].where(False, obs_val)
    example_persistence_coldata.data[0] = example_persistence_coldata.data[0].where(
        False, p_mod_val
    )

    setup = EvalSetup(**eval_config)
    c23engine = CAMS2_83_Engine(setup)

    mqi_vectorized = c23engine._calc_forecast_target_MQI_vectorized(
        example_coldata, example_persistence_coldata, "concno2", 1
    )

    stations_list = example_coldata.coords["station_name"].values.tolist()
    assert len(mqi_vectorized) == len(stations_list)
    for station in stations_list:
        assert len(mqi_vectorized[station]) == 3
        assert mqi_vectorized[station][0].dtype == mqi_vectorized[station][1].dtype == "float64"
        assert (
            np.round(1.0 / mqi_vectorized[station][0], 8)
            == np.round(mqi_vectorized[station][1], 8)
            == np.round(expected_val, 8)
        )
