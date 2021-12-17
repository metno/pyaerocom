from pathlib import Path

import numpy as np
from numpy.testing import assert_allclose

from tests.conftest import TEST_RTOL


def test_load_thessaloniki(aeronet_sda_subset_reader):
    reader = aeronet_sda_subset_reader
    files = reader.find_in_file_list("*Thessaloniki*")
    assert len(files) == 1
    assert Path(files[0]).name == "Thessaloniki.lev30"

    test_vars = ["ang4487aer", "od550aer", "od550gt1aer", "od550lt1aer"]

    data = reader.read_file(files[0], vars_to_retrieve=test_vars)

    assert all([x in data for x in test_vars])

    # more than 100 timestamps
    assert all([len(data[x]) > 100 for x in test_vars])

    assert isinstance(data["dtime"][0], np.datetime64)
    assert data["dtime"][0] == np.datetime64("2003-06-01T12:00:00"), data["dtime"][0]

    means = []
    for var in test_vars:
        means.append(np.nanmean(data[var]))

    desired = [1.4777584841303428, 0.1988665578854858, 0.036805761707404114, 0.16206080598741934]

    assert_allclose(actual=means, desired=desired, rtol=TEST_RTOL)
