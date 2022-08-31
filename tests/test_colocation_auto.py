from pathlib import Path

import numpy as np
import pytest

from pyaerocom import ColocatedData, GriddedData, UngriddedData, const
from pyaerocom.colocation_auto import ColocationSetup, Colocator
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import ColocationError, ColocationSetupError
from pyaerocom.io.aux_read_cubes import add_cubes
from pyaerocom.plugins.mscw_ctm.reader import ReadMscwCtm
from tests.fixtures.data_access import TEST_DATA

COL_OUT_DEFAULT = Path(const.OUTPUTDIR) / "colocated_data"

default_setup = {
    "model_id": None,
    "obs_id": None,
    "obs_vars": [],
    "ts_type": "monthly",
    "start": None,
    "stop": None,
    "filter_name": f"{ALL_REGION_NAME}-wMOUNTAINS",
    "basedir_coldata": COL_OUT_DEFAULT,
    "save_coldata": False,
    "obs_name": None,
    "obs_data_dir": None,
    "obs_use_climatology": False,
    "_obs_cache_only": False,
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
def tm5_aero_stp():
    return dict(
        model_id="TM5-met2010_CTRL-TEST",
        obs_id="AeronetSunV3L2Subset.daily",
        obs_vars="od550aer",
        start=2010,
        raise_exceptions=True,
        reanalyse_existing=True,
    )


@pytest.fixture(scope="function")
def col():
    return Colocator(raise_exceptions=True, reanalyse_existing=True)


@pytest.mark.parametrize("stp,should_be", [(ColocationSetup(), default_setup)])
def test_colocation_setup(stp: ColocationSetup, should_be: dict):
    for key, val in should_be.items():
        assert key in stp
        if key == "basedir_coldata":
            assert Path(val) == Path(stp["basedir_coldata"])
        else:
            assert val == stp[key], key


@pytest.mark.parametrize(
    "key,val,raises",
    [
        ("obs_vars", 42, pytest.raises(ValueError)),
        ("var_ref_outlier_ranges", [41, 42], pytest.raises(KeyError)),
        ("var_outlier_ranges", [41, 42], pytest.raises(KeyError)),
        ("remove_outliers", True, pytest.raises(KeyError)),
    ],
)
def test_ColocationSetup_invalid_input(key, val, raises):
    with raises:
        stp = ColocationSetup(**{key: val})
        assert stp[key] == val


def test_Colocator__obs_vars__setter(col):
    col.obs_vars = "var"
    assert col.obs_vars == ["var"]


def test_Colocator__add_attr(col):
    col.bla = "blub"
    col["blub"] = 42

    assert col.bla == "blub"
    assert "blub" in col


@pytest.mark.parametrize("ts_type_desired", ["daily", "monthly"])
@pytest.mark.parametrize("ts_type", ["monthly"])
@pytest.mark.parametrize("flex", [False, True])
def test_Colocator_model_ts_type_read(tm5_aero_stp, ts_type_desired, ts_type, flex):
    col = Colocator(**tm5_aero_stp)
    obs_var = "od550aer"
    assert tm5_aero_stp["obs_vars"] == obs_var
    col.save_coldata = False
    col.flex_ts_type = flex
    col.ts_type = ts_type
    # Problem with saving since obs_id is different
    # from obs_data.contains_dataset[0]...
    col.model_ts_type_read = {obs_var: ts_type_desired}
    data = col.run()
    assert isinstance(data, dict)
    assert obs_var in data
    coldata = data[obs_var][obs_var]
    assert coldata.ts_type == ts_type
    assert coldata.metadata["ts_type_src"][0] == "daily"
    if not flex:
        assert coldata.metadata["ts_type_src"][1] == ts_type_desired


def test_Colocator_model_ts_type_read_error(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    col.model_ts_type_read = {"od550aer": "minutely"}
    with pytest.raises(ColocationError) as e:
        col.run()
    assert str(e.value).startswith("Failed to load model data: TM5-met2010_CTRL-TEST (od550aer)")


def test_Colocator_model_add_vars(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    model_var = "abs550aer"
    obs_var = "od550aer"
    col.save_coldata = False
    # Problem with saving since obs_id is different

    col.model_add_vars = {obs_var: [model_var]}
    data = col.run(var_name=model_var)
    assert isinstance(data, dict)
    assert model_var in data
    coldata = data[model_var][obs_var]
    assert coldata.var_name == ["od550aer", "abs550aer"]


def test_Colocator_init_basedir_coldata(tmp_path: Path):
    base_path = tmp_path / "basedir"
    Colocator(raise_exceptions=True, basedir_coldata=base_path)
    assert base_path.is_dir()


def test_Colocator__infer_start_stop_yr_from_model_reader():
    col = Colocator()
    col.model_id = "TM5-met2010_CTRL-TEST"
    col._infer_start_stop_yr_from_model_reader()
    assert col.start == 2010
    assert col.stop == None


def test_Colocator__coldata_savename():
    col = Colocator(raise_exceptions=True)
    col.obs_name = "obs"
    col.model_name = "model"
    col.filter_name = ALL_REGION_NAME
    col.start = 2015
    col._check_set_start_stop()
    savename = col._coldata_savename("od550aer", "od550ss", "daily")
    assert isinstance(savename, str)
    n = f"od550ss_od550aer_MOD-model_REF-obs_20150101_20151231_daily_{ALL_REGION_NAME}.nc"
    assert savename == n


def test_Colocator_basedir_coldata(tmp_path: Path):
    base_path = tmp_path / "test"
    col = Colocator(raise_exceptions=True)
    col.basedir_coldata = base_path
    assert not base_path.is_dir()


def test_Colocator_update_basedir_coldata(tmp_path: Path):
    col = Colocator(raise_exceptions=True)

    base_path = tmp_path / "basedir"
    assert not base_path.is_dir()
    col.update(basedir_coldata=base_path)
    assert base_path.is_dir()


@pytest.mark.parametrize(
    "what",
    [
        dict(blaa=42),
        dict(obs_id="test", model_id="test"),
        dict(gridded_reader_id="test"),
        dict(gridded_reader_id={"test": 42}),
        dict(resample_how={"daily": {"hourly": "max"}}),
    ],
)
def test_Colocator_update(what):
    col = Colocator(raise_exceptions=True)
    col.update(**what)
    for key, val in what.items():
        assert col[key] == val


def test_Colocator_run_gridded_gridded(tm5_aero_stp):
    col = Colocator(**tm5_aero_stp)
    col.obs_id = col.model_id
    col.run()
    var = col.obs_vars[0]
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
                obs_use_climatology=True,
            ),
            "abs550aer",
            "od550aer",
            (2, 12, 1),
            0.123,
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
            dict(model_use_vars={"od550aer": "abs550aer"}, obs_use_climatology=True),
            "abs550aer",
            "od550aer",
            (2, 12, 16),
            0.259,
            0.014,
        ),
    ],
)
def test_Colocator_run_gridded_ungridded(
    tm5_aero_stp, update, chk_mvar, chk_ovar, sh, mean_obs, mean_mod
):
    stp = ColocationSetup(**tm5_aero_stp)
    stp.update(**update)

    result = Colocator(**stp).run()
    assert isinstance(result, dict)

    coldata = result[chk_mvar][chk_ovar]
    assert coldata.shape == sh

    mod_clim_used = any("9999" in x for x in coldata.metadata["from_files"])
    assert stp.model_use_climatology == mod_clim_used

    assert np.nanmean(coldata.data[0].values) == pytest.approx(mean_obs, abs=0.01)
    assert np.nanmean(coldata.data[1].values) == pytest.approx(mean_mod, abs=0.01)


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
def test_Colocator_run_gridded_ungridded_error(tm5_aero_stp, update, error):
    stp = ColocationSetup(**tm5_aero_stp)
    stp.update(**update)
    with pytest.raises(ColocationSetupError) as e:
        Colocator(**stp).run()
    assert str(e.value).startswith(error)


