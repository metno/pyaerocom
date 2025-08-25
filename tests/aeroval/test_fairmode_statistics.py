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
            "exceedances_obs",
            "MPI_mean",
            "MPI_R_t",
            "MPI_bias_t",
            "MPI_std_t",
            "MPI_R_s",
            "MPI_std_s",
            "MPI_Hperc",
            "fa",
            "ma",
            "gan",
            "gap",
            "bias",
            "NMB",
            "RMSU",
            "sign",
            "beta_mqi",
            "crms",
            "rms",
        ]
    )


def test_fairmode_statistics_wrongspecies(
    fairmode_statistics, dummy_coldata_to_fairmode_statistics
):
    wrongspec = "concco"
    example_coldata = dummy_coldata_to_fairmode_statistics
    example_coldata.data = example_coldata.data.assign_attrs(var_name=[wrongspec, wrongspec])

    with pytest.raises(ValueError) as e:
        fairmode_statistics.fairmode_statistics(example_coldata, wrongspec)
    assert f"Unsupported spec='{wrongspec}'" in str(e.value)


def test_βRMSUt_wrongspecies(fairmode_statistics, dummy_coldata_to_fairmode_statistics):
    obsvals = dummy_coldata_to_fairmode_statistics.data[0]
    wrongspec = "concso2"

    with pytest.raises(ValueError) as e:
        fairmode_statistics._βRMSU_t(obsvals, beta=1, var_name=wrongspec, mask=None)
    assert f"Unsupported spec='{wrongspec}'" in str(e.value)


def test_βRMSUs_wrongspecies(fairmode_statistics, dummy_coldata_to_fairmode_statistics):
    obsvals = dummy_coldata_to_fairmode_statistics.data[0]
    obsmean = np.nanmean(obsvals, axis=0)
    wrongspec = "concso2"

    with pytest.raises(ValueError) as e:
        fairmode_statistics._βRMSU_s(obsmean, beta=1, var_name=wrongspec)
    assert f"Unsupported spec='{wrongspec}'" in str(e.value)


