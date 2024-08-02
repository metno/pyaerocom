import numpy as np
import pytest


def test_meta_blocks_ungridded(aeronetsunv3lev2_subset):
    assert len(aeronetsunv3lev2_subset.metadata) == 22
    assert len(aeronetsunv3lev2_subset.unique_station_names) == 22

    names = [
        "AAOT",
        "ARIAKE_TOWER",
        "Agoufou",
        "Alta_Floresta",
        "American_Samoa",
        "Amsterdam_Island",
        "Anmyon",
        "Avignon",
        "Azores",
        "BORDEAUX",
        "Barbados",
        "Blyth_NOAH",
        "La_Paz",
        "Mauna_Loa",
        "Tahiti",
        "Taihu",
        "Taipei_CWB",
        "Tamanrasset_INM",
        "The_Hague",
        "Thessaloniki",
        "Thornton_C-power",
        "Trelew",
    ]
    assert aeronetsunv3lev2_subset.unique_station_names == names


def test_od550aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset.to_station_data_all()["stats"]:
        if "od550aer" not in stat:
            no_odcount += 1
            continue
        td = stat.od550aer[:100]
        mean = np.mean(td)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(td))
    assert no_odcount == 4
    assert np.mean(mean_vals) == pytest.approx(0.2097, abs=1e-2)
    assert np.mean(std_vals) == pytest.approx(0.1397, abs=1e-2)


def test_ang4487aer_meanval_stats(aeronetsunv3lev2_subset):
    no_odcount = 0
    mean_vals = []
    std_vals = []
    for stat in aeronetsunv3lev2_subset.to_station_data_all()["stats"]:
        if "ang4487aer" not in stat:
            no_odcount += 1
            continue
        td = stat.ang4487aer[:100]
        mean = np.mean(td)
        if np.isnan(mean):
            no_odcount += 1
            continue
        mean_vals.append(mean)
        std_vals.append(np.std(td))
    assert no_odcount == 0
    assert np.mean(mean_vals) == pytest.approx(0.9196, abs=1e-2)
    assert np.mean(std_vals) == pytest.approx(0.325, abs=1e-2)
