from pathlib import Path

import numpy as np
import pytest

from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from tests.conftest import TEST_RTOL, lustre_unavail


@lustre_unavail
def test_load_berlin():
    dataset = ReadAeronetInvV3()
    files = dataset.find_in_file_list("*Berlin*")
    assert len(files) == 1
    assert Path(files[0]).name == "19930101_20220416_Berlin_FUB.all"
    data = dataset.read_file(files[0], vars_to_retrieve=["abs550aer"])

    test_vars = ["abs440aer", "angabs4487aer", "abs550aer"]
    assert all(x in data for x in test_vars)

    # more than 100 timestamps
    assert all(len(data[x]) > 100 for x in test_vars)

    assert isinstance(data["dtime"][0], np.datetime64)
    t0 = data["dtime"][0]

    assert t0 == np.datetime64("2014-07-07T12:00:00")

    first_vals = [np.nanmean(data[var]) for var in test_vars]

    nominal = [0.014609, 0.876344, 0.012291]
    assert first_vals == pytest.approx(nominal, rel=TEST_RTOL)
