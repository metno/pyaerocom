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
from pyaerocom.helpers import get_lowest_resolution
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

    @property
    def model_config(self):
        return self.cfg.model_cfg

    @property
    def obs_config(self):
        return self.cfg.obs_cfg

    @property
    def model_order_menu(self):
        """Order of models in menu

        Note
        ----
        Returns empty list if no specific order is to be used in which case
        the models will be alphabetically ordered
        """
        order = []
        if self.modelorder_from_config:
            order.extend(self.model_config.keys())
        return order

    @property
    def obs_order_menu(self):
        """Order of observations in menu

        Note
        ----
        Returns empty list if no specific order is to be used in which case
        the observations will be alphabetically ordered
        """
        order = []
        if self.obsorder_from_config:
            order.extend(self.obs_config.keys())
        return order




    @property
    def all_model_vars(self):
        """List of unique model variables for processing"""
        mod_vars = self.all_obs_vars
        for mname, mcfg in self.model_config.items():
            for mvar in mcfg.model_use_vars.values():
                if not mvar in mod_vars:
                    mod_vars.append(mvar)
            for mvars in mcfg.model_add_vars.values():
                for mvar in mvars:
                    if not mvar in mod_vars:
                        mod_vars.append(mvar)
        return mod_vars

    @property
    def all_model_map_files(self):
        """List of all jsoncontour and json files associated with model maps"""
        if not os.path.exists(self.out_dirs['contour']):
            raise FileNotFoundError('No data available for this experiment')
        return os.listdir(self.out_dirs['contour'])

    def get_diurnal_only(self, obs_name, colocated_data):
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
            diurnal_only = self.obs_config[obs_name]['diurnal_only']
        except KeyError:
            diurnal_only = False

        ts_type = colocated_data.ts_type
        try:
            if diurnal_only and ts_type != 'hourly':
                raise NotImplementedError
        except:
            const.print_log.warning(
                f'Diurnal processing is only available for ColocatedData with '
                f'ts_type=hourly. Got diurnal_only={diurnal_only} for '
                f'{obs_name} with ts_type {ts_type}.')
        return diurnal_only

    def _get_web_iface_name(self, obs_name):
        """
        Get webinterface name for obs entry

        Note
        ----
        Normally this is the key of the obsentry in :attr:`obs_config`,
        however, it might be specified explicitly via key `web_interface_name`
        in the corresponding value.

        Parameters
        ----------
        obs_name : str
            name of obs entry (must be key in :attr:`obs_config`).

        Returns
        -------
        str
            obs name to be used in the aeroval interface.

        """
        if not 'web_interface_name' in self.obs_config[obs_name]:
            return obs_name
        return self.obs_config[obs_name]['web_interface_name']

    def coldata_to_json(self, file):
        """Creates all json files for one ColocatedData object"""
        coldata = ColocatedData(file)
        obs_var = coldata.metadata['var_name'][0]
        obs_name = coldata.obs_name
        vert_code = self.get_vert_code(obs_name, obs_var)
        web_iface_name = self._get_web_iface_name(obs_name)
        if web_iface_name != obs_name:
            coldata.metadata['obs_name'] = web_iface_name

        if self.main_freq is None:
            self.main_freq = get_lowest_resolution(*self.statistics_freqs)
        diurnal_only = self.get_diurnal_only(obs_name, coldata)

        compute_json_files_from_colocateddata(
                coldata=coldata,
                use_weights=self.weighted_stats,
                vert_code=vert_code,
                out_dirs=self.out_dirs,
                regions_json=self.regions_file,
                diurnal_only=diurnal_only,
                statistics_freqs=self.statistics_freqs,
                statistics_periods=self.statistics_periods,
                main_freq = self.main_freq,
                regions_how=self.regions_how,
                annual_stats_constrained=self.annual_stats_constrained
                )

    def get_vert_code(self, obs_name, obs_var):
        """Get vertical code name for obs / var combination"""
        info =  self.obs_config[obs_name]['obs_vert_type']
        if isinstance(info, str):
            return info
        return info[obs_var]

    @property
    def _heatmap_files(self):
        """
        dict: Dictionary containing heatmap files for this experiment
        """
        dirloc = os.path.join(self.out_dirs['hm'])
        files = {}
        for freq in self.statistics_freqs:
            files[freq] = os.path.join(dirloc, get_heatmap_filename(freq))
        return files

    def update_heatmap_json(self):
        """
        Synchronise content of heatmap json files with content of menu.json

        Raises
        ------
        ValueError
            if this experiment (:attr:`exp_id`) is not registered in menu.json
        """
        for freq, fp in self._heatmap_files.items():
            if not os.path.exists(fp):
                #raise FileNotFoundError(fp)
                const.print_log.warning('Skipping heatmap file {} (for {} freq). '
                                        'File does not exist'.format(fp, freq))
                continue
            menu = read_json(self.menu_file)
            data = read_json(fp)
            hm = {}
            for var, info in menu.items():
                obs_dict = info['obs']
                if not var in hm:
                    hm[var] = {}
                for obs, vdict in obs_dict.items():
                    if not obs in hm[var]:
                        hm[var][obs] = {}
                    for vc, mdict in vdict.items():
                        if not vc in hm[var][obs]:
                            hm[var][obs][vc] = {}
                        for mod, minfo in mdict.items():
                            if not mod in hm[var][obs][vc]:
                                hm[var][obs][vc][mod] = {}
                            modvar = minfo['var']
                            if not modvar in hm[var][obs][vc][mod]:
                                hm[var][obs][vc][mod][modvar] = {}

                            hm_data = data[var][obs][vc][mod][modvar]
                            hm[var][obs][vc][mod][modvar] = hm_data
            write_json(hm, fp, ignore_nan=True)

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
        if model_name:
            mod_cfg = self.cfg.get_model_entry(model_name)
            col.import_from(mod_cfg)
        outdir = self.cfg.path_manager.get_coldata_dir()
        col.basedir_coldata = outdir
        return col

    def _check_and_get_iface_names(self):
        """
        Get aeroval interface names of all observations.

        Raises
        ------
        ValueError
            if value of one obsentry name is not a string.

        Returns
        -------
        iface_names : list
            list of obs names used in the aeroval interface.

        """
        obs_list = list(self.obs_config)
        iface_names = []
        for obs_name in obs_list:
            try:
                if self.obs_config[obs_name]['web_interface_name'] == None:
                    self.obs_config[obs_name]['web_interface_name'] = obs_name
                else:
                    pass
            except KeyError:
                self.obs_config[obs_name]['web_interface_name'] = obs_name
            if not isinstance(self.obs_config[obs_name]['web_interface_name'], str):
                raise ValueError(
                    f'Invalid value for web_iface_name in {obs_name}. Need str.'
                    )
            iface_names.append(self.obs_config[obs_name]['web_interface_name'])
        iface_names = list(set(iface_names))
        return iface_names

    @property
    def iface_names(self):
        """
        List of observation dataset names used in aeroval interface
        """
        return self._check_and_get_iface_names()

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

        if self.obs_config[obs_name]['is_superobs']:
            try:
                self._run_superobs_entry(model_name, obs_name, var_name,
                                         try_colocate_if_missing=True)
            except Exception:
                if self.raise_exceptions:
                    raise
                const.print_log.warning(
                    'failed to process superobs...')
        elif self.obs_config[obs_name]['only_superobs']:
            const.print_log.info(
                f'Skipping json processing of {obs_name}, as this is '
                f'marked to be used only as part of a superobs '
                f'network')
        else:
            col = self.init_colocator(model_name, obs_name)
            if self.cfg.processing_opts.only_json:
                files_to_convert = col.get_available_coldata_files()
            else:
                col.run(var_name)
                files_to_convert = col.files_written

            if self.cfg.processing_opts.only_colocation:
                self._log.info(
                    f'FLAG ACTIVE: only_colocation: Skipping '
                    f'computation of json files for {obs_name} /'
                    f'{model_name} combination.')
                return
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

    @staticmethod
    def _info_from_map_file(filename):
        spl = os.path.basename(filename).split('.json')[0].split('_')
        if not len(spl) == 3:
            raise FileConventionError(
                f'Invalid map filename: {filename}'
                )
        obsinfo = spl[0]
        vert_code = spl[1]
        modinfo = spl[2]

        mspl = modinfo.split('-')
        mvar = mspl[-1]
        mname = '-'.join(mspl[:-1])

        ospl = obsinfo.split('-')
        ovar = ospl[-1]
        oname = '-'.join(ospl[:-1])
        return (oname, ovar, vert_code, mname, mvar)

    def _get_var_name_and_type(self, var_name):
        """Get menu name and type of observation variable

        Parameters
        ----------
        var_name : str
            Name of variable

        Returns
        -------
        str
            menu name of this variable
        str
            vertical type of this variable (2D, 3D)
        str
            variable category

        """

        try:
            name, tp, cat = self.var_mapping[var_name]
        except Exception:
            name, tp, cat = var_name, 'UNDEFINED', 'UNDEFINED'
            self._log.warning(
                'Missing menu name definition for var {var_name}.')
        return (name, tp, cat)

    def update_interface(self):
        """Update aeroval interface

        Things done here:

            - Update menu file
            - Make aeroval info table json (tab informations in interface)
            - update and order heatmap file
        """
        self.update_menu()
        try:
            self.make_info_table_web()
            self.update_heatmap_json()
            self.to_json(self.exp_dir)
        except KeyError: # if no data is available for this experiment
            pass

    def update_menu(self):
        """Update menu

        The menu.json file is created based on the available json map files in the
        map directory of an experiment.

        Parameters
        ----------
        menu_file : str
            path to json menu file
        delete_mode : bool
            if True, then no attempts are being made to find json files for the
            experiment specified in `config`.

        """
        avail = self._get_available_results_dict()
        avail = self._sort_menu_entries(avail)
        write_json(avail, self.menu_file, indent=4)

    def _sort_menu_entries(self, avail):
        """
        Used in method :func:`update_menu_evaluation_iface`

        Sorts results of different menu entries (i.e. variables, observations
        and models).

        Parameters
        ----------
        avail : dict
            nested dictionary contining info about available results
        config : AerocomEvaluation
            Configuration class

        Returns
        -------
        dict
            input dictionary sorted in variable, obs and model layers. The order
            of variables, observations and models may be specified in
            AerocomEvaluation class and if not, alphabetic order is used.

        """
        # sort first layer (i.e. variables)
        avail = sort_dict_by_name(avail, pref_list=config.var_order_menu)

        new_sorted = {}
        for var, info in avail.items():
            new_sorted[var] = info
            obs_order = config.obs_order_menu
            sorted_obs = sort_dict_by_name(info['obs'],
                                           pref_list=obs_order)
            new_sorted[var]['obs'] = sorted_obs
            for obs_name, vert_codes in sorted_obs.items():
                vert_codes_sorted = sort_dict_by_name(vert_codes)
                new_sorted[var]['obs'][obs_name] = vert_codes_sorted
                for vert_code, models in vert_codes_sorted.items():
                    model_order = config.model_order_menu
                    models_sorted = sort_dict_by_name(models,
                                                      pref_list=model_order)
                    new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
        return new_sorted

    def _get_meta_from_map_files(self):
        """List of all existing map files"""
        dirloc = self.out_dirs['map']
        if not os.path.exists(dirloc):
            raise FileNotFoundError('No data available for this experiment')
        files = glob.glob(f'{dirloc}/*.json')
        tab = []
        if len(files) > 0:
            obs_names = self.iface_names
            obs_vars = self.all_obs_vars
            mod_names = self.all_model_names
            mod_vars = self.all_model_vars

            for file in files:
                (obs_name, obs_var,
                 vert_code,
                 mod_name, mod_var) = self._info_from_map_file(file)

                if not mod_name in mod_names:
                    const.print_log.warning(
                        f'Found outdated json map file (model name): {file}. '
                        f'Will be ignored'
                        )
                    continue
                elif not obs_name in obs_names:
                    const.print_log.warning(
                        f'Found outdated json map file (obs name): {file}. '
                        f'Will be ignored'
                        )
                    continue
                elif not obs_var in obs_vars:
                    const.print_log.warning(
                        f'Found outdated json map file (obs var): {file}. '
                        f'Will be ignored'
                        )
                    continue
                elif not mod_var in mod_vars:
                    const.print_log.warning(
                        f'Found outdated json map file (mod var): {file}. '
                        f'Will be ignored'
                        )
                    continue
                tab.append([obs_var, obs_name, vert_code, mod_name, mod_var])
        return tab

    def _get_available_results_dict(self):
        def var_dummy():
            """Helper that creates empty dict for variable info"""
            return {'type'      :   '',
                    'cat'       :   '',
                    'name'      :   '',
                    'longname'  :   '',
                    'obs'       :   {}}
        new = {}
        tab = self._get_meta_from_map_files()
        for row in tab:
            obs_var, obs_name, vert_code, mod_name, mod_var = row
            modvarname = mod_var + '*' if mod_var != obs_var else mod_var
            if not modvarname in new:
                new[modvarname] = d = var_dummy()
                name, tp, cat = self._get_var_name_and_type(mod_var)
                d['name'] = name
                d['type'] = tp
                d['cat']  = cat
                d['longname'] = const.VARS[mod_var].description
            else:
                d = new[modvarname]

            if not obs_name in d['obs']:
                d['obs'][obs_name] = dobs = {}
            else:
                dobs = d['obs'][obs_name]
            if not obs_var in dobs:
                dobs[obs_var] = dobsvar = {}
            else:
                dobsvar = dobs[obs_var]
            if not vert_code in dobsvar:
                dobsvar[vert_code] = dobs_vert = {}
            else:
                dobs_vert = dobsvar[vert_code]
            model_id = self.model_config[mod_name]['model_id']
            dobs_vert[mod_name] = {'model_id'  : model_id,
                                   'model_var' : mod_var,
                                   'obs_var'   : obs_var}
        return new

    def make_info_table_evaluation_iface(self):
        """
        Make an information table for an aeroval experiment based on menu.json

        Returns
        -------
        dict
            dictionary containing meta information

        """
        if not os.path.exists(self.menu_file):
            raise FileNotFoundError(f'No menu.json found for {self.exp_id}')

        SKIP_META = ['data_source', 'var_name', 'lon_range',
                     'lat_range', 'alt_range']
        menu = read_json(self.menu_file)
        with open(self.menu_file, 'r') as f:
            menu = simplejson.load(f)
        table = {}
        for obs_var, info in exp.items():
            for obs_name, vert_types in info['obs'].items():
                for vert_type, models in vert_types.items():
                    for mname, minfo in models.items():
                        if not mname in table:
                            table[mname] = mi = {}
                            mi['id'] = model_id = minfo['id']
                        else:
                            mi = table[mname]
                            model_id = mi['id']
                            if minfo['id'] != mi['id']:
                                raise KeyError('Unexpected error: conflict in model ID and name')

                        try:
                            mo = mi['obs']
                        except Exception:
                            mi['obs'] = mo = {}
                        if 'var' in minfo:
                            mvar = minfo['var']
                        else:
                            mvar = obs_var
                        if not obs_var in mo:
                            mo[obs_var] = oi = {}
                        else:
                            oi = mo[obs_var]
                        if obs_name in oi:
                            raise Exception
                        oi[obs_name] = motab = {}
                        motab['model_var'] = mvar
                        motab['obs_id'] = config.get_obs_id(obs_name)
                        files = glob.glob('{}/{}/{}*REF-{}*.nc'
                                          .format(config.coldata_dir,
                                                  model_id, mvar, obs_name))

                        if not len(files) == 1:
                            if len(files) > 1:
                                motab['MULTIFILES'] = len(files)
                            else:
                                motab['NOFILES'] = True
                            continue

                        coldata = ColocatedData(files[0])
                        for k, v in coldata.metadata.items():
                            if not k in SKIP_META:
                                if isinstance(v, (list, tuple)):
                                    if len(v) == 2:
                                        motab['{}_obs'.format(k)] = str(v[0])
                                        motab['{}_mod'.format(k)] = str(v[1])
                                    else:
                                        motab[k] = ';'.join([str(x) for x in v])
                                else:
                                    motab[k] = str(v)
        return table

    def make_info_table_web(self):
        """Make and safe table with detailed infos about processed data files

        The table is stored in as file minfo.json in directory :attr:`exp_dir`.
        """
        table = make_info_table_evaluation_iface(self)
        outname = os.path.join(self.exp_dir, 'minfo.json')
        write_json()
        with open(outname, 'w+') as f:
            f.write(simplejson.dumps(table, indent=2))
        return table

    def _obs_config_asdict(self):
        output = {}
        for k, cfg in self.obs_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            output[k] = as_dict
        return output

    def _model_config_asdict(self):
        output = {}
        for k, cfg in self.model_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            output[k] = as_dict
        return output

    def delete_experiment_data(self, base_dir=None, proj_id=None, exp_id=None,
                               also_coldata=True):
        """Delete all data associated with a certain experiment

        Parameters
        ----------
        base_dir : str, optional
            basic output direcory (containing subdirs of all projects)
        proj_name : str, optional
            name of project, if None, then this project is used
        exp_name : str, optional
            name experiment, if None, then this project is used
        also_coldata : bool
            if True and if output directory for colocated data is default and
            specific for input experiment ID, then also all associated colocated
            NetCDF files are deleted. Defaults to True.
        """
        if proj_id is None:
            proj_id = self.proj_id
        if exp_id is None:
            exp_id = self.exp_id
        if base_dir is None:
            base_dir = self.out_basedir
        try:
            delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)
        except NameError:
            pass
        if also_coldata:
            coldir = self.cfg_colocation['basedir_coldata']
            chk = os.path.normpath(f'{self.proj_id}/{self.exp_id}')
            if os.path.normpath(coldir).endswith(chk) and os.path.exists(coldir):
                const.print_log.info(f'Deleting everything under {coldir}')
                shutil.rmtree(coldir)
        self.update_menu(delete_mode=True)

    def _clean_modelmap_files(self):
        all_vars = self.all_modelmap_vars
        all_mods = self.all_model_names
        out_dir = self.out_dirs['contour']

        for file in os.listdir(out_dir):
            spl = file.replace('.', '_').split('_')
            if not len(spl) == 4:
                raise ValueError(f'Invalid json map filename {file}')
            var, vc, mod_name = spl[:3]
            rm = (not var in all_vars or
                  not mod_name in all_mods or
                  not vc in self.JSON_SUPPORTED_VERT_SCHEMES)
            if rm:
                const.print_log.info(
                    f'Removing invalid model maps file {file}'
                    )
                os.remove(os.path.join(out_dir, file))

    def clean_json_files(self, update_interface=False):
        """Checks all existing json files and removes outdated data

        This may be relevant when updating a model name or similar.
        """
        self._clean_modelmap_files()

        for file in self.all_map_files:
            (obs_name, obs_var, vc,
             mod_name, mod_var) = self._info_from_map_file(file)

            remove=False
            if not (obs_name in self.iface_names and
                    mod_name in self.model_config):
                remove = True
            elif not obs_var in self._get_valid_obs_vars(obs_name):
                remove = True
            elif not vc in self.JSON_SUPPORTED_VERT_SCHEMES:
                remove = True
            else:
                mcfg = self.model_config[mod_name]
                if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                    if not mod_var == mcfg['model_use_vars'][obs_var]:
                        remove=True

            if remove:
                const.print_log.info(f'Removing outdated map file: {file}')
                os.remove(os.path.join(self.out_dirs['map'], file))

        for fp in glob.glob('{}/*.json'.format(self.out_dirs['ts'])):
            self._check_clean_ts_file(fp)

        if update_interface:
            self.update_interface()

    def _get_valid_obs_vars(self, obs_name):
        if obs_name in self._valid_obs_vars:
            return self._valid_obs_vars[obs_name]

        obs_vars = self.obs_config[obs_name]['obs_vars']
        add = []
        for mname, mcfg in self.model_config.items():
            if 'model_add_vars' in mcfg:
                for ovar, mvar in mcfg['model_add_vars'].items():
                    if ovar in obs_vars and not mvar in add:
                        add.append(mvar)
        obs_vars.extend(add)
        self._valid_obs_vars[obs_name]  = obs_vars
        return obs_vars

    def _check_clean_ts_file(self, fp):
        spl = os.path.basename(fp).split('OBS-')[-1].split(':')
        obs_name = spl[0]
        obs_var, vc, _ = spl[1].replace('.', '_').split('_')
        rm = (not vc in self.JSON_SUPPORTED_VERT_SCHEMES or
              not obs_name in self.obs_config or
              not obs_var in self._get_valid_obs_vars(obs_name))
        if rm:
            const.print_log.info('Removing outdated ts file: {}'.format(fp))
            os.remove(fp)
            return
        try:
            data = read_json(fp)
        except Exception:
            const.print_log.exception('FATAL: detected corrupt json file: {}. '
                                      'Removing file...'.format(fp))
            os.remove(fp)
            return
        if all([x in self.model_config for x in list(data.keys())]):
            return
        data_new = {}
        for mod_name in data.keys():
            if not mod_name in self.model_config:
                const.print_log.info('Removing model {} from {}'
                                .format(mod_name, os.path.basename(fp)))
                continue

            data_new[mod_name] = data[mod_name]

        write_json(data_new, fp)

    def to_dict(self):
        """Convert configuration to dictionary"""
        d = {}
        for key, val in self.__dict__.items():
            if key in self.JSON_CFG_IGNORE:
                continue
            elif isinstance(val, dict):
                if key == 'model_config':
                    sub = self._model_config_asdict()
                elif key == 'obs_config':
                    sub = self._obs_config_asdict()
                else:
                    sub = {}
                    for k, v in val.items():
                        if v is not None:
                            sub[k] = v
                d[key] = sub
            else:
                d[key] = val
        return d

    @property
    def name_config_file(self):
        """
        File name of config file (without file ending specification)

        Returns
        -------
        str
            name of config file
        """
        return

    @property
    def name_config_file_json(self):
        """
        File name of config file (with json ending)

        Returns
        -------
        str
            name of config file
        """
        return '{}.json'.format(self.name_config_file)

    def __str__(self):
        raise NotImplementedError('Under revision')

if __name__ == '__main__':
    stp = ExperimentProcessor('bla', 'blub')
    stp.to_json('/home/jonasg/MyPyaerocom/tmp/')


