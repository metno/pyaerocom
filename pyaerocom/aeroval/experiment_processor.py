#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import numpy as np
import shutil
from traceback import format_exc

# internal pyaerocom imports
from pyaerocom._lowlevel_helpers import (sort_dict_by_name)
from pyaerocom import const
from pyaerocom.exceptions import FileConventionError
from pyaerocom.colocation_auto import Colocator
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.helpers import isnumeric

from pyaerocom.aeroval.helpers import (
    delete_experiment_data_evaluation_iface,
    read_json, write_json)

from pyaerocom.aeroval.coldata_to_json import (
    compute_json_files_from_colocateddata,
    get_heatmap_filename
    )

from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.aeroval.experiment_output import ExperimentOutput

class MapProcessor:

    @property
    def all_modelmap_vars(self):
        """List of variables to be processed for model map display

        Note
        ----
        For now this is just a wrapper for :attr:`all_obs_vars`
        """
        return self.all_obs_vars

    def run_map_eval(self, model_name, var_name):
        """Run evaluation of map processing

        Create json files for model-maps display. This analysis does not
        require any observation data but processes model output at all model
        grid points, which is then displayed on the website in the maps
        section.

        Parameters
        ----------
        model_name : str
            name of model to be processed
        var_name : str, optional
            name of variable to be processed. If None, all available
            observation variables are used.
        reanalyse_existing : bool
            if True, existing json files will be reprocessed
        raise_exceptions : bool
            if True, any exceptions that may occur will be raised
        """
        if var_name is None:
            all_vars = self.all_modelmap_vars
        else:
            all_vars = [var_name]

        model_cfg = self.get_model_config(model_name)
        settings = {}
        settings.update(self.cfg_colocation)
        settings.update(model_cfg)

        for var in all_vars:
            const.print_log.info(f'Processing model maps for '
                                 f'{model_name} ({var})')

            try:
                self._process_map_var(model_name, var,
                                      self.reanalyse_existing)

            except Exception:
                if self.raise_exceptions:
                    raise
                const.print_log.warning(
                    f'Failed to process maps for {model_name} {var} data. '
                    f'Reason: {format_exc()}')

    def _process_map_var(self, model_name, var, reanalyse_existing):
        """
        Process model data to create map json files

        Parameters
        ----------
        model_name : str
            name of model
        var : str
            name of variable
        reanalyse_existing : bool
            if True, already existing json files will be reprocessed

        Raises
        ------
        ValueError
            If vertical code of data is invalid or not set
        AttributeError
            If the data has the incorrect number of dimensions or misses either
            of time, latitude or longitude dimension.
        """
        from pyaerocom.aeroval.modelmaps_helpers import (calc_contour_json,
                                                         griddeddata_to_jsondict)

        data = self.read_model_data(model_name, var)

        vc = data.vert_code
        if not isinstance(vc, str) or vc=='':
            raise ValueError(f'Invalid vert_code {vc} in GriddedData')
        elif vc == 'ModelLevel':
            if not data.ndim == 4:
                raise ValueError('Invalid ModelLevel file, needs to have '
                                 '4 dimensions (time, lat, lon, lev)')
            data = data.extract_surface_level()
            vc = 'Surface'
        elif not vc in self.JSON_SUPPORTED_VERT_SCHEMES:
            raise ValueError(f'Cannot process {vc} files. Supported vertical '
                             f'codes are {self.JSON_SUPPORTED_VERT_SCHEMES}')
        if not data.has_time_dim:
            raise AttributeError('Data needs to have time dimension...')
        elif not data.has_latlon_dims:
            raise AttributeError('Data needs to have lat and lon dimensions')
        elif not data.ndim == 3:
            raise AttributeError('Data needs to be 3-dimensional')

        outdir = self.out_dirs['contour']
        outname = f'{var}_{vc}_{model_name}'

        fp_json = os.path.join(outdir, f'{outname}.json')
        fp_geojson = os.path.join(outdir, f'{outname}.geojson')

        if not reanalyse_existing:
            if os.path.exists(fp_json) and os.path.exists(fp_geojson):
                const.print_log.info(
                    f'Skipping processing of {outname}: data already exists.'
                    )
                return


        if not data.ts_type == 'monthly':
            data = data.resample_time('monthly')

        data.check_unit()

        vminmax = self.maps_vmin_vmax
        if var in self.cfg_model_maps['vmin_vmax']:
            vmin, vmax = vminmax[var]
        else:
            vmin, vmax = None, None

        # first calcualate and save geojson with contour levels
        contourjson = calc_contour_json(data, vmin=vmin, vmax=vmax)

        # now calculate pixel data json file (basically a json file
        # containing monthly mean timeseries at each grid point at
        # a lower resolution)
        if isnumeric(self.maps_res_deg):
            lat_res = self.maps_res_deg
            lon_res = self.maps_res_deg
        else:
            lat_res = self.maps_res_deg['lat_res_deg']
            lon_res = self.maps_res_deg['lon_res_deg']


        datajson = griddeddata_to_jsondict(data,
                                           lat_res_deg=lat_res,
                                           lon_res_deg=lon_res)
        write_json(contourjson, fp_geojson, ignore_nan=True)
        write_json(datajson, fp_json, ignore_nan=True)

