"""
High level test methods that check AasEtAl time series data for selected stations
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
from numpy.testing import assert_almost_equal

from pyaerocom import const
from pyaerocom.units import UnitConversionError
from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units.units_helpers import convert_unit
from tests.conftest import lustre_unavail

VARUNITS = {
    "concso2": "ug m-3",
    "concso4": "ug m-3",
    "wetso4": "kg m-2 s-1",
    "concso4pr": "g m-3",
    "pr": "mm",
}

DATA_ID = "GAWTADsubsetAasEtAl"

FILENAMES = ["monthly_so2.csv", "monthly_so4_aero.csv", "monthly_so4_precip.csv"]

VARS = ["concso2", "concso4", "concso4pr", "pr", "wetso4"]


@pytest.fixture
def data_path() -> Path:
    data_dir = const.OBSLOCS_UNGRIDDED[const.GAWTADSUBSETAASETAL_NAME]
    path = Path(data_dir)
    assert path.exists()
    assert path.is_dir()
    return path


@pytest.fixture
def data_paths(data_path: Path) -> list[Path]:
    paths = [data_path / file for file in FILENAMES]
    assert all(path.exists() for path in paths)
    return paths


@lustre_unavail
def test__get_time_stamps(data_paths: list[Path]):
    df = pd.read_csv(data_paths[0], sep=",", low_memory=False)
    reader = ReadAasEtal()
    timestamps = reader._get_time_stamps(df[:10])

    assert str(timestamps[0]) == "1997-09-01T00:00:00"
    assert str(timestamps[-1]) == "1998-09-01T00:00:00"


@lustre_unavail
def test_reader(data_path: Path):
    reader = ReadAasEtal(DATA_ID)
    assert reader.data_id == DATA_ID
    assert reader.data_dir == str(data_path)
    assert reader.PROVIDES_VARIABLES == ["concso2", "concso4", "pr", "wetso4", "concso4pr"]
    filenames = [Path(file).name for file in reader.get_file_list()]
    assert filenames == FILENAMES


@pytest.fixture(scope="session")
def aasetal_data() -> UngriddedData:
    """read expensive dataset"""
    reader = ReadAasEtal()
    return reader.read()


@lustre_unavail
@pytest.mark.xfail(raises=UnitConversionError)
def test_aasetal_data(aasetal_data: UngriddedData):
    data = aasetal_data
    assert len(data.station_name) == 890
    assert len(data.unique_station_names) == 667
    assert data.shape == (416243, 12)
    assert data.contains_vars == VARS
    assert data.contains_instruments == [
        "3_stage_filterpack",
        "passive_sampler",
        "abs_solution",
        "monitor",
        "filter_1pack",
        "filterpack",
        "2_stage_filterpack",
        "filter_denuder_sampler",
        "IMPROVE_PM2.5",
        "filter-1pack",
        "filter_3pack",
        "filter_2pack",
        "pm10_sampler",
        "filter-3pack",
        "wet only",
        "bulk",
        "bulk ",
        "wet-only",
    ]


@lustre_unavail
@pytest.mark.xfail(raises=UnitConversionError)
def test_aasetal_data_correct_units(aasetal_data: UngriddedData):
    tested = []
    stats = []
    for meta_key, meta in aasetal_data.metadata.items():
        for var, info in meta["var_info"].items():
            if var in tested:
                # test each variable only once
                continue
            assert info["units"] == VARUNITS[var]
            tested.append(var)
            stats.append(meta["station_name"])
        if len(tested) == len(VARS):
            break

    assert meta_key == 520
    assert stats == [
        "Abington",
        "Abington",
        "Abington (CT15)",
        "Abington (CT15)",
        "Abington (CT15)",
    ]


# TODO: test wetso4 (needs proper unit conversion)
testdata = [
    (0, "Yellowstone NP", "concentration_ugS/m3", "concso2"),
    (1, "Payerne", "concentration_ugS/m3", "concso4"),
    # (2, 'Abington (CT15)', 'deposition_kgS/ha', 'wetso4')
]


@lustre_unavail
@pytest.mark.parametrize("filenum,station_name,colname,var_name", testdata)
@pytest.mark.xfail(raises=UnitConversionError)
def test_reading_routines(
    aasetal_data: UngriddedData, data_paths: list[Path], filenum, station_name, colname, var_name
):
    UNITCONVERSION = ReadAasEtal().UNITCONVERSION

    df = pd.read_csv(data_paths[filenum], sep=",", low_memory=False)
    subset = df[df.station_name == station_name]
    # values in original units
    vals = subset[colname].astype(float).values
    from_unit, to_unit = UNITCONVERSION[var_name]
    should_be = convert_unit(
        data=vals, from_unit=from_unit, to_unit=to_unit, var_name=var_name
    ).mean()

    actual = aasetal_data.to_station_data(station_name, var_name)[var_name].values.mean()

    if var_name == "wetso4":
        raise NotImplementedError
        # from pyaerocom.helpers import get_tot_number_of_seconds

        # numsecs = get_tot_number_of_seconds(ts_type='monthly',
        #                                    dtime=station_group['dtime'])
        # stat[var] = stat[var]/numsecs
        # to_unit = 'kg m-2 s-1'
    assert_almost_equal(should_be, actual)
