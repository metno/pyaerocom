# -*- coding: utf-8 -*-
import os
from pyaerocom import const
from pyaerocom._lowlevel_helpers import (ConstrainedContainer, DirLoc,
                                         StrType, JSONFile)

class OutputPathManager(ConstrainedContainer):
    JSON_SUBDIRS = ['map', 'ts', 'ts/dw', 'scat', 'hm', 'profiles', 'contour']

    json_basedir = DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/data'),
        assert_exists=True,
        auto_create=True,
        logger=const.print_log,
        tooltip='Base directory for json output files')

    coldata_basedir =DirLoc(
        default=os.path.join(const.OUTPUTDIR, 'aeroval/coldata'),
        assert_exists=True,
        auto_create=True,
        logger=const.print_log,
        tooltip='Base directory for colocated data output files (NetCDF)')

    ADD_GLOB = ['coldata_basedir', 'json_basedir']
    proj_id = StrType()
    exp_id = StrType()
    def __init__(self, proj_id:str, exp_id:str,
                 json_basedir:str=None, coldata_basedir:str=None):
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

class ProjectOutput:
    """JSON output for project"""
    proj_id = StrType()
    json_basedir = DirLoc(assert_exists=True)
    experiments_file = JSONFile(assert_exists=True)

    def __init__(self, proj_id:str, json_basedir:str):
        self.proj_id = proj_id
        self.json_basedir = json_basedir

    @property
    def proj_dir(self):
        """Project directory"""
        return os.path.join(self.json_basedir, self.proj_id)

    @property
    def experiments_file(self):
        """json file containing region specifications"""
        return os.path.join(self.proj_dir, 'experiments.json')

    @property
    def available_experiments(self):
        raise NotImplementedError()


class ExperimentOutput(ProjectOutput):
    """JSON output for experiment"""
    exp_id = StrType()
    def __init__(self, exp_id:str, proj_id:str, json_basedir:str):
        super(ExperimentOutput, self).__init__(proj_id, json_basedir)
        self.exp_id = exp_id

    @property
    def exp_dir(self):
        """Experiment directory"""
        return os.path.join(self.proj_dir, self.exp_id)

    @property
    def regions_file(self):
        """json file containing region specifications"""
        return os.path.join(self.exp_dir, 'regions.json')

    @property
    def menu_file(self):
        """json file containing region specifications"""
        return os.path.join(self.exp_dir, 'menu.json')

    @property
    def results_available(self):
        """
        bool: True if results are available for this experiment, else False
        """
        if not self.exp_id in os.listdir(self.proj_id):
            return False
        elif not len(self.all_map_files) > 0:
            return False
        return True




if __name__ == '__main__':
    m = OutputPathManager('bla', 'blub')
    print(m)
    bd = os.path.join(const.OUTPUTDIR, 'tmp')
    pr = ExperimentOutput('bla', 'blub', json_basedir=bd)
    pr.experiments_file