class ExperimentProcessor:
    """Composite class representing a full setup for an AeroVal experiment
    """

    JSON_SUPPORTED_VERT_SCHEMES = ['Column', 'Surface']

    #: Attributes that are ignored when writing setup to json file
    JSON_CFG_IGNORE = ['add_methods', '_log', 'out_dirs']

    #: attributes that are not supported by this interface
    FORBIDDEN_ATTRS = ['basedir_coldata']
    _log = const.print_log
    def __init__(self, cfg):
        if not isinstance(cfg, EvalSetup):
            raise ValueError()
        self.cfg = cfg
        self.exp_output = ExperimentOutput(cfg)

    def _get_diurnal_only(self, obs_name):
        """
        Check if colocated data is flagged for only diurnal processing

        Parameters
        ----------
        obs_name : string
            Name of observational subset
        colocated_data : ColocatedData
            A ColocatedData object that will be checked for suitability of
            diurnal processing.

        Returns
        -------
        diurnal_only : bool
        """
        try:
            diurnal_only = self.cfg.get_obs_entry(obs_name).diurnal_only
        except AttributeError:
            diurnal_only = False
        return diurnal_only

    def coldata_to_json(self, file):
        """Creates all json files for one ColocatedData object"""
        coldata = ColocatedData(file)
        compute_json_files_from_colocateddata(
                coldata=coldata,
                cfg=self.cfg,
                exp_output=self.exp_output)

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

    def init_colocator(self, model_name:str=None,
                       obs_name:str=None) -> Colocator:
        """
        Instantate colocation engine

        Parameters
        ----------
        model_name : str, optional
            name of model. The default is None.
        obs_name : str, optional
            name of obs. The default is None.

        Returns
        -------
        Colocator

        """
        col = Colocator(**self.cfg.colocation_opts)
        if obs_name:
            obs_cfg = self.cfg.get_obs_entry(obs_name)
            col.import_from(obs_cfg)
            col.add_glob_meta(diurnal_only=self._get_diurnal_only(obs_name))
        if model_name:
            mod_cfg = self.cfg.get_model_entry(model_name)
            col.import_from(mod_cfg)
        outdir = self.cfg.path_manager.get_coldata_dir()
        col.basedir_coldata = outdir
        return col

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





    def delete_invalid_coldata_files(self, dry_run=False):
        """
        Find and delete invalid colocated NetCDF files

        Invalid NetCDF files are identified via model and obs name specified
        in this setup and by list of variable specified for model and obs,
        respectively, see also :func:`check_available_coldata_files`.

        Parameters
        ----------
        dry_run : bool, optional
            If True, then no files are deleted but a print statement is
            provided for each file that would be deleted. The default is False.


        Returns
        -------
        list
            List of invalid files that have been (would be) deleted.

        """
        raise NotImplementedError
        for mod in self.all_model_names:
            for obs in self.all_obs_names:
                col = self.init_colocator(mod, obs)

        invalid = self.check_available_coldata_files()[1]
        if len(invalid) == 0:
            const.print_log.info('No invalid colocated data files found.')
        else:
            for file in invalid:
                if dry_run:
                    const.print_log.info(f'Would delete {file}')
                else:
                    os.remove(file)
        return invalid

    def _run_single_entry(self, model_name, obs_name, var_name):
        if model_name == obs_name:
            msg = ('Cannot run same dataset against each other'
                   '({} vs. {})'.format(model_name, model_name))
            self._log.info(msg)
            const.print_log.info(msg)
            return
        ocfg = self.cfg.get_obs_entry(obs_name)
        if ocfg['is_superobs']:
            try:
                self._run_superobs_entry(model_name, obs_name, var_name,
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
            col = self.init_colocator(model_name, obs_name)
            if self.cfg.processing_opts.only_json:
                files_to_convert = col.get_available_coldata_files(var_name)
            else:
                col.run(var_name)
                files_to_convert = col.files_written

            if self.cfg.processing_opts.only_colocation:
                self._log.info(
                    f'FLAG ACTIVE: only_colocation: Skipping '
                    f'computation of json files for {obs_name} /'
                    f'{model_name} combination.')
            else:
                self.make_json_files(files_to_convert)

    def run_evaluation(self, model_name=None, obs_name=None, var_name=None,
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
        var_name : str, optional
            name of variable supposed to be analysed. If None, then all
            variables available for observation network are used (defined in
            :attr:`obs_config` for each entry). Defaults to None.
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
        self.cfg._check_time_config()
        model_list = self.cfg.model_cfg.keylist(model_name)
        obs_list = self.cfg.obs_cfg.keylist(obs_name)

        const.print_log.info('Start processing')

        # compute model maps (completely independent of obs-eval
        # processing below)
        if self.cfg.webdisp_opts.add_maps:
            for model_name in model_list:
                self.run_map_eval(model_name, var_name)

        if not self.cfg.processing_opts.only_maps:
            for obs_name in obs_list:
                for model_name in model_list:
                    self._run_single_entry(model_name, obs_name, var_name)

        if update_interface:
            self.update_interface()
        const.print_log.info('Finished processing.')


    def read_model_data(self, model_name, var_name,
                        **kwargs):
        """Read model variable data

        """
        if not model_name in self.model_config:
            raise ValueError(f'No such model available {model_name}')

        col = Colocator()
        col.update(**self.cfg.colocation_opts)
        col.update(**self.cfg.get_model_config(model_name))
        data = col.read_model_data(var_name, **kwargs)

        return data

    def read_ungridded_obsdata(self, obs_name, vars_to_read=None):
        """Read observation network"""

        col = Colocator()
        col.update(**self.cfg_colocation)
        col.update(**self.obs_config[obs_name])

        data = col.read_ungridded(vars_to_read)
        return data

    def update_interface(self):
        """Update aeroval interface

        Things done here:

            - Update menu file
            - Make aeroval info table json (tab informations in interface)
            - update and order heatmap file
        """
        self.exp_output.update_interface()

    def __str__(self):
        raise NotImplementedError('Under revision')

if __name__ == '__main__':
    stp = ExperimentProcessor('bla', 'blub')
    stp.to_json('/home/jonasg/MyPyaerocom/tmp/')


