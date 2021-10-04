import pytest
import os, glob
from pyaerocom import const
from pyaerocom._lowlevel_helpers import read_json,write_json
from pyaerocom.aeroval import experiment_output as mod, ExperimentProcessor
from pyaerocom.aeroval.setupclasses import EvalSetup
from ..conftest import does_not_raise_exception
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
BASEDIR_DEFAULT = os.path.join(const.OUTPUTDIR, 'aeroval/data')


@pytest.fixture(scope='module')
def dummy_setup():
    return EvalSetup(proj_id='proj',exp_id='exp')

@pytest.fixture(scope='module')
def dummy_expout(dummy_setup):
    return mod.ExperimentOutput(dummy_setup)

@pytest.mark.parametrize('proj_id,json_basedir,raises', [
    (42,None,pytest.raises(ValueError)),
    ('bla',None,does_not_raise_exception()),
    ('bla','/',does_not_raise_exception()),
    ('bla','/blablub/blaaaa',pytest.raises(FileNotFoundError)),
])
def test_ProjectOutput___init__(proj_id,json_basedir,raises):
    with raises:
        val = mod.ProjectOutput(proj_id,json_basedir)
        assert val.proj_id == proj_id
        if json_basedir is not None:
            assert os.path.exists(val.json_basedir)

def test_ProjectOutput_proj_dir(tmpdir):
    loc = str(tmpdir)
    val = mod.ProjectOutput('test', loc)
    path = os.path.join(loc, 'test')
    assert val.proj_dir == path
    assert os.path.exists(path)

def test_ProjectOutput_experiments_file(tmpdir):
    loc = str(tmpdir)
    val = mod.ProjectOutput('test', loc)
    fp = os.path.join(loc, 'test', 'experiments.json')
    assert val.experiments_file == fp
    assert os.path.exists(fp)

@pytest.mark.parametrize('add', [None, 'exp'])
def test_ProjectOutput_available_experiments(tmpdir,add):
    loc = str(tmpdir)
    val = mod.ProjectOutput('test', loc)
    fp = val.experiments_file
    if add is not None:
        write_json({add:42}, fp)
        assert add in val.available_experiments
    else:
        val.available_experiments == []

def test_ProjectOutput__add_entry_experiments_json(tmpdir):
    loc = str(tmpdir)
    val = mod.ProjectOutput('test', loc)
    val._add_entry_experiments_json('test',42)
    assert 'test' in val.available_experiments

def test_ProjectOutput__del_entry_experiments_json(tmpdir):
    loc = str(tmpdir)
    exp_id = 'test'
    val = mod.ProjectOutput('test', loc)
    val._add_entry_experiments_json(exp_id,{})
    assert exp_id in val.available_experiments
    val._del_entry_experiments_json(exp_id)
    assert exp_id not in val.available_experiments
    # to catch KeyError and make sure it passes
    val._del_entry_experiments_json(exp_id)


@pytest.mark.parametrize('cfg,raises', [
    (None, pytest.raises(ValueError)),
    (EvalSetup(proj_id='proj', exp_id='exp'), does_not_raise_exception())
])
def test_ExperimentOutput___init__(cfg,raises):
    with raises:
        val = mod.ExperimentOutput(cfg)
        assert isinstance(val.cfg, EvalSetup)
        assert val.proj_id == cfg['proj_info']['proj_id']
        assert os.path.exists(BASEDIR_DEFAULT)
        assert os.path.samefile(val.json_basedir, BASEDIR_DEFAULT)

def test_ExperimentOutput_exp_id(dummy_expout):
    assert dummy_expout.exp_id == 'exp'

def test_ExperimentOutput_exp_dir(dummy_expout):

    exp_dir = os.path.join(BASEDIR_DEFAULT, 'proj','exp')
    assert dummy_expout.exp_dir == exp_dir

def test_ExperimentOutput_regions_file(dummy_expout):
    assert dummy_expout.regions_file == os.path.join(dummy_expout.exp_dir,
                                                    'regions.json')

def test_ExperimentOutput_statistics_file(dummy_expout):
    assert dummy_expout.statistics_file == os.path.join(dummy_expout.exp_dir,
                                                    'statistics.json')

def test_ExperimentOutput_var_ranges_file(dummy_expout):
    assert dummy_expout.var_ranges_file == os.path.join(dummy_expout.exp_dir,
                                                    'ranges.json')

def test_ExperimentOutput_menu_file(dummy_expout):
    assert dummy_expout.menu_file == os.path.join(dummy_expout.exp_dir,
                                                  'menu.json')


def test_ExperimentOutput_results_available_False(dummy_expout):
    assert not dummy_expout.results_available

def test_ExperimentOutput_update_menu_EMPTY(dummy_expout):
    dummy_expout.update_menu()
    assert os.path.exists(dummy_expout.menu_file)
    assert read_json(dummy_expout.menu_file) == {}

def test_ExperimentOutput_update_interface_EMPTY(dummy_expout):
    dummy_expout.update_interface()

def test_ExperimentOutput_update_heatmap_json_EMPTY(dummy_expout):
    dummy_expout._sync_heatmaps_with_menu_and_regions()

