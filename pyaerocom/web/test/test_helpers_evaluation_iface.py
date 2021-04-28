import os
import pytest
import simplejson

from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.web import helpers_evaluation_iface as h

@pytest.mark.parametrize('base_dir, proj_id, exp_id', [
    ('/blaaa', 'blub', '42'), ('tmpdir', 'blub', '42'),
    ])
def test_delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id,
                                                 tmpdir):
    if base_dir == 'tmpdir':
        base_dir = tmpdir
        dp = os.path.join(str(tmpdir), proj_id, exp_id)
        os.makedirs(dp)
        assert os.path.exists(dp)
    h.delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)

@pytest.mark.parametrize('cfgdir, mkfiles, raises', [
    ('/blaaa', None, does_not_raise_exception()),
    ('tmpdir', None, does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub')], does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub_blablub')], does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub'), ('bla', 'blub1'), ('blub', 'blub')], does_not_raise_exception()),
    ])
def test_get_all_config_files_evaluation_iface(cfgdir, mkfiles, raises,
                                               tmpdir):
    res = {}
    if cfgdir == 'tmpdir':
        cfgdir = str(tmpdir)
        if isinstance(mkfiles, list):
            for pr, ex in mkfiles:

                fname = f'cfg_{pr}_{ex}.json'
                fp = os.path.join(tmpdir, fname)
                with open(fp, 'w'):
                    print(fp)
                if '_' in pr or '_' in ex:
                    continue
                if not pr in res:
                    res[pr] = {}
                res[pr][ex] = fp
    result = h.get_all_config_files_evaluation_iface(cfgdir)
    assert result == res

@pytest.mark.parametrize('exp_order, raises', [
    (['42', 'invalid'], does_not_raise_exception()),
    ('42', does_not_raise_exception()),
    ('43', does_not_raise_exception()),
    (None, does_not_raise_exception()),
    ({}, pytest.raises(ValueError))
    ])
def test_reorder_experiments_menu_evaluation_iface(exp_order, raises,
                                                   tmpdir):
    menu = {'bla' : {}, 'blub': {}, '42': {}}
    fp = tmpdir.join('menu.json')
    with open(fp, 'w') as f:
        simplejson.dump(menu, f)
    with raises:
        h.reorder_experiments_menu_evaluation_iface(fp, exp_order)

        with open(fp, 'r') as f:
            new = simplejson.load(f)
        if isinstance(exp_order, str):
            exp_order = [exp_order]
        elif exp_order is None:
            exp_order = []
        new_order = []
        for exp in exp_order:
            if exp in menu:
                new_order.append(exp)
        for exp in sorted(menu):
            if not exp in new_order:
                new_order.append(exp)
        assert list(new.keys()) == new_order

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)