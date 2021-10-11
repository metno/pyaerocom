import os
from time import time

from pyaerocom import ColocatedData, const
from pyaerocom._lowlevel_helpers import write_json
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import _init_meta_glob, \
    init_regions_web, update_regions_json, _init_data_default_frequencies, \
    _apply_annual_constraint, _process_statistics_timeseries, _add_entry_json, \
    _process_heatmap_data, get_heatmap_filename, _process_regional_timeseries, \
    _write_site_data, _process_sites, _process_map_and_scat, get_json_mapname, \
    _process_sites_weekly_ts, _write_stationdata_json
from pyaerocom.exceptions import AeroValConfigError, TemporalResolutionError


class ColdataToJsonEngine(ProcessingEngine):

    def run(self, files):
        """
        Convert colocated data files to json

        Parameters
        ----------
        files : list
            list of file paths pointing to colocated data objects to be
            processed.

        Returns
        -------
        list
            list of files that have been converted.

        """
        converted = []
        for file in files:
            const.print_log.info(f'Processing: {file}')
            coldata = ColocatedData(file)
            self.process_coldata(coldata)
            converted.append(file)
        return converted

    def process_coldata(self, coldata: ColocatedData):
        """
        Creates all json files for one ColocatedData object

        Parameters
        ----------
        coldata : ColocatedData
            colocated data to be processed.

        Raises
        ------
        NotImplementedError
            DESCRIPTION.
        ValueError
            DESCRIPTION.
        AeroValConfigError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        t00 = time()
        use_weights = self.cfg.statistics_opts.weighted_stats
        # redundant, but cheap and important to be correct
        self.cfg._check_time_config()
        freqs = self.cfg.time_cfg.freqs
        periods = self.cfg.time_cfg.periods
        seasons = self.cfg.time_cfg.get_seasons()
        main_freq = self.cfg.time_cfg.main_freq
        annual_stats_constrained = self.cfg.statistics_opts.annual_stats_constrained

        out_dirs = self.cfg.path_manager.get_json_output_dirs(True)
        regions_json = self.exp_output.regions_file
        regions_how = self.cfg.webdisp_opts.regions_how

        stats_min_num = self.cfg.statistics_opts.MIN_NUM


        vert_code = coldata.get_meta_item('vert_code')
        diurnal_only = coldata.get_meta_item('diurnal_only')

        add_trends = self.cfg.statistics_opts.add_trends
        trends_min_yrs = self.cfg.statistics_opts.trends_min_yrs

        # ToDo: some of the checks below could be done automatically in
        # EvalSetup, and at an earlier stage
        if vert_code == 'ModelLevel':
            raise NotImplementedError('Coming (not so) soon...')

        # this will need to be figured out as soon as there is altitude
        elif 'altitude' in coldata.data.dims:
            raise NotImplementedError('Cannot yet handle profile data')

        elif not isinstance(coldata, ColocatedData):
            raise ValueError('Need ColocatedData object, got {}'
                             .format(type(coldata)))

        elif coldata.has_latlon_dims and regions_how=='country':
            raise NotImplementedError('Cannot yet apply country filtering for '
                                      '4D colocated data instances')
        elif not main_freq in freqs:
            raise AeroValConfigError(
                f'Scatter plot frequency {main_freq} is not in '
                f'experiment frequencies: {freqs}'
                )
        if self.cfg.statistics_opts.stats_tseries_base_freq is not None:
            if not self.cfg.statistics_opts.stats_tseries_base_freq in freqs:
                raise AeroValConfigError(
                    f'Base frequency for statistics timeseries needs to be '
                    f'specified in experiment frequencies: {freqs}')
        # init some stuff
        if 'var_name' in coldata.metadata:
            obs_var = coldata.metadata['var_name'][0]
            model_var = coldata.metadata['var_name'][1]
        else:
            obs_var = model_var = 'UNDEFINED'

        model_name = coldata.model_name
        obs_name = coldata.obs_name

        mcfg = self.cfg.model_cfg.get_entry(model_name)
        var_name_web = mcfg.get_varname_web(model_var, obs_var)

        const.print_log.info(
            f'Computing json files for {model_name} ({model_var}) vs. '
            f'{obs_name} ({obs_var})'
            )

        meta_glob = _init_meta_glob(coldata,
                                    vert_code=vert_code,
                                    obs_name=obs_name,
                                    model_name=model_name,
                                    var_name_web=var_name_web)

        # get region IDs
        (regborders, regs, regnames) = init_regions_web(coldata, regions_how)

        update_regions_json(regborders, regions_json)

        use_country = True if regions_how == 'country' else False

        data = _init_data_default_frequencies(coldata,
                                              freqs)
        if annual_stats_constrained:
            data = _apply_annual_constraint(data)

        if not diurnal_only:
            const.print_log.info('Processing statistics timeseries for all regions')
            input_freq = self.cfg.statistics_opts.stats_tseries_base_freq
            try:
                stats_ts = _process_statistics_timeseries(
                    data=data,
                    freq=main_freq,
                    region_ids=regnames,
                    use_weights=use_weights,
                    use_country=use_country,
                    data_freq=input_freq)
            except TemporalResolutionError:
                stats_ts = {}

            ts_file = os.path.join(out_dirs['hm/ts'], 'stats_ts.json')
            _add_entry_json(ts_file, stats_ts, obs_name, var_name_web,
                            vert_code, model_name, model_var)

            const.print_log.info('Processing heatmap data for all regions')
            hm_all = _process_heatmap_data(data, regnames, use_weights,
                                           use_country, meta_glob,
                                           periods,
                                           seasons,
                                           add_trends,
                                           trends_min_yrs,
                                           )

            for freq, hm_data in hm_all.items():
                fname = get_heatmap_filename(freq)

                hm_file = os.path.join(out_dirs['hm'], fname)

                _add_entry_json(hm_file, hm_data, obs_name, var_name_web,
                                vert_code, model_name, model_var)

            const.print_log.info('Processing regional timeseries for all regions')
            ts_objs_regional = _process_regional_timeseries(data,
                                                            regnames,
                                                            regions_how,
                                                            meta_glob)

            _write_site_data(ts_objs_regional, out_dirs['ts'])
            if coldata.has_latlon_dims:
                for cd in data.values():
                    if cd is not None:
                        cd.data = cd.flatten_latlondim_station_name().data

            const.print_log.info('Processing individual site timeseries data')
            (ts_objs,
             map_meta,
             site_indices) = _process_sites(data, regs, regions_how, meta_glob)

            _write_site_data(ts_objs, out_dirs['ts'])

            map_data, scat_data = _process_map_and_scat(data, map_meta,
                                                        site_indices,
                                                        periods,
                                                        main_freq,
                                                        stats_min_num,
                                                        seasons,
                                                        add_trends,
                                                        trends_min_yrs,
                                                        )

            map_name = get_json_mapname(obs_name, var_name_web, model_name,
                                        model_var, vert_code)

            outfile_map =  os.path.join(out_dirs['map'], map_name)
            write_json(map_data, outfile_map, ignore_nan=True)

            outfile_scat =  os.path.join(out_dirs['scat'], map_name)
            write_json(scat_data, outfile_scat, ignore_nan=True)

        if coldata.ts_type == 'hourly':
            const.print_log.info('Processing diurnal profiles')
            (ts_objs_weekly,
             ts_objs_weekly_reg) = _process_sites_weekly_ts(coldata, regions_how,
                                                            regnames, meta_glob)
            outdir = os.path.join(out_dirs['ts/diurnal'])
            for ts_data_weekly in ts_objs_weekly:
                #writes json file
                _write_stationdata_json(ts_data_weekly, outdir)
            if ts_objs_weekly_reg != None:
                for ts_data_weekly_reg in ts_objs_weekly_reg:
                    #writes json file
                    _write_stationdata_json(ts_data_weekly_reg, outdir)

        const.print_log.info(
            f'Finished computing json files for {model_name} ({model_var}) vs. '
            f'{obs_name} ({obs_var})'
            )

        dt = time() - t00
        const.print_log.info(f'Time expired (TOTAL): {dt:.2f} s')