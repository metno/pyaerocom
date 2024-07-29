import numpy as np
import pandas as pd
import pytest
from scipy.constants import Avogadro

from pyaerocom._warnings import ignore_warnings
from pyaerocom.io.helpers_units import (
    mass_to_nr_molecules,
    nr_molecules_to_mass,
    unitconv_sfc_conc,
    unitconv_sfc_conc_bck,
    unitconv_wet_depo_bck,
    unitconv_wet_depo_from_emep,
)


@pytest.mark.parametrize(
    "mass,nm, result",
    [
        (0, 1, 0),
        (1, 1, Avogadro),
    ],
)
def test_mass_to_nr_molecules(mass, nm, result):
    assert result == mass_to_nr_molecules(mass, nm)


@pytest.mark.parametrize(
    "nr_molecules,mm, result",
    [
        (0, 1, 0),
        (1, Avogadro, 1),
    ],
)
def test_nr_molecules_to_mass(nr_molecules, mm, result):
    assert result == nr_molecules_to_mass(nr_molecules, mm)


@pytest.fixture()
def dummy_data():
    return np.ones(10)


def test_unitconv_sfc_conc_bck(dummy_data):
    result = unitconv_sfc_conc_bck(dummy_data)
    assert len(result) == len(dummy_data)
    assert np.all(result == pytest.approx(0.50050886, 1e-4))


def test_unitconv_sfc_conc(dummy_data):
    result = unitconv_sfc_conc(dummy_data)
    assert len(result) == len(dummy_data)
    assert np.all(result == pytest.approx(1.99796663, 1e-4))


@ignore_warnings(
    FutureWarning,
    "'M' is deprecated and will be removed in a future version, please use 'ME' instead.",
)
# TODO: The above warning is ignored because the old-dependency CI tests don't currently
# support ME. Once we bump dependencies so we can change over, this should be removed.
def test_unitconv_wet_depo_bck(dummy_data):
    time = pd.Series(pd.date_range(start="2000-01-01", periods=len(dummy_data), freq="M"))
    result = unitconv_wet_depo_bck(dummy_data, time)
    assert len(result) == len(
        dummy_data
    )  # sufficent to check length b/c wet depo will change month-to-month


@ignore_warnings(
    FutureWarning,
    "'M' is deprecated and will be removed in a future version, please use 'ME' instead.",
)
# TODO: The above warning is ignored because the old-dependency CI tests don't currently
# support ME. Once we bump dependencies so we can change over, this should be removed.
def test_unitconv_wet_depo_from_emep(dummy_data):
    time = pd.Series(pd.date_range(start="2000-01-01", periods=len(dummy_data), freq="M"))
    result = unitconv_wet_depo_from_emep(dummy_data, time)
    assert len(result) == len(
        dummy_data
    )  # sufficent to check length b/c wet depo will change month-to-month


@ignore_warnings(
    FutureWarning,
    "'M' is deprecated and will be removed in a future version, please use 'ME' instead.",
)
# TODO: The above warning is ignored because the old-dependency CI tests don't currently
# support ME. Once we bump dependencies so we can change over, this should be removed.
def test_unitconv_wet_depo_from_emep_time_not_pandas_series(dummy_data):
    time = pd.date_range(start="2000-01-01", periods=len(dummy_data), freq="M")
    result = unitconv_wet_depo_from_emep(dummy_data, time)
    assert len(result) == len(dummy_data)
