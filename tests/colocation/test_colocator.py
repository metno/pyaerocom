import string
from pathlib import Path

import numpy as np
import pytest
from pydantic import ValidationError

from pyaerocom import ColocatedData, GriddedData, UngriddedData, const
from pyaerocom.climatology_config import ClimatologyConfig
from pyaerocom.colocation.colocation_setup import ColocationSetup
from pyaerocom.colocation.colocator import Colocator
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import ColocationError, ColocationSetupError
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from tests.fixtures.data_access import TEST_DATA

COL_OUT_DEFAULT = Path(const.OUTPUTDIR) / "colocated_data"

default_setup = {
    "model_id": None,
    "obs_id": None,
    "obs_vars": (),
    "ts_type": "monthly",
    "start": None,
    "stop": None,
    "filter_name": f"{ALL_REGION_NAME}-wMOUNTAINS",
    "basedir_coldata": COL_OUT_DEFAULT,
    "save_coldata": False,
    "obs_name": None,
    "obs_data_dir": None,
    "obs_use_climatology": False,
    "obs_cache_only": False,
    "obs_vert_type": None,
    "obs_ts_type_read": None,
    "obs_filters": {},
    "model_name": None,
    "model_data_dir": None,
    "model_read_opts": {},
    "read_opts_ungridded": {},
    "model_use_vars": {},
    "model_rename_vars": {},
    "model_add_vars": {},
    "model_to_stp": False,
    "model_ts_type_read": None,
    "model_read_aux": {},
    "model_use_climatology": False,
    "gridded_reader_id": {"model": "ReadGridded", "obs": "ReadGridded"},
    "flex_ts_type": True,
    "min_num_obs": None,
    "resample_how": "mean",
    "obs_remove_outliers": False,
    "model_remove_outliers": False,
    "zeros_to_nan": False,
    "obs_outlier_ranges": {},
    "model_outlier_ranges": {},
    "harmonise_units": False,
    "regrid_res_deg": None,
    "colocate_time": False,
    "reanalyse_existing": True,
    "raise_exceptions": False,
    "keep_data": True,
    "add_meta": {},
}


@pytest.fixture(scope="function")
def setup():
    return dict(
        model_id="TM5-met2010_CTRL-TEST",
        obs_id="AeronetSunV3L2Subset.daily",
        obs_vars="od550aer",
        start=2010,
        raise_exceptions=True,
        reanalyse_existing=True,
    )


@pytest.fixture(scope="function")
def tm5_aero_col_stp(setup):
    return ColocationSetup(**setup)


@pytest.fixture(scope="function")
def col(tm5_aero_col_stp):
    col = Colocator(tm5_aero_col_stp, raise_exceptions=True, reanalyse_existing=True)
    return col


@pytest.mark.parametrize("col_stp,should_be", [(ColocationSetup(), default_setup)])
def test_colocation_setup(col_stp: ColocationSetup, should_be: dict):
    stp_dict = col_stp.model_dump()
    for key, val in should_be.items():
        assert key in stp_dict
        if key == "basedir_coldata":
            assert Path(val) == Path(stp_dict["basedir_coldata"])
        else:
            assert val == stp_dict[key], key


@pytest.mark.parametrize(
    "key,val,raises",
    [
        ("obs_vars", 42, pytest.raises(ValidationError)),
        ("var_ref_outlier_ranges", [41, 42], pytest.raises(KeyError)),
        ("var_outlier_ranges", [41, 42], pytest.raises(KeyError)),
        ("remove_outliers", True, pytest.raises(KeyError)),
    ],
)
def test_ColocationSetup_invalid_input(key, val, raises):
    with raises:
        stp = ColocationSetup(**{key: val})
        assert stp.model_dump()[key] == val


@pytest.mark.parametrize("ts_type_desired", ["daily", "monthly"])
@pytest.mark.parametrize("ts_type", ["monthly"])
@pytest.mark.parametrize("flex", [False, True])
def test_Colocator_model_ts_type_read(setup, ts_type_desired, ts_type, flex):
    obs_var = "od550aer"
    setup["model_ts_type_read"] = {obs_var: ts_type_desired}
    setup.update(dict(ts_type=ts_type, flex=flex))
    assert setup["obs_vars"] == obs_var
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    # Problem with saving since obs_id is different
    # from obs_data.contains_dataset[0]...
    data = col.run()
    assert isinstance(data, dict)
    assert obs_var in data
    coldata = data[obs_var][obs_var]
    assert coldata.ts_type == ts_type
    assert coldata.metadata["ts_type_src"][0] == "daily"
    if not flex:
        assert coldata.metadata["ts_type_src"][1] == ts_type_desired


