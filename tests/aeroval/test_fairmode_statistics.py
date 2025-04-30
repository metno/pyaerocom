import numpy as np
import pytest

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
        for item in ["RMSU", "sign", "beta_mqi", "Hperc", "crms", "bias", "rms"]
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