def test_colocator_filter_name():
    col = Colocator(filter_name=ALL_REGION_NAME)
    assert col.filter_name == ALL_REGION_NAME


def test_colocator_read_ungridded():
    col = Colocator(raise_exceptions=True)
    obs_id = "AeronetSunV3L2Subset.daily"
    obs_var = "od550aer"
    col.obs_filters = {"longitude": [-30, 30]}
    col.obs_id = obs_id
    col.read_opts_ungridded = {"last_file": 1}

    data = col._read_ungridded(obs_var)
    assert isinstance(data, UngriddedData)
    assert len(data.metadata) == 1

    col.obs_vars = ["invalid"]
    with pytest.raises(ValueError):
        data = col._read_ungridded("invalid")


def test_colocator_get_model_data():
    col = Colocator(raise_exceptions=True)
    model_id = "TM5-met2010_CTRL-TEST"
    col.model_id = model_id
    data = col.get_model_data("od550aer")
    assert isinstance(data, GriddedData)


def test_colocator__find_var_matches():
    col = Colocator()
    col.model_id = "TM5-met2010_CTRL-TEST"
    col.obs_id = "AeronetSunV3L2Subset.daily"
    col.obs_vars = "od550aer"

    var_matches = col._find_var_matches()
    assert var_matches == {"od550aer": "od550aer"}

    obs_var = "conco3"
    col.obs_vars = [obs_var]
    col.model_use_vars = {obs_var: "od550aer"}
    var_matches = col._find_var_matches()
    assert var_matches == {"od550aer": "conco3"}