def test_Colocator_model_ts_type_read_error(setup):
    setup["model_ts_type_read"] = {"od550aer": "minutely"}
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    with pytest.raises(ColocationError) as e:
        col.run()
    assert str(e.value).startswith("Failed to load model data: TM5-met2010_CTRL-TEST (od550aer)")


def test_Colocator_model_add_vars(setup):
    model_var = "abs550aer"
    obs_var = "od550aer"
    setup["model_add_vars"] = {obs_var: [model_var]}
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    # Problem with saving since obs_id is different
    data = col.run(var_list=[model_var])
    assert isinstance(data, dict)
    assert model_var in data
    coldata = data[model_var][obs_var]
    assert coldata.var_name == ["od550aer", "abs550aer"]


def test_Colocator_init_basedir_coldata(setup, tmp_path: Path):
    base_path = tmp_path / "basedir"
    setup["basedir_coldata"] = base_path
    setup["raise_exceptions"] = True
    col_stp = ColocationSetup(**setup)
    Colocator(col_stp)

    assert base_path.is_dir()


def test_Colocator__infer_start_stop_yr_from_model_reader(tm5_aero_col_stp):
    col = Colocator(tm5_aero_col_stp)
    col.model_id = "TM5-met2010_CTRL-TEST"
    col._infer_start_stop_yr_from_model_reader()
    assert col.start == 2010
    assert col.stop is None


def test_Colocator__coldata_savename(setup):
    setup["raise_exceptions"] = True
    setup["obs_name"] = "obs"
    setup["model_name"] = "model"
    setup["filter_name"] = ALL_REGION_NAME
    setup["start"] = 2015
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    col._check_set_start_stop()
    savename = col._coldata_savename("od550aer", "od550ss", "daily")
    assert isinstance(savename, str)
    n = f"od550ss_od550aer_MOD-model_REF-obs_20150101_20151231_daily_{ALL_REGION_NAME}.nc"
    assert savename == n


def test_Colocator_run_gridded_gridded(setup):
    setup["obs_id"] = setup["model_id"]
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    col.run()
    var = col.colocation_setup.obs_vars[0]
    coldata = col.data[var][var]
    assert isinstance(coldata, ColocatedData)
    assert coldata.ndim == 4


@pytest.mark.parametrize(
    "update,chk_mvar,chk_ovar,sh,mean_obs,mean_mod",
    [
        (dict(), "od550aer", "od550aer", (2, 12, 11), 0.272, 0.244),
        (dict(regrid_res_deg=10), "od550aer", "od550aer", (2, 12, 11), 0.272, 0.229),
        (dict(), "od550aer", "od550aer", (2, 12, 11), 0.272, 0.244),
        (
            dict(
                model_use_vars={"od550aer": "abs550aer"},
                model_use_climatology=True,
                obs_use_climatology=ClimatologyConfig(set_year=2010),
            ),
            "abs550aer",
            "od550aer",
            (2, 12, 1),
            0.135,  # 0.123,
            0.002,
        ),
        (
            dict(model_use_vars={"od550aer": "abs550aer"}, model_use_climatology=True),
            "abs550aer",
            "od550aer",
            (2, 12, 1),
            0.159,
            0.002,
        ),
        (
            dict(
                model_use_vars={"od550aer": "abs550aer"},
                obs_use_climatology=ClimatologyConfig(set_year=2010),
            ),
            "abs550aer",
            "od550aer",
            (2, 12, 16),
            0.259,
            0.014,
        ),
    ],
)
def test_Colocator_run_gridded_ungridded(
    setup, update, chk_mvar, chk_ovar, sh, mean_obs, mean_mod
):
    setup.update(update)
    col_stp = ColocationSetup(**setup)

    result = Colocator(col_stp).run()
    assert isinstance(result, dict)

    coldata = result[chk_mvar][chk_ovar]
    assert "station_type" in coldata.coords
    assert coldata.shape == sh

    mod_clim_used = any("9999" in x for x in coldata.metadata["from_files"])
    assert col_stp.model_use_climatology == mod_clim_used

    assert np.nanmean(coldata.data[0].values) == pytest.approx(mean_obs, abs=0.01)
    assert np.nanmean(coldata.data[1].values) == pytest.approx(mean_mod, abs=0.01)


