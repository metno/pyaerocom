from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom.io.read_eprofile import ReadEprofile


TEST_FILES: list[str] = [
    "/lustre/storeB/project/fou/kl/v-profiles/2025/01/01/AP_0-20000-0-06235-A-2025-01-01.nc",
    "/lustre/storeB/project/fou/kl/v-profiles/2025/01/01/AP_0-20000-0-06240-A-2025-01-01.nc",
]


def test_all_files_exist():
    for file in TEST_FILES:
        assert Path(file).exists()


@pytest.mark.parametrize(
    "vars_to_retrieve",
    [
        (["ec1064aer"], 2),
    ],
)
def test_ReadEarlinet_get_file_list(vars_to_retrieve: list[str] | None):
    reader = ReadEprofile()
    files = reader.get_file_list()
    assert len(files) > 0