@pytest.fixture
def fairmode_stats_example() -> dict:
    return {
        "ALL": {
            "2010-DJF": {
                "Alta_Floresta": {
                    "exceedances_obs": 0,
                    "MPI_mean": np.float64(0.040463086151092224),
                    "MPI_R_t": np.float64(0.0005913779651058249),
                    "MPI_bias_t": np.float64(9.168897156799856e-05),
                    "MPI_std_t": np.float64(0.01621269226072656),
                    "MPI_R_s": np.float64(0.001440664233921059),
                    "MPI_std_s": np.float64(-0.031303579243870915),
                    "MPI_Hperc": np.float64(0.054898295733501835),
                    "fa": 0,
                    "ma": 0,
                    "gan": 10,
                    "gap": 0,
                    "bias": np.float64(0.0008803075523111548),
                    "NMB": np.float64(0.0020848533921114204),
                    "RMSU": np.float64(9.601018936702271),
                    "sign": [np.float64(1.0)],
                    "crms": np.float64(0.2806109229399387),
                    "rms": [np.float64(0.2806123037476991)],
                    "beta_mqi": [np.float64(0.029227346138750866)],
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                    "Np": 5.2,
                    "Nnp": 5.5,
                },
                "Thessaloniki": {
                    "exceedances_obs": 0,
                    "MPI_mean": np.float64(0.019649444323128436),
                    "MPI_R_t": np.float64(1.910032059129425e-05),
                    "MPI_bias_t": np.float64(0.005486454983897092),
                    "MPI_std_t": np.float64(0.001172539992895984),
                    "MPI_R_s": np.float64(0.001440664233921059),
                    "MPI_std_s": np.float64(-0.031303579243870915),
                    "MPI_Hperc": np.float64(0.0019844616931031385),
                    "fa": 0,
                    "ma": 0,
                    "gan": 11,
                    "gap": 0,
                    "bias": np.float64(0.05267057812092559),
                    "NMB": np.float64(0.20555936048513765),
                    "RMSU": np.float64(9.600111233121442),
                    "sign": [np.float64(-1.0)],
                    "crms": np.float64(0.043440021333975364),
                    "rms": [np.float64(0.06827316642055471)],
                    "beta_mqi": [np.float64(0.0071117057670128615)],
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                    "Np": 5.2,
                    "Nnp": 5.5,
                },
                "Trelew": {
                    "exceedances_obs": 0,
                    "MPI_mean": np.float64(0.004412910794973912),
                    "MPI_R_t": np.float64(2.1497603568997187e-06),
                    "MPI_bias_t": np.float64(7.3362264675617376e-06),
                    "MPI_std_t": np.float64(0.0001217991618271935),
                    "MPI_R_s": np.float64(0.001440664233921059),
                    "MPI_std_s": np.float64(-0.031303579243870915),
                    "MPI_Hperc": np.float64(-0.0005195246019656068),
                    "fa": 0,
                    "ma": 0,
                    "gan": 9,
                    "gap": 0,
                    "bias": np.float64(7.04278139020833e-05),
                    "NMB": np.float64(0.0013019203413407127),
                    "RMSU": np.float64(9.600005426971212),
                    "sign": [np.float64(-1.0)],
                    "crms": np.float64(0.01412406941853019),
                    "rms": [np.float64(0.014124245006952786)],
                    "beta_mqi": [np.float64(0.0014712746898320208)],
                    "persistence_model": False,
                    "station_type": np.str_("bla"),
                    "UrRV": 0.24,
                    "RV": 200,
                    "alpha": 0.2,
                    "freq": "hourly",
                    "percentile": 99.8,
                    "Np": 5.2,
                    "Nnp": 5.5,
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
    period = "2015"
    region = "ALL"
    fairmode_statistics.save_fairmode_stats(
        fairmode_exp_output,
        fairmode_stats_example,
        obs_name,
        var_name_web,
        vert_code,
        modelname,
        model_var,
        period,
        region,
    )

    fileout = (
        tmp_path
        / f"{fairmode_exp_output.cfg.proj_id}/{fairmode_exp_output.cfg.exp_id}/fairmode/{list(fairmode_stats_example.keys())[0]}_{obs_name}_{var_name_web}_{vert_code}_{modelname}_{period}.json"
    )
    assert fileout.is_file()


@pytest.mark.parametrize(
    "var, threshold, freq",
    [
        pytest.param(
            "concno2",
            210.0,
            "h",
            id="no2",
        ),
        pytest.param(
            "concpm10",
            60.0,
            "D",
            id="pm10",
        ),
    ],
)
def test_exceedances(
    fairmode_statistics, dummy_coldata_to_fairmode_statistics, var, threshold, freq
):
    # reindex fake data and assign new fake values all above threshold (for concno2 threshold is 200)
    start = dummy_coldata_to_fairmode_statistics.data["time"].values[0]
    end = dummy_coldata_to_fairmode_statistics.data["time"].values[-1]
    dummy_coldata_to_fairmode_statistics.data = dummy_coldata_to_fairmode_statistics.data.reindex(
        {"time": xr.date_range(start, end, freq=freq)}
    )
    nhours = len(xr.date_range(start, end, freq=freq))  # 335 for concpm10 and 8017 for concno2
    assert dummy_coldata_to_fairmode_statistics.shape == (
        2,
        nhours,
        8,
    )  # dummy coldata has 8 stations
    dummy_coldata_to_fairmode_statistics.data[1] = dummy_coldata_to_fairmode_statistics.data[
        1
    ].where(False, threshold)
    dummy_coldata_to_fairmode_statistics.data[0] = dummy_coldata_to_fairmode_statistics.data[
        0
    ].where(False, threshold)
    [exco, excm] = fairmode_statistics._exceedances(dummy_coldata_to_fairmode_statistics.data, var)
    # concno2 is resampled daily inside the _exceedances function, so the count is 335 for both
    assert all(exco == len(xr.date_range(start, end, freq="D")))
    assert all(excm == len(xr.date_range(start, end, freq="D")))