@pytest.mark.parametrize('filename,result,raises', [
    ('blaaaa', None, pytest.raises(ValueError)),
    ('EBAS-2010-ac550aer_Surface_ECHAM-HAM-ac550dryaer.json',
     ('EBAS-2010', 'ac550aer', 'Surface', 'ECHAM-HAM', 'ac550dryaer'),
     does_not_raise_exception()),
    ('EBAS-2010-ac550aer_Surface_ECHAM-HAM_ac550dryaer.json',None,
     pytest.raises(ValueError)),
])
def test_ExperimentOutput__info_from_map_file(filename,result,raises):
    with raises:
        output = mod.ExperimentOutput._info_from_map_file(filename)
        assert output == result

def test_ExperimentOutput__results_summary_EMPTY(dummy_expout):
    assert dummy_expout._results_summary() == {'obs': [], 'ovar': [],
                                               'vc': [], 'mod': [], 'mvar': []}

@pytest.mark.skip(reason='needs revision')
def test_ExperimentOutput_clean_json_files(dummy_expout):
    pass

@pytest.mark.skip(reason='needs revision')
def test_ExperimentOutput__clean_modelmap_files(dummy_expout):
    dummy_expout._clean_modelmap_files()

@pytest.mark.parametrize('also_coldata',[True,False])
def test_ExperimentOutput_delete_experiment_data(tmpdir, also_coldata):
    json_dir = os.path.join(tmpdir, 'json')
    coldata_dir = os.path.join(tmpdir, 'coldata')
    stp = EvalSetup(proj_id='proj', exp_id='exp',
                    coldata_basedir=coldata_dir,
                    json_basedir=json_dir)

    eo = mod.ExperimentOutput(stp)
    expdir = os.path.join(json_dir, 'proj', 'exp')
    coldir = os.path.join(coldata_dir, 'proj', 'exp')
    col_out = eo.cfg.path_manager.get_coldata_dir()
    assert os.path.samefile(coldir, col_out)
    assert os.path.samefile(expdir, eo.exp_dir)
    assert os.path.exists(coldata_dir)
    assert os.path.exists(coldir)
    eo.delete_experiment_data(also_coldata=also_coldata)
    assert not os.path.exists(expdir)
    if also_coldata:
        assert not os.path.exists(coldir)
    else:
        assert os.path.exists(coldata_dir)

### BELOW ARE TESTS ON ACTUAL OUTPUT THAT DEPEND ON EVALUATION RUNS

def test_ExperimentOutput_delete_experiment_data():
    cfg = EvalSetup(**cfgexp1)
    cfg.webdisp_opts.regions_how='htap'
    cfg.webdisp_opts.add_model_maps=False
    cfg.statistics_opts.add_trends=False
    cfg.time_cfg.add_seasons=False
    proc = ExperimentProcessor(cfg)
    proc.run()
    chk = proc.exp_output.exp_dir
    assert os.path.exists(chk)
    proc.exp_output.delete_experiment_data()
    assert not os.path.exists(chk)

CHK_CFG1 = {
    'map': ['AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json'],
    'contour': ['od550aer_TM5-AP3-CTRL.geojson',
                'od550aer_TM5-AP3-CTRL.json'],
    'hm': ['glob_stats_daily.json','glob_stats_monthly.json',
           'glob_stats_yearly.json'],
    'hm/ts': ['stats_ts.json'],
    'scat': ['AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json'],
    'ts': 11, # number of .json files in subdir
    'ts/diurnal': 0 # number of .json files in subdir
}

CHK_CFG2 = {
    'map': ['AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json',
            'AERONET-SDA-od550aer_Column_TM5-AP3-CTRL-od550aer.json'],
    'contour': 0,
    'hm': ['glob_stats_monthly.json'],
    'hm/ts': ['stats_ts.json'],
    'scat': ['AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json',
             'AERONET-SDA-od550aer_Column_TM5-AP3-CTRL-od550aer.json'],
    'ts': 40, # number of .json files in subdir
    'ts/diurnal': 0 # number of .json files in subdir
}

@pytest.mark.parametrize('cfgdict,chk_files',[
    (cfgexp1,CHK_CFG1),
    (cfgexp2,CHK_CFG2),
])
def test_ExperimentOutput__FILES(cfgdict,chk_files):
    cfg = EvalSetup(**cfgdict)
    fname = f'cfg_{cfg.proj_id}_{cfg.exp_id}.json'
    #cfg.webdisp_opts.regions_how='country'
    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()

    output = proc.exp_output
    assert os.path.exists(output.exp_dir)
    assert os.path.exists(output.experiments_file)
    assert os.path.exists(output.var_ranges_file)
    assert os.path.exists(output.statistics_file)
    assert os.path.exists(output.menu_file)
    assert os.path.exists(os.path.join(output.exp_dir, fname))
    for key, val in cfg.path_manager.get_json_output_dirs().items():
        assert os.path.exists(val)
        files = os.listdir(val)
        if key in chk_files:
            check = chk_files[key]
            if isinstance(check, list):
                for fname in check:
                    assert fname in files
            elif isinstance(check, int):
                numfiles = glob.glob(f'{val}/*.json')
                assert len(numfiles) == check




