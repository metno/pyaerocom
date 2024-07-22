from pyaerocom.colocation.colocation_utils import colocate_gridded_ungridded
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from pyaerocom.ungriddeddata import UngriddedData
from tests.fixtures.data_access import TEST_DATA
from tests.fixtures.stations import create_fake_station_data

ROOT = TEST_DATA["MODELS"].path


def test_read_emep_colocate_projection():
    reader = ReadMscwCtm(data_dir=str(ROOT / "emep4no20240630"))
    data_emep = reader.read_var("concpm10", ts_type="hourly")
    assert isinstance(data_emep, GriddedData)

    S1 = create_fake_station_data(
        "concpm10",
        {"concpm10": {"units": "ug m-3"}},
        1,
        "2024-06-30T23:30:00",
        "2024-07-01T05:30:00",
        "h",
        {"ts_type": "hourly"},
    )
    S1.longitude = 10
    S1.latitude = 60
    S1.station_name = "S1"
    S2 = create_fake_station_data(
        "concpm10",
        {"concpm10": {"units": "ug m-3"}},
        1,
        "2024-06-30T23:30:00",
        "2024-07-01T05:30:00",
        "h",
        {"ts_type": "hourly"},
    )
    S2.longitude = 10.5
    S2.latitude = 60.5
    S2.station_name = "S2"
    ug = UngriddedData.from_station_data([S1, S2])
    colocate_gridded_ungridded(data_emep, ug)
