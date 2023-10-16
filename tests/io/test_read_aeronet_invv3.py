import re
from pathlib import Path

import numpy as np
import pytest

from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from tests.conftest import TEST_RTOL, lustre_unavail


@lustre_unavail
def test_load_berlin():
    dataset = ReadAeronetInvV3()
    files = dataset.find_in_file_list("*Berlin_FUB*")
    assert len(files) == 1
    assert re.match(r"^19930101_\d{8}_Berlin_FUB.all$", Path(files[0]).name)
    data = dataset.read_file(files[0], vars_to_retrieve=["abs550aer"])

    test_vars = ["abs440aer", "angabs4487aer", "abs550aer"]
    assert all(x in data for x in test_vars)

    # more than 100 timestamps
    assert all(len(data[x]) > 100 for x in test_vars)

    assert isinstance(data["dtime"][0], np.datetime64)
    t0 = data["dtime"][0]

    assert t0 == np.datetime64("2014-07-07T12:00:00")

    first_vals = [np.nanmean(data[var]) for var in test_vars]

    nominal = [0.015538, 0.915505, 0.012879]
    assert first_vals == pytest.approx(nominal, rel=TEST_RTOL)
