# -*- coding: utf-8 -*-
import os
from pathlib import Path
from pyaerocom import const
from pyaerocom._lowlevel_helpers import ConstrainedContainer


class DirLoc:
    def __init__(self, default=None, assert_exists=True):
        if default is None:
            default = ''
        self.assert_exists = assert_exists
        self.__set__(self, default)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        try:
            val = instance.__dict__[self.name]
        except (KeyError, AttributeError):
            val = self.val
        if not os.path.exists(val):
            const.print_log.info('creating', val)
            os.makedirs(val)
        return val

    def __set__(self, instance, value):

        if isinstance(value, Path):
            value = str(value)
        elif not isinstance(value, str):
            raise ValueError(value)
        try:
            instance.__dict__[self.name] = value
        except AttributeError:
            self.val = value

class OutputPathManager(ConstrainedContainer):
    JSON_SUBDIRS = ['map', 'ts', 'ts/dw', 'scat', 'hm', 'profiles', 'contour']

    json_basedir = DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/data'),
        assert_exists=False)

    coldata_basedir =DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/coldata'),
        assert_exists=False)

    ADD_GLOB = ['coldata_basedir', 'json_basedir']
    def __init__(self, proj_id:str, exp_id:str,
                 json_basedir:str=None, coldata_basedir:str=None
                 ):
        #: Base directory for output
        if not all([isinstance(x, str) for x in (proj_id, exp_id)]):
            raise ValueError('invalid input (both must be str)', proj_id,
                             exp_id)
        self.proj_id = proj_id
        self.exp_id = exp_id
        if coldata_basedir:
            self.coldata_basedir = coldata_basedir
        if json_basedir:
            self.json_basedir = json_basedir

    def _check_init_dir(self, loc, assert_exists):
        if assert_exists and not os.path.exists(loc):
            os.makedirs(loc)
        return loc

    def get_coldata_dir(self, assert_exists=True):
        loc = os.path.join(self.coldata_basedir, self.proj_id, self.exp_id)
        return self._check_init_dir(loc, assert_exists)

    def get_json_output_dirs(self, assert_exists=True):
        out = {}
        base = os.path.join(self.json_basedir, self.proj_id, self.exp_id)
        for subdir in self.JSON_SUBDIRS:
            loc = self._check_init_dir(os.path.join(base, subdir),
                                       assert_exists)
            out[subdir] = loc
        return out


if __name__ == '__main__':
    m = OutputPathManager('bla', 'blub')
    m.update(coldata_basedir='/')

    print(m.keys())
    print(m.values())