def test_colocator__find_var_matches_model_add_vars():
    col = Colocator()
    col.model_id = "TM5-met2010_CTRL-TEST"
    col.obs_id = "AeronetSunV3L2Subset.daily"
    ovar = "od550aer"
    col.obs_vars = [ovar]

    col.model_add_vars = {ovar: ["abs550aer"]}
    var_matches = col._find_var_matches()
    assert var_matches == {"abs550aer": ovar, ovar: ovar}


def test_colocator_instantiate_gridded_reader(path_emep):
    col = Colocator(gridded_reader_id={"model": "ReadMscwCtm", "obs": "ReadGridded"})
    col.filepath = path_emep["daily"]
    model_id = "model"
    col.model_id = model_id
    r = col._instantiate_gridded_reader(what="model")
    assert isinstance(r, ReadMscwCtm)
    assert r.data_id == model_id


def test_colocator_instantiate_gridded_reader_model_data_dir(path_emep):
    col = Colocator(gridded_reader_id={"model": "ReadMscwCtm", "obs": "ReadGridded"})
    model_data_dir = path_emep["data_dir"]
    col.model_data_dir = path_emep["data_dir"]
    model_id = "model"
    col.model_id = model_id
    r = col._instantiate_gridded_reader(what="model")
    assert isinstance(r, ReadMscwCtm)
    assert r.data_dir == model_data_dir
    assert r.data_id == model_id


def test_colocator__get_gridded_reader_class():
    gridded_reader_id = {"model": "ReadMscwCtm", "obs": "ReadMscwCtm"}
    col = Colocator(gridded_reader_id=gridded_reader_id)
    for what in ["model", "obs"]:
        assert col._get_gridded_reader_class(what=what) == ReadMscwCtm


def test_colocator__check_add_model_read_aux():
    col = Colocator(raise_exceptions=True)
    col.model_id = "TM5-met2010_CTRL-TEST"
    assert not col._check_add_model_read_aux("od550aer")
    col.model_read_aux = {"od550aer": dict(vars_required=["od550aer", "od550aer"], fun=add_cubes)}
    assert col._check_add_model_read_aux("od550aer")


def test_colocator_with_obs_data_dir_ungridded():
    col = Colocator(save_coldata=False)
    col.model_id = "TM5-met2010_CTRL-TEST"
    col.obs_id = "AeronetSunV3L2Subset.daily"
    col.obs_vars = "od550aer"
    col.ts_type = "monthly"

    col.obs_data_dir = TEST_DATA["AeronetSunV3L2Subset.daily"].path

    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T00:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T00:00:00.000000000"


def test_colocator_with_model_data_dir_ungridded():
    col = Colocator(save_coldata=False)
    col.model_id = "TM5-met2010_CTRL-TEST"
    col.obs_id = "AeronetSunV3L2Subset.daily"
    col.obs_vars = "od550aer"
    col.ts_type = "monthly"

    col.model_data_dir = TEST_DATA["MODELS"].path / "TM5-met2010_CTRL-TEST/renamed"

    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T00:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T00:00:00.000000000"


def test_colocator_with_obs_data_dir_gridded():
    col = Colocator(save_coldata=False)
    col.model_id = "TM5-met2010_CTRL-TEST"
    col.obs_id = "TM5-met2010_CTRL-TEST"
    col.obs_vars = "od550aer"
    col.ts_type = "monthly"

    obs_dir = TEST_DATA["MODELS"].path / "TM5-met2010_CTRL-TEST/renamed"
    col.obs_data_dir = str(obs_dir)

    data = col.run()
    assert len(data) == 1
    cd = data["od550aer"]["od550aer"]
    assert isinstance(cd, ColocatedData)
    assert cd.ts_type == "monthly"
    assert str(cd.start) == "2010-01-15T12:00:00.000000000"
    assert str(cd.stop) == "2010-12-15T12:00:00.000000000"
