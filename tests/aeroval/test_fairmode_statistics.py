import numpy as np
import pytest
import xarray as xr

# from pyaerocom import ColocatedData, Colocator
from pyaerocom.aeroval import EvalSetup  # , ExperimentProcessor
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.fairmode_statistics import SPECIES, FairmodeStatistics

# from tests.fixtures.aeroval.cfg_test_fairmode import CFG, fairmode_cfg
from tests.fixtures.collocated_data import COLDATA


@pytest.fixture
def fairmode_statistics(patched_config):
    fairmode_statistics = FairmodeStatistics()

    return fairmode_statistics


@pytest.fixture
def fairmode_exp_output(patched_config):
    setup = EvalSetup(**patched_config)
    exp_output = ExperimentOutput(setup)

    assert isinstance(exp_output, ExperimentOutput)

    return exp_output


@pytest.fixture
def dummy_coldata_to_fairmode_statistics():
    example_coldata = COLDATA["tm5_aeronet"]()

    # add fake station_type
    fake_types = ["bla"] * example_coldata.coords["station_name"].shape[0]

    example_coldata.data = example_coldata.data.assign_coords(
        station_type=("station_name", fake_types)
    )

    # rename variable to pretend it's a fairmode species,
    example_coldata.data = example_coldata.data.assign_attrs(var_name=["concno2", "concno2"])

    return example_coldata


@pytest.mark.filterwarnings("ignore:divide by zero encountered in .*divide:RuntimeWarning")
def test_fairmode_statistics(fairmode_statistics, dummy_coldata_to_fairmode_statistics):
    fm_stats = fairmode_statistics.fairmode_statistics(
        dummy_coldata_to_fairmode_statistics, "concno2"
    )

    assert not fm_stats["Agoufou"]["persistence_model"]
    assert fm_stats["Agoufou"]["station_type"] == np.str_("bla")
    assert fm_stats["Agoufou"]["freq"] == "hourly"
    assert all(
        fm_stats["Agoufou"][item] == SPECIES["concno2"][item]
        for item in ["freq", "alpha", "percentile", "RV", "UrRV"]
    )
    assert all(
        item in fm_stats["Agoufou"]
        for item in [
            "obs_mean",
            "mod_std",
            "mod_mean",
            "exceedances_obs",
            "exceedances_mod",
            "NMB",
            "R",
            "RMSU",
            "sign",
            "beta_mqi",
            "Hperc",
            "crms",
            "bias",
            "rms",
        ]
    )


def test_fairmode_statistics_wrongspecies(
    fairmode_statistics, dummy_coldata_to_fairmode_statistics, caplog
):
    wrongspec = "concco"
    example_coldata = dummy_coldata_to_fairmode_statistics
    example_coldata.data = example_coldata.data.assign_attrs(var_name=[wrongspec, wrongspec])

    with pytest.raises(ValueError) as e:
        fairmode_statistics.fairmode_statistics(example_coldata, wrongspec)
    assert f"Unsupported spec='{wrongspec}'" in str(e.value)


@pytest.fixture
def fairmode_stats_example() -> dict:
    return {
        "ALL": {
            "2010-DJF": {
                "Alta_Floresta": {
                    "obs_mean": np.float64(0.3884868563740519),
                    "mod_std": np.float64(0.6060961573280594),
                    "mod_mean": np.float64(0.389367163926363),
                    "exceedances_obs": np.int64(0),
                    "exceedances_mod": np.int64(0),
                    "NMB": np.float64(0.0020848533921114204),
                    "R": np.float64(0.900162558255497),
                    "RMSU": np.float64(9.600056476313366),
                    "sign": [np.float64(1.0)],
                    "crms": np.float64(0.02482145009443063),
                    "bias": np.float64(-0.0593675912149444),
                    "rms": [np.float64(0.064347612787539)],
                    "beta_mqi": [np.float64(0.006702836899585607)],
                    "Hperc": np.float64(0.00965331794743008),
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                },
                "Thessaloniki": {
                    "obs_mean": np.float64(0.18863685117105966),
                    "mod_std": np.float64(0.043870373343254006),
                    "mod_mean": np.float64(0.24130742929198526),
                    "exceedances_obs": np.int64(0),
                    "exceedances_mod": np.int64(0),
                    "NMB": np.float64(0.20555936048513765),
                    "R": np.float64(0.6360611765520063),
                    "RMSU": np.float64(9.600986774272528),
                    "sign": [np.float64(-1.0)],
                    "crms": np.float64(0.4285870343218295),
                    "bias": np.float64(-0.23278371875543458),
                    "rms": [np.float64(0.4877244157374022)],
                    "beta_mqi": [np.float64(0.05079940501994467)],
                    "Hperc": np.float64(0.08138205388790398),
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                },
                "Trelew": {
                    "obs_mean": np.float64(0.0423639675804894),
                    "mod_std": np.float64(0.008299612612318126),
                    "mod_mean": np.float64(0.042434395394391485),
                    "exceedances_obs": np.int64(0),
                    "exceedances_mod": np.int64(0),
                    "NMB": np.float64(0.0013019203413407127),
                    "R": np.float64(-0.26051012045618877),
                    "RMSU": np.float64(9.600004401086988),
                    "sign": [np.float64(-1.0)],
                    "crms": np.float64(0.006734189622538359),
                    "bias": np.float64(0.010339278114124648),
                    "rms": [np.float64(0.012338961941489254)],
                    "beta_mqi": [np.float64(0.0012853079463267891)],
                    "Hperc": np.float64(-0.0009102268365390729),
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                },
            }
        }
    }


def test_save_fairmode_stats(
    fairmode_statistics, fairmode_exp_output, fairmode_stats_example, tmp_path
):
    obs_name = "obsname"
    var_name_web = "name"
    vert_code = "Surface"
    modelname = "modelname"
    model_var = "modelvar"
    fairmode_statistics.save_fairmode_stats(
        fairmode_exp_output,
        fairmode_stats_example,
        obs_name,
        var_name_web,
        vert_code,
        modelname,
        model_var,
    )

    fileout = (
        tmp_path
        / f"{fairmode_exp_output.cfg.proj_id}/{fairmode_exp_output.cfg.exp_id}/fairmode/{list(fairmode_stats_example.keys())[0]}_{obs_name}_{var_name_web}_{vert_code}.json"
    )
    assert fileout.is_file()


def test_exceedances(fairmode_statistics, dummy_coldata_to_fairmode_statistics):
    # reindex fake data hourly and assign new fake values all above threshold (for concno2 threshold is 200)
    start = dummy_coldata_to_fairmode_statistics.data["time"].values[0]
    end = dummy_coldata_to_fairmode_statistics.data["time"].values[-1]
    dummy_coldata_to_fairmode_statistics.data = dummy_coldata_to_fairmode_statistics.data.reindex(
        {"time": xr.date_range(start, end, freq="h")}
    )

    nhours = len(xr.date_range(start, end, freq="h"))
    assert dummy_coldata_to_fairmode_statistics.shape == (2, nhours, 8)
    dummy_coldata_to_fairmode_statistics.data[1] = dummy_coldata_to_fairmode_statistics.data[
        1
    ].where(False, 250.0)
    dummy_coldata_to_fairmode_statistics.data[0] = dummy_coldata_to_fairmode_statistics.data[
        0
    ].where(False, 250.0)
    [exco, excm] = fairmode_statistics._exceedances(
        dummy_coldata_to_fairmode_statistics.data, "concno2"
    )

    assert all(exco == nhours // 24 + 1)
    assert all(excm == nhours // 24 + 1)
