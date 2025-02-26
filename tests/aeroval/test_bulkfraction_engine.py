from copy import deepcopy
import pytest
import numpy as np
from pathlib import Path

from pyaerocom.aeroval.bulkfraction_engine import BulkFractionEngine
from pyaerocom.aeroval import ExperimentProcessor
from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine, ExperimentOutput
from pyaerocom.aeroval import EvalSetup
from pyaerocom import ColocatedData
from tests.fixtures.aeroval import cfg_test_bulk


@pytest.fixture
def cfg(tmpdir) -> dict:
    cfg = deepcopy(cfg_test_bulk.CFG)
    cfg["json_basedir"] = f"{tmpdir}/data"
    cfg["coldata_basedir"] = f"{tmpdir}/coldata"
    return cfg


@pytest.fixture
def bulkengine_instance(cfg: dict) -> BulkFractionEngine:
    setup = deepcopy(EvalSetup(**cfg))
    bfe = BulkFractionEngine(setup)
    return bfe


def test___init__(cfg: dict):
    setup = EvalSetup(**cfg)
    bfe = BulkFractionEngine(setup)
    assert isinstance(bfe, ProcessingEngine)
    assert isinstance(bfe, HasColocator)


def test__get_bulk_vars(bulkengine_instance: BulkFractionEngine):
    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry("EBAS-m")
    assert (
        bulkengine_instance._get_bulk_vars("concwetrdn", obsentry)
        == obsentry.bulk_options["concwetrdn"].vars
    )

    with pytest.raises(KeyError, match="Could not find bulk vars entry"):
        bulkengine_instance._get_bulk_vars("concwetrdn2", obsentry)


def test_get_colocators_modelexists(bulkengine_instance: BulkFractionEngine):
    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry("EBAS-m")
    freq = obsentry.ts_type
    bulk_vars = bulkengine_instance._get_bulk_vars("concwetrdn", obsentry)
    cols_exist = bulkengine_instance.get_colocators(
        bulk_vars, "concwetrdn", freq, "EMEP", "EBAS-m", True
    )

    assert len(cols_exist) == 2

    assert (
        cols_exist[0][bulk_vars[0]].colocation_setup.model_use_vars[bulk_vars[0]]
        == cols_exist[1][bulk_vars[1]].colocation_setup.model_use_vars[bulk_vars[1]]
    )


def test_get_colocators(bulkengine_instance: BulkFractionEngine):
    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry("EBAS-m")
    freq = obsentry.ts_type
    bulk_vars = bulkengine_instance._get_bulk_vars("concwetrdn", obsentry)
    cols_exist = bulkengine_instance.get_colocators(
        bulk_vars, "concwetrdn", freq, "EMEP", "EBAS-m", False
    )

    assert len(cols_exist) == 2

    assert cols_exist[0][bulk_vars[0]].colocation_setup.obs_vars[0] == bulk_vars[0]
    assert cols_exist[1][bulk_vars[1]].colocation_setup.obs_vars[0] == bulk_vars[1]


def test__run_var(bulkengine_instance: BulkFractionEngine):
    obs_name = "AERONET-Sun"
    model_name = "TM5-AP3-CTRL"
    var_name = "fraction"
    freq = "monthly"
    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry(obs_name)
    modelentry = bulkengine_instance.cfg.model_cfg.get_entry(model_name)
    bulk_vars = bulkengine_instance._get_bulk_vars(var_name, obsentry)

    col, fp = bulkengine_instance._run_var(
        model_name, obs_name, var_name, bulk_vars, freq, obsentry, modelentry
    )

    assert isinstance(fp[0], str)
    assert isinstance(col, ColocatedData)
    assert pytest.approx(np.nanmean(col.data), rel=1e-5) == 1.0


