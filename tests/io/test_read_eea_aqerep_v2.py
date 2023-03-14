import pytest

from pyaerocom.io import ReadEEAAQEREP_V2
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from tests.conftest import TEST_RTOL, lustre_avail

# Subset data id used for testing.
DATA_ID = "EEA_AQeRep.v2.Subset"


@pytest.fixture(scope="module")
def reader():
    return ReadEEAAQEREP_V2(DATA_ID)


def test_get_file_list(reader):
    # at this point that is the base directory without recursive search
    # so this returns only Revision.txt and metadata.csv
    # don't be too restrictive since we might have additional files in the subdirectory
    assert len(reader.get_file_list()) >= 2


@lustre_avail
def test_read(reader):
    # special station codes to test
    # not sure if these are really needed
    # station ids to test
    station_id = {}
    # respective mean for a station; index has to be the same as station_id
    station_means = {}
    # list of tested variables will be extended
    var_name = "concpm10"
    # station #3 has in time unordered data
    # station #4 has just one time step
    station_id[var_name] = [
        "AT10002",
        "AT52000",
        "AT90TAB",
        "AT4S418",
    ]
    station_means[var_name] = [
        17.128,
        15.1,
        26.968,
        77.098,
    ]

    var_names_to_test = station_id.keys()
    for var_name in var_names_to_test:
        data = None
        data = reader.read(vars_to_retrieve=[var_name])
        assert isinstance(data, UngriddedData)

        for stat_idx, statid in enumerate(station_id[var_name]):
            stat_data = data[statid]
            # It makes no sense to test this for every station
            if stat_idx == 1:
                assert isinstance(stat_data, StationData)

            assert stat_data[var_name].mean() == pytest.approx(
                station_means[var_name][stat_idx], TEST_RTOL
            )
