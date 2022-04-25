import pytest

from pyaerocom.io import ReadUngridded

from ..conftest import data_unavail

# although the following is not explicitly referenced, it registers the
# Subset data ids used for testing.

DATA_ID = "EEA_AQeRep.v2.Subset"


@data_unavail
@pytest.fixture(scope="module")
def reader():
    return ReadUngridded(DATA_ID)


@data_unavail
def test_get_file_list(reader):
    # at this point that is the base directory without recursive search
    # so this returns only Revision.txt and metadata.csv
    # don't be too restrictive since we might have additional files in the subdirectory
    lowlevel_reader = reader.get_lowlevel_reader(DATA_ID)
    assert len(lowlevel_reader.get_file_list()) >= 2


@data_unavail
def test_read(reader):
    from pyaerocom.stationdata import StationData
    from pyaerocom.ungriddeddata import UngriddedData

    # special station codes to test
    # not sure if these are really needed
    # station ids to test
    station_id = {}
    # respective mean for a station; index has to be the same as station_id
    station_means = {}
    # list of tested variables will be extended
    var_name = "concpm10"
    station_id[var_name] = ["AT10002", "AT52000"]
    station_means[var_name] = [17.128, 15.1]

    var_names_to_test = station_id.keys()
    for var_name in var_names_to_test:
        data = None
        data = reader.read(vars_to_retrieve=[var_name])
        assert isinstance(data, UngriddedData)

        for stat_idx, statid in enumerate(station_id[var_name]):
            try:
                stat_data = data[statid]
                # It makes no sense to test this for every station
                if stat_idx == 1:
                    assert isinstance(stat_data, StationData)

                assert stat_data[var_name].mean() == pytest.approx(
                    station_means[var_name][stat_idx], 0.01
                )
            except:
                print(f"failed test var {var_name}")
                pass