def test__combine_coldatas(bulkengine_instance: BulkFractionEngine):
    obs_name = "AERONET-Sun"
    model_name = "TM5-AP3-CTRL"
    var_name = "fraction"
    freq = "monthly"
    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry(obs_name)
    modelentry = bulkengine_instance.cfg.model_cfg.get_entry(model_name)
    bulk_vars = bulkengine_instance._get_bulk_vars(var_name, obsentry)

    num_name = bulk_vars[0]
    denum_name = bulk_vars[1]

    model_exists = obsentry.bulk_options[var_name].model_exists
    cols = bulkengine_instance.get_colocators(
        bulk_vars, var_name, freq, model_name, obs_name, model_exists
    )

    coldatas = []
    for col in cols:
        if len(list(col.keys())) != 1:
            raise ValueError(
                "Found more than one colocated object when trying to run bulk variable"
            )
        bv = list(col.keys())[0]
        coldatas.append(col[bv].run(bv))

    obsentry2 = obsentry.model_copy()
    obsentry2.bulk_options[var_name].mode = "fraction"
    model_num_name, model_denum_name = bulkengine_instance._get_model_var_names(
        var_name, bulk_vars, model_exists, modelentry
    )

    data1 = bulkengine_instance._combine_coldatas(
        coldatas[0][model_num_name][num_name],
        coldatas[1][model_denum_name][denum_name],
        var_name,
        obsentry2,
    )

    assert pytest.approx(np.nanmean(data1.data), rel=1e-5) == 1.0
    assert len(data1.data) == max(
        len(coldatas[0][model_num_name][num_name].data),
        len(coldatas[1][model_denum_name][denum_name].data),
    )

    obsentry3 = obsentry.model_copy()
    obsentry3.bulk_options[var_name].mode = "product"
    data2 = bulkengine_instance._combine_coldatas(
        coldatas[0][model_num_name][num_name],
        coldatas[1][model_denum_name][denum_name],
        var_name,
        obsentry3,
    )

    assert len(data2.data) == max(
        len(coldatas[0][model_num_name][num_name].data),
        len(coldatas[1][model_denum_name][denum_name].data),
    )
    assert np.array_equal(
        data2.data.data, coldatas[0][model_num_name][num_name].data.data ** 2, equal_nan=True
    )


def test__combine_coldatas_model_exist(bulkengine_instance: BulkFractionEngine):
    obs_name = "AERONET-Sun-exist"
    model_name = "TM5-AP3-CTRL"
    var_name = "abs550aer"
    freq = "monthly"

    obsentry = bulkengine_instance.cfg.obs_cfg.get_entry(obs_name)
    modelentry = bulkengine_instance.cfg.model_cfg.get_entry(model_name)
    bulk_vars = bulkengine_instance._get_bulk_vars(var_name, obsentry)

    num_name = bulk_vars[0]
    denum_name = bulk_vars[1]

    model_exists = obsentry.bulk_options[var_name].model_exists
    cols = bulkengine_instance.get_colocators(
        bulk_vars, var_name, freq, model_name, obs_name, model_exists
    )

    coldatas = []
    for col in cols:
        if len(list(col.keys())) != 1:
            raise ValueError(
                "Found more than one colocated object when trying to run bulk variable"
            )
        bv = list(col.keys())[0]
        coldatas.append(col[bv].run(bv))

    obsentry2 = obsentry.model_copy()
    obsentry2.bulk_options[var_name].mode = "fraction"
    model_num_name, model_denum_name = bulkengine_instance._get_model_var_names(
        var_name, bulk_vars, model_exists, modelentry
    )

    data1 = bulkengine_instance._combine_coldatas(
        coldatas[0][model_num_name][num_name],
        coldatas[1][model_denum_name][denum_name],
        var_name,
        obsentry2,
    )

    assert pytest.approx(np.nanmean(data1.data[0]), rel=1e-5) == 1.0
    assert pytest.approx(np.nanmean(data1.data[1]), rel=1e-5) != 0.0135


def test_run(bulkengine_instance: BulkFractionEngine):
    obs_name = "AERONET-Sun-exist"
    model_name = "TM5-AP3-CTRL"
    var_name = "abs550aer"

    bulkengine_instance.exp_output.delete_experiment_data(also_coldata=True)

    bulkengine_instance.run(var_name, model_name, obs_name)

    output: ExperimentOutput = bulkengine_instance.exp_output
    assert Path(output.exp_dir).is_dir()


def test_run_cfg(cfg: dict):
    model_name = "TM5-AP3-CTRL"
    setup = EvalSetup(**cfg)
    proc = ExperimentProcessor(setup)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run(obs_name="AERONET-Sun", model_name="TM5-AP3-CTRL")

    output: ExperimentOutput = proc.exp_output
    assert Path(output.exp_dir).is_dir()

    output.avdb.get_experiments(output.proj_id)
    data = output.avdb.get_timeseries(
        output.proj_id, output.exp_id, "ALL", "AERONET-Sun", "fraction", "Column"
    )
    m_data = data[model_name]["monthly_mod"]
    o_data = data[model_name]["monthly_obs"]
    assert pytest.approx(np.nanmean(m_data), rel=1e-5) == 1.0
    assert pytest.approx(np.nanmean(o_data), rel=1e-5) == 1.0
