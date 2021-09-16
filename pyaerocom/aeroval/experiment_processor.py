#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
from traceback import format_exc

from pyaerocom import const
from pyaerocom.aeroval._processing_base import ProcessingEngine, HasColocator
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.aeroval.coldatatojson_engine import ColdataToJsonEngine


class ExperimentProcessor(ProcessingEngine, HasColocator):
    """Processing engine for AeroVal experiment

    By default, this class processes one configuration file, represented by
    :class:`EvalSetup`. As such, an instance of :class:`EvalSetup` represents
    an AeroVal experiment, comprising a list of models, a list of observations
    (and variables).

    For each possible (or defined) model / obs / variable combination, the
    processing engine will perform spatial and temporal co-location and will
    store on co-located NetCDF file (e.g. if there are 2 models, 2 observation
    networks and 2 variables there will be 4 co-located NetCDF files).
    The co-location is done using :class:`pyaerocom.colocation_auto.Colocator`.



    """

    _log = const.print_log
    def coldata_to_json(self, file):
        """Creates all json files for one ColocatedData object"""
        coldata = ColocatedData(file)
        engine = ColdataToJsonEngine(self.cfg)
        return engine.run(coldata)

    def find_coldata_files(self, model_name, obs_name, var_name=None):
        """Find colocated data files for a certain model/obs/var combination

        Parameters
        ----------
        model_name : str
            name of model
        obs_name : str
            name of observation network
        var_name : str, optional
            name of variable.

        Returns
        -------
        list
            list of file paths of ColocatedData files that match input specs
        """

        files = []
        coldata_dir = os.path.join(self.coldata_dir, model_name)
        if os.path.exists(coldata_dir):
            for fname in os.listdir(coldata_dir):
                try:
                    m = ColocatedData.get_meta_from_filename(fname)
                    match = (m['data_source'][0] == obs_name and
                             m['data_source'][1] == model_name)
                    if var_name is not None:
                        try:
                            var_name = self.model_config[model_name]['model_use_vars'][var_name]
                        except:
                            pass
                        if not m['var_name'] == var_name:
                            match = False
                    if match:
                        files.append(os.path.join(coldata_dir, fname))
                except Exception:
                    const.print_log.warning('Invalid file {} in coldata dir'
                                            .format(fname))

        if len(files) == 0:
            msg = ('Could not find any colocated data files for model {}, '
                   'obs {}'
                   .format(model_name, obs_name))
            if self.cfg_colocation['raise_exceptions']:
                raise IOError(msg)
            else:
                self._log.warning(msg)
        return files

    def make_json_files(self, files):
        """Convert colocated data file(s) in model data directory into json

        Parameters
        ----------
        files : list
            list of colocated data files that are supposed to be converted to
            json files.

        Returns
        -------
        list
            list of colocated data files that were converted
        """
        converted = []
        for file in files:
            const.print_log.info(f'Processing: {file}')
            self.coldata_to_json(file)
            converted.append(file)
        return converted

    # ToDo: rewrite before v0.12.0
    def _run_superobs_entry_var(self, model_name, superobs_name, var_name,
                                try_colocate_if_missing):
        """
        Run evaluation of superobs entry

        Parameters
        ----------
        model_name : str
            name of model in :attr:`model_config`
        superobs_name : str
            name of super observation in :attr:`obs_config`
        var_name : str
            name of variable to be processed.
        try_colocate_if_missing : bool
            if True, then missing colocated data objects are computed on the
            fly.

        Raises
        ------
        ValueError
            If multiple (or no) colocated data objects are available for
            individual obs datasets of which the superobservation is comprised.

        Returns
        -------
        None
        """
        raise NotImplementedError('version of old AeroVal tools, needs revision')
        coldata_files = []
        coldata_resolutions = []
        vert_codes = []
        obs_needed = self.obs_config[superobs_name]['obs_id']
        for obs_name in obs_needed:
            if self.reanalyse_existing:
                self.run_colocation(model_name, obs_name, var_name)
                cdf = self.find_coldata_files(model_name, obs_name, var_name)
            else:
                cdf = self.find_coldata_files(model_name, obs_name, var_name)
                if len(cdf) == 0 and try_colocate_if_missing:
                    self.run_colocation(model_name, obs_name, var_name)
                    cdf = self.find_coldata_files(model_name, obs_name, var_name)

            if len(cdf) != 1:
                raise ValueError(
                    f'Fatal: Found multiple colocated data objects for '
                    f'{model_name}, {obs_name}, {var_name}: {cdf}...'
                    )
            fp = cdf[0]
            coldata_files.append(fp)
            meta = ColocatedData.get_meta_from_filename(fp)
            coldata_resolutions.append(meta['ts_type'])
            vc = self.get_vert_code(obs_name, var_name)
            vert_codes.append(vc)

        if len(np.unique(vert_codes)) > 1 or vert_codes[0] != self.get_vert_code(superobs_name, var_name):
            raise ValueError(
                "Cannot merge observations with different vertical types into "
                "super observation...")
        vert_code = vert_codes[0]
        if not len(coldata_files) == len(obs_needed):
            raise ValueError(f'Could not retrieve colocated data files for '
                             f'all required observations for super obs '
                             f'{superobs_name}')

        coldata = []
        from pyaerocom.helpers import get_lowest_resolution
        to_freq = get_lowest_resolution(*coldata_resolutions)
        import xarray as xr
        darrs = []
        for fp in coldata_files:
            data = ColocatedData(fp)
            if data.ts_type != to_freq:
                meta = data.metadata
                try:
                    rshow = meta['resample_how']
                except KeyError:
                    rshow = None

                data.resample_time(
                    to_ts_type=to_freq,
                    how=rshow,
                    apply_constraints=meta['apply_constraints'],
                    min_num_obs=meta['min_num_obs'],
                    colocate_time=meta['colocate_time'],
                    inplace=True)
            arr = data.data
            ds = arr['data_source'].values
            source_new = [superobs_name, ds[1]]
            arr['data_source'] = source_new #obs, model_id
            arr.attrs['data_source'] = source_new
            darrs.append(arr)

        merged = xr.concat(darrs, dim='station_name')
        coldata = ColocatedData(merged)
        return compute_json_files_from_colocateddata(
                coldata=coldata,
                obs_name=superobs_name,
                model_name=model_name,
                use_weights=self.weighted_stats,
                colocation_settings=coldata.get_time_resampling_settings(),
                vert_code=vert_code,
                out_dirs=self.out_dirs,
                regions_json=self.regions_file,
                web_iface_name=superobs_name,
                diurnal_only=False,
                statistics_freqs=self.statistics_freqs,
                regions_how=self.regions_how,
                zeros_to_nan=self.zeros_to_nan,
                annual_stats_constrained=self.annual_stats_constrained
                )

    def _run_superobs_entry(self, model_name, superobs_name, var_name=None,
                            try_colocate_if_missing=True):
        if not superobs_name in self.obs_config:
            raise AttributeError(
                f'No such super-observation {superobs_name}'
                )
        sobs_cfg = self.obs_config[superobs_name]
        if not sobs_cfg['is_superobs']:
            raise ValueError(f'Obs config entry for {superobs_name} is not '
                             f'marked as a superobservation. Please add '
                             f'is_superobs in config entry...')
        if isinstance(var_name, str):
            process_vars = [var_name]
        else:
            process_vars = sobs_cfg['obs_vars']
        for var_name in process_vars:
            try:
                self._run_superobs_entry_var(model_name,
                                             superobs_name,
                                             var_name,
                                             try_colocate_if_missing)
            except Exception:
                if self.raise_exceptions:
                    raise
                const.print_log.warning(
                    f'Failed to process superobs entry for {superobs_name},  '
                    f'{model_name}, var {var_name}. Reason: {format_exc()}')

    def _run_single_entry(self, model_name, obs_name, var_list):
        if model_name == obs_name:
            msg = ('Cannot run same dataset against each other'
                   '({} vs. {})'.format(model_name, model_name))
            self._log.info(msg)
            const.print_log.info(msg)
            return
        ocfg = self.cfg.get_obs_entry(obs_name)
        if ocfg['is_superobs']:
            try:
                self._run_superobs_entry(model_name, obs_name, var_list,
                                         try_colocate_if_missing=True)
            except Exception:
                if self.raise_exceptions:
                    raise
                const.print_log.warning(
                    'failed to process superobs...')
        elif ocfg['only_superobs']:
            const.print_log.info(
                f'Skipping json processing of {obs_name}, as this is '
                f'marked to be used only as part of a superobs '
                f'network')
        else:
            col = self.get_colocator(model_name, obs_name)
            if self.cfg.processing_opts.only_json:
                files_to_convert = col.get_available_coldata_files(var_list)
            else:
                col.run(var_list)
                files_to_convert = col.files_written

            if self.cfg.processing_opts.only_colocation:
                self._log.info(
                    f'FLAG ACTIVE: only_colocation: Skipping '
                    f'computation of json files for {obs_name} /'
                    f'{model_name} combination.')
            else:
                self.make_json_files(files_to_convert)

    def run(self, model_name=None, obs_name=None, var_list=None,
            update_interface=True):
        """Create colocated data and json files for model / obs combination

        Parameters
        ----------
        model_name : str or list, optional
            Name or pattern specifying model that is supposed to be analysed.
            Can also be a list of names or patterns to specify multiple models.
            If None (default), then all models are run that are part of this
            experiment.
        obs_name : :obj:`str`, or :obj:`list`, optional
            Like :attr:`model_name`, but for specification(s) of observations
            that are supposed to be used. If None (default) all observations
            are used.
        var_list : list, optional
            list variables supposed to be analysed. If None, then all
            variables available are used. Defaults to None. Can also be
            `str` type.
        update_interface : bool
            if true, relevant json files that determine what is displayed
            online are updated after the run, including the the menu.json file
            and also, the model info table (minfo.json) file is created and
            saved in :attr:`exp_dir`.

        Returns
        -------
        list
            list containing all colocated data objects that have been converted
            to json files.
        """
        if isinstance(var_list, str):
            var_list = [var_list]
        self.cfg._check_time_config()
        model_list = self.cfg.model_cfg.keylist(model_name)
        obs_list = self.cfg.obs_cfg.keylist(obs_name)

        const.print_log.info('Start processing')

        # compute model maps (completely independent of obs-eval
        # processing below)
        if self.cfg.webdisp_opts.add_model_maps:
            engine = ModelMapsEngine(self.cfg)
            map_files = engine.run(model_list=model_list,
                                   var_list=var_list)

        if not self.cfg.processing_opts.only_model_maps:
            for obs_name in obs_list:
                for model_name in model_list:
                    self._run_single_entry(model_name, obs_name, var_list)

        if update_interface:
            self.update_interface()
        const.print_log.info('Finished processing.')

    def update_interface(self):
        """Update aeroval interface

        Things done here:

            - Update menu file
            - Make aeroval info table json (tab informations in interface)
            - update and order heatmap file
        """
        self.exp_output.update_interface()

if __name__ == '__main__':
    stp = ExperimentProcessor('bla', 'blub')
    stp.to_json('/home/jonasg/MyPyaerocom/tmp/')


