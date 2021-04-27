# -*- coding: utf-8 -*-
import os
import pytest
from pyaerocom.conftest import does_not_raise_exception, testdata_unavail
from pyaerocom import utils

def test_print_file(tmpdir):
    fp = os.path.join(tmpdir, 'file.txt')
    with pytest.raises(IOError):
        utils.print_file(fp)
    with open(fp, 'w') as f:
        f.write('Blaaaa\nBlub\n')
    utils.print_file(fp)

@testdata_unavail
@pytest.mark.parametrize('kwargs,raises,tabshape', [
    ({}, pytest.raises(TypeError), None),
    ({'model_ids' : 'TM5-met2010_CTRL-TEST',
      'vars_or_var_patterns' : 'abs550*'}, does_not_raise_exception(), (2,11)),
    ({'model_ids' : 'TM5-met2010_CTRL-TEST',
      'vars_or_var_patterns' : '*550*'}, does_not_raise_exception(), (4,11)),
    ({'model_ids' : 'TM5-met2010_CTRL-TEST',
      'vars_or_var_patterns' : 'od550aer',
      'read_data' : True}, does_not_raise_exception(), (2,11))
    ])
def test_create_varinfo_table(kwargs, raises, tabshape):
    with raises:
        df =  utils.create_varinfo_table(**kwargs)
        assert df.shape == tabshape




if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
