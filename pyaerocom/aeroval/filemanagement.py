# -*- coding: utf-8 -*-
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import ConstrainedContainer

class OutputPathManager(ConstrainedContainer):
    OUT_DIR_NAMES = ['map', 'ts', 'ts/dw', 'scat', 'hm', 'profiles', 'contour']
    PRIVATE_KEYS = ['_out_dirs']
    def __init__(self, out_basedir: str = None, **kwargs):
        #: Base directory for output
        if out_basedir is None:
            out_basedir = os.path.join(const.OUTPUTDIR, 'aeroval')
        self.out_basedir = out_basedir

        #: Output directories for different types of json files (will be filled
        #: in :func:`init_json_output_dirs`)
        self._out_dirs = {}



if __name__ == '__main__':
    stp = OutputPathManager()
    stp.update(res_deg=10)
    print(stp)
    for key, val in stp.items():
        print(key, val)