def test_Colocator_prepare_colocation_args(monkeypatch):
    def dummy_mdata(*args):
        d = GriddedData()
        d.ts_type = "hourly"
        return d

    def dummy_odata(*args):
        d = UngriddedData()
        d.ts_type = "hourly"
        fake_data = list(string.ascii_lowercase)
        for i, n in enumerate(fake_data):
            d.metadata[i] = dict(
                data_id="testcase",
                station_name=n,
                station_type=n,
            )
        assert d.station_name == fake_data
        assert {"station_type" in dict for dict in d.metadata.values()} == {True}
        return d

    with monkeypatch.context() as mp:
        mp.setattr("pyaerocom.colocation.colocator.Colocator.get_model_data", dummy_mdata)
        mp.setattr("pyaerocom.colocation.colocator.Colocator.get_obs_data", dummy_odata)

        col_stp = ColocationSetup(**default_setup)
        colocator = Colocator(col_stp)
        colocator.start = 2015
        colocator.stop = None
        # with pytest.raises(DataDimensionError) as e:
        args = colocator._prepare_colocation_args("abs550aer", "od550aer")
        assert args["add_meta_keys"] == ["station_type"]


def test_Colocator_prepare_colocation_args_malformed_metadata(monkeypatch):
    def dummy_mdata(*args):
        d = GriddedData()
        d.ts_type = "hourly"
        return d

    def dummy_odata(*args):
        d = UngriddedData()
        d.ts_type = "hourly"
        fake_data = list(string.ascii_lowercase)
        # add station_type only to some
        for i, n in enumerate(fake_data):
            if i > len(fake_data) / 2:
                d.metadata[i] = dict(
                    data_id="testcase",
                    station_name=n,
                    station_type=n,
                )
            else:
                d.metadata[i] = dict(
                    data_id="testcase",
                    station_name=n,
                )

        assert {"station_type" in dict for dict in d.metadata.values()} == {True, False}
        return d

    with monkeypatch.context() as mp:
        mp.setattr("pyaerocom.colocation.colocator.Colocator.get_model_data", dummy_mdata)
        mp.setattr("pyaerocom.colocation.colocator.Colocator.get_obs_data", dummy_odata)

        col_stp = ColocationSetup(**default_setup)
        colocator = Colocator(col_stp)
        colocator.start = 2015
        colocator.stop = None
        with pytest.raises(ValueError) as e:
            colocator._prepare_colocation_args("abs550aer", "od550aer")
        assert "some stations have `station_type` metadata while others do not" == e.value.args[0]


@pytest.mark.parametrize(
    "update,error",
    [
        pytest.param(dict(obs_vars=[]), "no observation variables specified", id="no obs"),
        pytest.param(
            dict(
                model_use_vars={"od550aer": "abs550aer"},
                model_use_climatology=True,
                obs_use_climatology=True,
                start=2008,
                stop=2012,
            ),
            "Conflict: only single year analyses are support",
            id="unsupported",
        ),
    ],
)
def test_Colocator_run_gridded_ungridded_error(setup, update, error):
    setup.update(update)
    col_stp = ColocationSetup(**setup)
    with pytest.raises(ColocationSetupError) as e:
        Colocator(col_stp).run()
    assert str(e.value).startswith(error)


def test_colocator_filter_name(setup):
    setup["filter_name"] = ALL_REGION_NAME
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    assert col.colocation_setup.filter_name == ALL_REGION_NAME


def test_colocator_read_ungridded(setup):
    # obs_id = "AeronetSunV3L2Subset.daily"
    obs_var = "od550aer"
    # setup["obs_id"] =
    setup["raise_exceptions"] = True
    setup["obs_filters"] = {"longitude": [-30, 30]}
    setup["read_opts_ungridded"] = {"last_file": 1}
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)

    data = col._read_ungridded(obs_var)
    assert isinstance(data, UngriddedData)
    assert len(data.metadata) == 1

    col.obs_vars = ["invalid"]
    with pytest.raises(ValueError):
        data = col._read_ungridded("invalid")


def test_colocator_get_model_data(setup):
    setup["raise_exceptions"] = True
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    col_stp = ColocationSetup(**setup)

    col = Colocator(col_stp)
    data = col.get_model_data("od550aer")
    assert isinstance(data, GriddedData)


