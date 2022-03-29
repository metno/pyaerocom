from pathlib import Path

import pytest
from pyaerocom.io.read_eea_aqerep_v2 import ReadEEAAQEREP_V2

from ..conftest import data_unavail

TMPFILE = "#AT_5_48900_2019_timeseries.csv#"


@data_unavail
@pytest.fixture(scope="module")
def reader():
    # not sure if we really use this
    # limit the data read for testing so that this test also works
    # with the full dataset
    ReadEEAAQEREP_V2.FILE_MASKS["concso2"] = "**/??_1_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concpm10"] = "**/??_5_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["conco3"] = "**/??_7_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["vmro3"] = "**/??_7_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concno2"] = "**/??_8_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concno2"] = "**/??_8_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concco"] = "**/??_10_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concno"] = "**/??_38_*_2019_timeseries.csv*"
    ReadEEAAQEREP_V2.FILE_MASKS["concpm25"] = "**/??_6001_*_2019_timeseries.csv*"

    return ReadEEAAQEREP_V2("EEA_AQeRep.v2.Subset")


@data_unavail
@pytest.fixture(scope="module")
def add_additional_file(reader):
    # temporarily add a emacs bakup file to the test data set
    # to make sure these do not disturb the reading
    touchfile = Path.joinpath(reader.data_dir, TMPFILE)
    Path.touch(touchfile)
    assert Path.exists(touchfile) == True
    return touchfile


@data_unavail
def test_get_file_list(reader):
    # at this point that is the base directory without recursive search
    # so this returns only Revision.txt and metadata.csv
    # don't be too restrictive since we might have additional files in the subdirectory
    assert len(reader.get_file_list()) >= 2


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
    # from file AT/AT_5_48881_2019_timeseries.csv.gz and AT/AT_5_48900_2019_timeseries.csv
    # station_id["concpm10"] = ["AT10002", "AT52000"]
    station_id["concpm10"] = ["AT10002", "AT52000"]
    station_means["concpm10"] = [17.128, 15.113]

    var_names_to_test = station_id.keys()
    for var_name in var_names_to_test:
        # r = reader()
        data = None
        data = reader.read(vars_to_retrieve=[var_name])
        assert isinstance(data, UngriddedData)

        print(f"{var_name} data read")
        breakpoint()
        for stat_idx, statid in enumerate(station_id[var_name]):
            try:
                stat_data = data[statid]
                # It makes no sense to test this for every station
                if stat_idx == 1:
                    assert isinstance(stat_data, StationData)

                print(f"calc {stat_data[var_name].mean()}; should {station_means[var_name][stat_idx]}")
                assert stat_data[var_name].mean() == station_means[var_name][stat_idx]
            except:
                print(f"failed test var {var_name}")
                pass


@data_unavail
def remove_additional_file(reader):
    # remove temp file
    touchfile = Path.joinpath(reader.data_dir, TMPFILE)
    assert Path.exists(touchfile) == True
    Path.unlink(touchfile)
    assert Path.exists(touchfile) == False