def test_colocator__find_var_matches(setup):
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_id"] = "AeronetSunV3L2Subset.daily"
    setup2 = setup.copy()
    setup["obs_vars"] = "od550aer"
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)

    var_matches = col._find_var_matches()
    assert var_matches == {"od550aer": "od550aer"}

    obs_var = "conco3"
    setup2["obs_vars"] = obs_var
    setup2["model_use_vars"] = {obs_var: "od550aer"}
    col_stp2 = ColocationSetup(**setup2)
    col2 = Colocator(col_stp2)

    var_matches = col2._find_var_matches()
    assert var_matches == {"od550aer": "conco3"}


def test_colocator__find_var_matches_model_add_vars(setup):
    ovar = "od550aer"
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_id"] = "AeronetSunV3L2Subset.daily"
    setup["obs_vars"] = (ovar,)
    setup["model_add_vars"] = {ovar: ("abs550aer",)}
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    var_matches = col._find_var_matches()
    assert var_matches == {"abs550aer": ovar, ovar: ovar}


def test_colocator_instantiate_gridded_reader(setup, path_emep):
    model_id = "model"
    setup["gridded_reader_id"] = {"model": "ReadMscwCtm", "obs": "ReadGridded"}
    setup["model_id"] = model_id
    setup["filepath"] = path_emep
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    r = col._instantiate_gridded_reader(what="model")
    assert isinstance(r, ReadMscwCtm)
    assert r.data_id == model_id


def test_colocator_instantiate_gridded_reader_model_data_dir(setup, path_emep):
    model_data_dir = path_emep["data_dir"]
    model_id = "model"
    setup["gridded_reader_id"] = {"model": "ReadMscwCtm", "obs": "ReadGridded"}
    setup["model_data_dir"] = model_data_dir
    setup["model_id"] = model_id
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    r = col._instantiate_gridded_reader(what="model")
    assert isinstance(r, ReadMscwCtm)
    assert r._data_dir == model_data_dir
    assert r.data_id == model_id


def test_colocator__get_gridded_reader_class(setup):
    setup["gridded_reader_id"] = {"model": "ReadMscwCtm", "obs": "ReadMscwCtm"}
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    for what in ["model", "obs"]:
        assert col._get_gridded_reader_class(what=what) == ReadMscwCtm


def test_colocator__check_add_model_read_aux(setup):
    setup["raise_exceptions"] = True
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    assert not col._check_add_model_read_aux("od550aer")
    setup["model_read_aux"] = {
        "od550aer": dict(vars_required=["od550aer", "od550aer"], fun=add_cubes)
    }
    col_stp2 = ColocationSetup(**setup)
    col2 = Colocator(col_stp2)
    assert col2._check_add_model_read_aux("od550aer")


def test_colocator_with_obs_data_dir_ungridded(setup):
    setup["obs_id"] = "AeronetSunV3L2Subset.daily"
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_vars"] = "od550aer"
    setup["obs_data_dir"] = TEST_DATA["AeronetSunV3L2Subset.daily"].path
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T00:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T00:00:00.000000000"


def test_colocator_with_model_data_dir_ungridded(setup):
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_id"] = "AeronetSunV3L2Subset.daily"
    setup["obs_vars"] = "od550aer"
    setup["model_data_dir"] = TEST_DATA["MODELS"].path / "TM5-met2010_CTRL-TEST/renamed"
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T00:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T00:00:00.000000000"


def test_colocator_with_obs_data_dir_gridded(setup):
    setup["model_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_id"] = "TM5-met2010_CTRL-TEST"
    setup["obs_vars"] = "od550aer"
    setup["obs_dir"] = TEST_DATA["MODELS"].path / "TM5-met2010_CTRL-TEST/renamed"
    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)
    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T12:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T12:00:00.000000000"


###################################
#   Test for colocation with Pyaro
###################################


def test_colocation_pyaro(pyaro_testconfig, fake_aod_MSCWCtm_data_monthly_2010, setup) -> None:
    config = pyaro_testconfig[0]
    setup["pyaro_config"] = config
    setup["model_id"] = "EMEP"
    setup["gridded_reader_id"] = {"model": "ReadMscwCtm"}
    setup["model_data_dir"] = fake_aod_MSCWCtm_data_monthly_2010
    setup["obs_vars"] = "od550aer"  # This obs does not exist in Aeronet

    col_stp = ColocationSetup(**setup)
    col = Colocator(col_stp)

    data = col.run()

    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T00:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T00:00:00.000000000"

    assert np.sum(np.isnan(cd.data[0, :].data)) == 0

    assert cd.data[0, :].data.shape[0] == 12
