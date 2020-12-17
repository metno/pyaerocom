#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level module containing analysis classes and methods to perform
colocation.

NOTE
----

This module will be deprecated soon but most of the code will be refactored
into colocation.py module.
"""
from datetime import datetime
import numpy as np
import os
import traceback

from pyaerocom._lowlevel_helpers import BrowseDict, chk_make_subdir
from pyaerocom import const, print_log
from pyaerocom.helpers import (to_pandas_timestamp, to_datestring_YYYYMMDD,
                               get_lowest_resolution, start_stop)
from pyaerocom.io.helpers import get_all_supported_ids_ungridded
from pyaerocom.colocation import (colocate_gridded_gridded,
                                  colocate_gridded_ungridded,
                                  correct_model_stp_coldata)
from pyaerocom.colocateddata import ColocatedData

from pyaerocom.filter import Filter
from pyaerocom.io import ReadUngridded, ReadGridded, ReadMscwCtm
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import (DataCoverageError,
                                  VariableDefinitionError)

class ColocationSetup(BrowseDict):
    """Setup class for model / obs intercomparison

    An instance of this setup class can be used to run a colocation analysis
    between a model and an observation network and will create a number of
    :class:`pya.ColocatedData` instances and save them as netCDF file.

    Note
    ----
    This is a very first draft and will likely undergo significant changes

    Attributes
    ----------
    model_id : str
        ID of model to be used
    obs_id : str
        ID of observation network to be used
    obs_vars : :obj:`str` or :obj:`list`, optional
        variables to be analysed. If any of the provided variables to be
        analysed in the model data is not available in obsdata, the obsdata
        will be checked against potential alternative variables which are
        specified in :attr:`model_use_vars` and which can be specified in form of a
        dictionary for each . If None, all
        variables are analysed that are available both in model and obsdata.
    ts_type
        string specifying colocation frequency
    start
        start time. Input can be anything that can be converted into
        :class:`pandas.Timestamp` using
        :func:`pyaerocom.helpers.to_pandas_timestamp`. If None, than the first
        available date in the model data is used.
    stop
        stop time. Anything that can be converted into
        :class:`pandas.Timestamp` using
        :func:`pyaerocom.helpers.to_pandas_timestamp` or None. If None and if
        ``start`` is on resolution of year (e.g. ``start=2010``) then ``stop``
        will be automatically set to the end of that year. Else, it will be
        set to the last available timestamp in the model data.
    filter_name : str
        name of filter to be applied. If None, AeroCom default is used
        (i.e. `pyaerocom.const.DEFAULT_REG_FILTER`)
    regrid_res_deg : :obj:`int`, optional
        resolution in degrees for regridding of model grid (done before
        colocation)
    remove_outliers : bool
        if True, outliers are removed from model and obs data before colocation,
        else not.
    vert_scheme : :obj:`str`, optional
        vertical scheme used for colocation
    harmonise_units : bool
        if True, units are attempted to be harmonised (note: raises Exception
        if True and units cannot be harmonised).
    model_use_vars : :obj:`dict`, optional
        dictionary that specifies mapping of model variables. Keys are
        observation variables, values are the corresponding model variables
        (e.g. model_use_vars=dict(od550aer='od550csaer')). Example: your
        observation has var *od550aer* but your model model uses a different
        variable name for that variable, say *od550*. Then, you can specify
        this via `model_use_vars = {'od550aer' : 'od550'}. NOTE: in this case,
        a model variable *od550aer* will be ignored, even if it exists
        (cf :attr:`model_add_vars`).
    model_read_aux : :obj:`dict`, optional
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys
        `vars_required` (list of required variables for computation of var
        and `fun` (method that takes list of read data objects and computes
        and returns var)
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).
    obs_vert_type : str or dict, optional
        Aerocom vertical code encoded in the model filenames (only AeroCom 3
        and later). Specifies which model file should be read in case there are
        multiple options (e.g. surface level data can be read from a
        *Surface*.nc file as well as from a *ModelLevel*.nc file). If input is
        string (e.g. 'Surface'), then the corresponding vertical type code is
        used for reading of all variables that are colocated (i.e. that are
        specified in :attr:`obs_vars`). Else (if input is dictionary, e.g.
        `obs_vert_type=dict(od550aer='Column', ec550aer='ModelLevel')`),
        information is extracted variable specific, for those who are defined
        in the dictionary, for all others, `None` is used.
    model_vert_type_alt : str or dict, optional
        like :attr:`obs_vert_type` but is used in case of exception cases, i.e.
        where the `obs_vert_type` is not available in the models.
    var_outlier_ranges : :obj:`dict`, optional
        dictionary specifying outlier ranges for individual variables.
        (e.g. dict(od550aer = [-0.05, 10], ang4487aer=[0,4]))
    model_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the
        model data. Not to be confused with :attr:`ts_type`, which specifies
        the frequency used for colocation. Can be specified variable specific
        by providing a dictionary.
    obs_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the
        observation data (so far, this does only apply to gridded obsdata such
        as satellites). For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Not to be confused with :attr:`ts_type`, which specifies the
        frequency used for colocation. Can be specified variable specific in
        form of dictionary.
    flex_ts_type_gridded : bool
        boolean specifying whether reading frequency of gridded data is
        allowed to be flexible. This includes all gridded data, whether it is
        model or gridded observation (e.g. satellites). Defaults to True.
    apply_time_resampling_constraints : bool, optional
        if True, then time resampling constraints are applied as provided via
        :attr:`min_num_obs` or if that one is unspecified, as defined in
        :attr:`pyaerocom.const.OBS_MIN_NUM_RESAMPLE`. If None, than
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used
        (which defaults to True !!).
    min_num_obs : dict or int, optional
        time resampling constraints applied if input arg
        `apply_time_resampling_constraints` is True - or None, in which case
        :attr:`pyaerocom.const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` is used.
    resample_how : str or dict
        string specifying how data should be aggregated when resampling in time.
        Default is "mean". Can also be a nested dictionary, e.g.
        resample_how={'conco3': 'daily': {'hourly' : 'max'}}} would use the
        maximum value to aggregate from hourly to daily for variable conco3,
        rather than the mean.
    model_keep_outliers : bool
        if True, no outliers are removed from model data
    obs_keep_outliers : bool
        if True, no outliers are removed from obs / reference data
    obs_use_climatology : bool
        BETA if True, pyaerocom default climatology is computed from observation
        stations (so far only possible for unrgidded / gridded colocation)
    colocate_time : bool
        if True and if obs and model sampling frequency (e.g. daily) are higher
        than input colocation frequency (e.g. monthly), then the datasets are
        first colocated in time (e.g. on a daily basis), before the monthly
        averages are calculated. Default is False.
    basedir_coldata : str
        base directory for storing of colocated data files
    obs_name : str, optional
        if provided, this string will be used in colocated data filename to
        specify obsnetwork, else obs_id will be used
    model_name : str, optional
        if provided, this string will be used in colocated data filename to
        specify model, else obs_id will be used
    save_coldata : bool
        if True, colocated data objects are saved as NetCDF file.
    """
    #: Dictionary specifying alternative vertical types that may be used to
    #: read model data. E.g. consider the variable is  ec550aer,
    #: obs_vert_type='Surface' and obs_vert_type_alt=dict(Surface='ModelLevel').
    #: Now, if a model that is used for the analysis does not contain a data
    #: file for ec550aer at the surface ('*ec550aer*Surface*.nc'), then, the
    #: colocation routine will look for '*ec550aer*ModelLevel*.nc' and if this
    #: exists, it will load it and extract the surface level.
    OBS_VERT_TYPES_ALT = {'Surface'    :   'ModelLevel'}

    def __init__(self, model_id=None, obs_id=None, obs_vars=None,
                 ts_type=None, start=None, stop=None,
                 filter_name=None,
                 regrid_res_deg=None, remove_outliers=True,
                 vert_scheme=None, harmonise_units=False,
                 model_use_vars=None, model_add_vars=None,
                 model_read_aux=None, read_opts_ungridded=None,
                 obs_vert_type=None, model_vert_type_alt=None,
                 var_outlier_ranges=None, var_ref_outlier_ranges=None,
                 model_ts_type_read=None,
                 obs_ts_type_read=None, flex_ts_type_gridded=True,
                 apply_time_resampling_constraints=None, min_num_obs=None,
                 model_keep_outliers=True,
                 obs_keep_outliers=False,
                 obs_use_climatology=False,
                 colocate_time=False, basedir_coldata=None,
                 obs_name=None, model_name=None,
                 save_coldata=True, **kwargs):

        if isinstance(obs_vars, str):
            obs_vars = [obs_vars]
        try:
            Filter(filter_name)
        except Exception:
            raise ValueError('Invalid input for filter_name {}'.format(filter_name))
        self.save_coldata = save_coldata
        if save_coldata:
            if basedir_coldata is None:
                basedir_coldata = const.COLOCATEDDATADIR
            if not os.path.exists(basedir_coldata):
                const.print_log.info('Creating directory: {}'.format(basedir_coldata))
                os.mkdir(basedir_coldata)

        self._obs_cache_only = False
        self.obs_vars = obs_vars
        self.obs_vert_type = obs_vert_type
        self.model_vert_type_alt = model_vert_type_alt
        self.read_opts_ungridded = read_opts_ungridded
        self.obs_ts_type_read = obs_ts_type_read

        self.model_use_vars = model_use_vars
        self.model_add_vars = model_add_vars
        self.model_keep_outliers = model_keep_outliers
        self.model_to_stp = False

        self.model_id = model_id
        self.model_name = model_name
        self.model_data_dir = None

        self.obs_id = obs_id
        self.obs_name = obs_name
        self.obs_data_dir = None
        self.obs_keep_outliers = obs_keep_outliers
        self.obs_use_climatology = obs_use_climatology
        self.obs_add_meta = []

        self.gridded_reader_id = {
         'model' : 'ReadGridded',
         'obs' : 'ReadGridded'}

        self.start = start
        self.stop = stop

        self.ts_type = ts_type

        self.filter_name = filter_name

        self.remove_outliers = remove_outliers

        # OPtions related to time resampling
        self.apply_time_resampling_constraints=apply_time_resampling_constraints
        self.min_num_obs=min_num_obs
        self.resample_how=None

        self.var_outlier_ranges = var_outlier_ranges
        self.var_ref_outlier_ranges = var_ref_outlier_ranges

        self.harmonise_units = harmonise_units
        self.vert_scheme = vert_scheme
        self.regrid_res_deg = regrid_res_deg
        self.ignore_station_names = None

        self.basedir_coldata = basedir_coldata

        self.model_ts_type_read = model_ts_type_read
        self.model_read_aux = model_read_aux
        self.model_use_climatology = False

        self.colocate_time = colocate_time
        self.flex_ts_type_gridded = True
        #: If True, existing colocated data files will be re-computed and overwritten
        self.reanalyse_existing = False
        #: If True, the colocation routine will raise any Exception that may occur,
        #: else (False), expected expcetions will be ignored and logged.
        self.raise_exceptions = False

        self.update(**kwargs)

    @property
    def basedir_logfiles(self):
        """Base directory for storing logfiles"""
        p = chk_make_subdir(self.basedir_coldata, 'logfiles')
        return p

    @property
    def UNGRIDDED_IDS(self):
        """ID's of all supported ungridded datasets"""
        return get_all_supported_ids_ungridded()

    def __dir__(self):
        return self.keys()

    def update(self, **kwargs):
        for key, val in kwargs.items():
            if key in self and isinstance(self[key], dict):
                if not isinstance(val, dict):
                    raise ValueError('Cannot update dict {} with non-dict input {}'
                                     .format(key, val))
                self[key].update(val)
            else:
                self[key] = val
        sd = self.basedir_coldata
        if isinstance(sd, str) and not os.path.exists(sd):
            os.mkdir(sd)

class Colocator(ColocationSetup):
    """High level class for running colocation

    Note
    ----
    This object inherits from :class:`ColocationSetup` and is also instantiated
    as such. For attributes, please see base class.
    """


    SUPPORTED_GRIDDED_READERS = {
        'ReadGridded' : ReadGridded,
        'ReadMscwCtm' : ReadMscwCtm
    }


    def __init__(self, **kwargs):
        super(Colocator, self).__init__(**kwargs)

        self._log = None
        self.logging = True
        self.data = {}

        self.file_status = {}

    def _write_log(self, msg):
        if self.logging:
            try:
                self._log.write(msg)
            except Exception as e:
                const.print_log.warning('Deactivating logging in Colocator. Reason: {}'
                                        .format(repr(e)))

    def run(self, var_name=None, **opts):
        """Perform colocation for current setup

        The current setup comprises at least

        Parameters
        ----------
        **opts
            keyword args that may be specified to change the current setup
            before colocation

        """
        self.update(**opts)
        # ToDo: setting the defaults for time resampling here should be
        # unnecessary since this is done in TimeResampler. Ensure that and
        # remove here
        if self.apply_time_resampling_constraints is None:
            self.apply_time_resampling_constraints = const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS

        if self.apply_time_resampling_constraints is True and self.min_num_obs is None:
            self.min_num_obs = const.OBS_MIN_NUM_RESAMPLE

        try:
            self._init_log()
        except Exception as e:
            const.print_log.warning('Deactivating logging in Colocator. Reason: {}'
                                    .format(repr(e)))
            self.logging = False

        self._write_log('\n\nModel: {}\n'.format(self.model_id))
        try:
            if self.obs_id in self.UNGRIDDED_IDS:
                self.data[self.model_id] = self._run_gridded_ungridded(var_name)
            else:
                self.data[self.model_id] = self._run_gridded_gridded(var_name)
        except Exception:
            msg = ('Failed to perform analysis: {}\n'
                   .format(traceback.format_exc()))
            const.print_log.warning(msg)
            self._write_log(msg)
            if self.raise_exceptions:
                self._close_log()
                raise Exception(traceback.format_exc())
        finally:
            self._close_log()

    def instantiate_gridded_reader(self, what):
        """
        Create reader for model or observational gridded data.

        Parameters
        ----------
        what : str
            Type of reader. ("model" or "obs")

        Returns
        -------
        Instance of reader class defined in self.SUPPORTED_GRIDDED_READERS
        """
        if what == 'model':
            data_id = self.model_id
            data_dir = self.model_data_dir
        else:
            data_id = self.obs_id
            data_dir = self.obs_data_dir
        reader_class = self._get_gridded_reader_class(what=what)
        reader = reader_class(data_id=data_id, data_dir=data_dir)
        if hasattr(reader, 'filepath') and hasattr(self, 'filepath'):
            reader.filepath = self.filepath
        return reader

    def _get_gridded_reader_class(self, what):
        """Returns the class of the reader for gridded data."""
        try:
            reader = self.SUPPORTED_GRIDDED_READERS[self.gridded_reader_id[what]]
        except KeyError as e:
            raise NotImplementedError('Reader {} is not supported: {}'.
                                      format(self.gridded_reader_id[what], e))
        return reader

    @staticmethod
    def get_lowest_resolution(ts_type, *ts_types):
        """Get the lowest resolution ts_type of input ts_types"""
        return get_lowest_resolution(ts_type, *ts_types)

    def _check_add_model_read_aux(self, model_var, model_reader):
        if not isinstance(self.model_read_aux, dict):
            return False
        if not model_var in self.model_read_aux:
            return False
        info = self.model_read_aux[model_var]
        if not isinstance(info, dict):
            raise ValueError('Invalid value for model_read_aux of variable '
                             '{}. Need dictionary, got {}'
                             .format(model_var, info))
        elif not all([x in info for x in ['vars_required', 'fun']]):
            raise ValueError('Invalid value for model_read_aux dict of variable '
                             '{}. Require keys vars_required and fun in dict, '
                             'got {}'.format(model_var, info))
        try:
            model_reader.add_aux_compute(var_name=model_var, **info)
        except DataCoverageError:
            return False
        return True

    def _check_model_add_var(self, var_name, model_reader, var_matches):
        if isinstance(self.model_add_vars, dict) and var_name in self.model_add_vars: #observation variable
            add_var = self.model_add_vars[var_name]
            self._check_add_model_read_aux(add_var, model_reader)
            if model_reader.has_var(add_var):
                var_matches[add_var] = var_name
        return var_matches

    def _find_var_matches(self, obs_vars, model_reader, var_name=None):
        """Find variable matches in model data for input obs variables"""
        if isinstance(obs_vars, str):
            obs_vars = [obs_vars]

        # dictionary that will map model variables (keys) with observation variables (values)
        var_matches = {}

        muv = self.model_use_vars if isinstance(self.model_use_vars, dict) else {}

        for obs_var in obs_vars:
            if obs_var in muv:
                model_var = muv[obs_var]
            else:
                model_var = obs_var

            try:
                self._check_add_model_read_aux(model_var, model_reader)


                if model_reader.has_var(model_var):
                    var_matches[model_var] = obs_var

                var_matches = self._check_model_add_var(obs_var, model_reader,
                                                        var_matches)
            except VariableDefinitionError:
                continue

        if var_name is not None:
            _var_matches = {}
            for mvar, ovar in var_matches.items():
                if mvar in var_name or ovar in var_name:
                    _var_matches[mvar] = ovar
            var_matches = _var_matches

        if len(var_matches) == 0:

            raise DataCoverageError('No variable matches between '
                                    '{} and {} for input vars: {}'
                                    .format(self.model_id,
                                            self.obs_id,
                                            obs_vars))
        return var_matches

    def read_model_data(self, var_name, **kwargs):
        """Read model variable data based on colocation setup

        Parameters
        ----------
        var_name : str
            variable to be read

        Returns
        -------
        GriddedData
            variable data
        """
        use_input_var = False
        if 'use_input_var' in kwargs:
            use_input_var = kwargs.pop('use_input_var')

        reader = self.instantiate_gridded_reader(what='model')
        if use_input_var:
            var = var_name
        else:
            try:
                var_matches = self._find_var_matches(var_name, reader)
            except DataCoverageError:
                raise DataCoverageError('No match could be found in {} for '
                                        'variable {}'
                                        .format(self.model_id, var_name))
            var = list(var_matches.keys())[0]
        return self._read_gridded(reader, var,
                                  is_model=True,
                                  **kwargs)

    def read_ungridded(self, vars_to_read=None):
        """Helper to read UngriddedData

        Note
        ----
        Currently not used in main processing method
        :func:`_run_gridded_ungridded`. But should be.

        Parameters
        ----------
        vars_to_read : str or list, optional
            variables that should be read from obs-network (:attr:`obs_id`)

        Returns
        -------
        UngriddedData
            loaded data object

        """
        if isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]

        obs_reader = ReadUngridded(self.obs_id, data_dir=self.obs_data_dir)
        if vars_to_read is None:
            vars_to_read = self.obs_vars
        obs_vars = []
        for var in vars_to_read:
            if var in obs_reader.get_reader(self.obs_id).PROVIDES_VARIABLES:
                obs_vars.append(var)
            else:
                const.print_log.warning('Variable {} is not supported by {} '
                                     'and will be skipped'
                                     .format(var, self.obs_id))
        if len(obs_vars) == 0:
            raise DataCoverageError('No observation variable matches found for '
                                    '{}'.format(self.obs_id))

        if self.read_opts_ungridded is not None:
            ropts = self.read_opts_ungridded
        else:
            ropts = {}
        obs_data = obs_reader.read(datasets_to_read=self.obs_id,
                                   vars_to_retrieve=obs_vars,
                                   **ropts)
        if 'obs_filters' in self:
            remaining_filters = self._eval_obs_filters()
            obs_data = obs_data.apply_filters(**remaining_filters)

        if self.remove_outliers:
            #self._update_var_outlier_ranges(obs_vars=obs_vars)
            for var in obs_vars:
                low, high=None, None
                try:
                    low, high = self.var_ref_outlier_ranges[var]
                except Exception:
                    pass

                obs_data.remove_outliers(var, inplace=True,
                                         low=low, high=high)
        return obs_data
    # ToDo: cumbersome (together with _find_var_matches, review whole handling
    # of vertical codes for variable mappings...)
    def _read_gridded(self, reader, var_name, is_model=True, **kwargs):
        try:
            start = kwargs.pop('start')
        except KeyError:
            start = self.start

        try:
            stop = kwargs.pop('stop')
        except KeyError:
            stop = self.stop
        if is_model:
            vert_which = self.obs_vert_type
            ts_type_read = self.model_ts_type_read
            if self.model_use_climatology:
                start = 9999
                stop = None
        else:
            vert_which = None
            ts_type_read = self.obs_ts_type_read

        try:
            # set defaults if input was not specified explicitely
            if ts_type_read is None and not self.flex_ts_type_gridded:
                ts_type_read = self.ts_type
            if not 'vert_which' in kwargs:
                kwargs['vert_which'] = vert_which
            if not 'ts_type' in kwargs:
                kwargs['ts_type'] = ts_type_read

            if isinstance(kwargs['ts_type'], dict):
                kwargs['ts_type'] = kwargs['ts_type'][var_name]

            return reader.read_var(var_name,
                                   start=start,
                                   stop=stop,
                                   flex_ts_type=self.flex_ts_type_gridded,
                                   **kwargs)
        except DataCoverageError:
            vt=None
            if is_model:
                if self.obs_vert_type in self.OBS_VERT_TYPES_ALT:
                    vt = self.OBS_VERT_TYPES_ALT[self.obs_vert_type]
                elif self.model_vert_type_alt is not None:
                    mva = self.model_vert_type_alt
                    if isinstance(mva, str):
                        vt = mva
                    elif isinstance(mva, dict) and var_name in mva:
                        vt = mva[var_name]

            if vt is None:
                raise DataCoverageError(('No data files available for dataset '
                                         '{} ({})'
                                         .format(reader.data_id, var_name)))

            return reader.read_var(var_name,
                                   start=start,
                                   stop=stop,
                                   ts_type=ts_type_read,
                                   flex_ts_type=self.flex_ts_type_gridded,
                                   vert_which=vt)

    def _eval_obs_filters(self):
        obs_filters = self['obs_filters']
        remaining = {}
        if not isinstance(obs_filters, dict):
            raise AttributeError('Detected obs_filters attribute in '
                                 'Colocator class, which is not a '
                                 'dictionary: {}'.format(obs_filters))
        for key, val in obs_filters.items():
            if key in self: # can be handled
                if isinstance(self[key], dict) and isinstance(val, dict):
                    self[key].update(val)
                else:
                    self[key] = val
            else:
                remaining[key] = val
        return remaining

    def _save_coldata(self, coldata, savename, out_dir, model_var, model_data,
                      obs_var):
        """Helper for saving colocateddata"""
        if model_var != model_data.var_name:
            coldata.rename_variable(model_data.var_name,
                                    model_var,
                                    model_data.data_id)
        if (isinstance(self.model_add_vars, dict) and
            obs_var in self.model_add_vars and
            self.model_add_vars[obs_var] == model_var):

            coldata.rename_variable(obs_var,
                                    model_var,
                                    self.obs_id)

        coldata.to_netcdf(out_dir, savename=savename)
        self.file_status[savename] = 'saved'
        if self._log:
            msg = 'WRITE: {}\n'.format(savename)
            self._write_log(msg)
            print_log.info(msg)

    def _eval_resample_how(self, model_var, obs_var):
        rshow = self.resample_how
        if not isinstance(rshow, dict):
            return rshow

        if obs_var in rshow:
            return rshow[obs_var]
        elif model_var in rshow:
            return rshow[model_var]
        else:
            return None

    def _infer_start_stop(self, reader):
        """
        Infer start / stop for colocation from gridded reader

        Parameters
        ----------
        reader : ReadGridded (or similar WE NEED A BASE CLASS)
            Re

        Raises
        ------
        AttributeError
            if input reader does not have start / stop specified.

        Returns
        -------
        None.

        """
        try:
            yrs_avail = reader.years_avail
        except AttributeError:
            raise AttributeError(f'Input reader {reader} does not have attr. '
                                 'years_avail')

        first, last = yrs_avail[0], yrs_avail[-1]
        self.start = first
        if last > first:
            self.stop=last
        elif self.stop is not None:
            self.stop = None

    def _run_gridded_ungridded(self, var_name=None):
        """Analysis method for gridded vs. ungridded data"""
        print_log.info('PREPARING colocation of {} vs. {}'
                       .format(self.model_id, self.obs_id))

        model_reader = self.instantiate_gridded_reader(what='model')
        obs_reader = ReadUngridded(self.obs_id, data_dir=self.obs_data_dir)

        obs_vars = obs_reader.get_vars_supported(self.obs_id,
                                                 self.obs_vars)

        if len(obs_vars) == 0:
            raise DataCoverageError('No observation variable matches found for '
                                    '{}'.format(self.obs_id))

        var_matches = self._find_var_matches(obs_vars, model_reader,
                                             var_name)

        print_log.info('The following variable combinations will be colocated\n'
                       'MODEL-VAR\tOBS-VAR')
        for key, val in var_matches.items():
            print_log.info('{}\t{}'.format(key, val))

        # get list of unique observation variables
        obs_vars = np.unique(list(var_matches.values())).tolist()

        if self.remove_outliers:
            self._update_var_outlier_ranges(var_matches)

        if self.read_opts_ungridded is not None:
            ropts = self.read_opts_ungridded
        else:
            ropts = {}

        data_objs = {}
        if self.start is None:
            self._infer_start_stop(model_reader)

        start, stop = start_stop(self.start, self.stop)

        for model_var, obs_var in var_matches.items():

            # ToDo: consider removing outliers already here.
            #if 'obs_filters' in self:
            ts_type = self.ts_type
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id,
                                                             self.obs_id,
                                                             model_var,
                                                             obs_var))

            try:
                model_data = self._read_gridded(reader=model_reader,
                                                var_name=model_var,
                                                start=start,
                                                stop=stop,
                                                is_model=True)
            except Exception as e:

                msg = ('Failed to load gridded data: {} / {}. Reason {}'
                       .format(self.model_id, model_var, repr(e)))
                const.print_log.warning(msg)
                self._write_log(msg + '\n')

                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
                else:
                    continue
            ts_type_src = model_data.ts_type
            rshow = self._eval_resample_how(model_var, obs_var)
            if ts_type is None:
                # if colocation frequency is not specified
                ts_type = ts_type_src

            ignore_stats = None
            if self.ignore_station_names is not None:
                ignore_stats = self.ignore_station_names
                if isinstance(ignore_stats, dict):
                    if obs_var in ignore_stats:
                        ignore_stats = ignore_stats[obs_var]
                    else:
                        ignore_stats = None

            #ts_type_src = model_data.ts_type
            if TsType(ts_type_src) < TsType(ts_type):# < all_ts_types.index(ts_type_src):
                print_log.info('Updating ts_type from {} to {} (highest '
                               'available in model {})'.format(ts_type,
                                                               ts_type_src,
                                                               self.model_id))
                ts_type = ts_type_src

            really_do_reanalysis = True
            if self.save_coldata:
                really_do_reanalysis = False
                savename = self._coldata_savename(model_data, start, stop,
                                                  ts_type, var_name=model_var)

                file_exists = self._check_coldata_exists(model_data.data_id,
                                                         savename)

                out_dir = chk_make_subdir(self.basedir_coldata, self.model_id)
                if file_exists:
                    if not self.reanalyse_existing:
                        if self._log:
                            self._write_log('SKIP: {}\n'
                                            .format(savename))
                            print_log.info('Skip {} (file already '
                                           'exists)'.format(savename))
                            self.file_status[savename] = 'skipped'
                        continue
                    else:
                        really_do_reanalysis = True
                        print_log.info('Deleting and recomputing existing '
                               'colocated data file {}'.format(savename))
                        print_log.info('REMOVE: {}\n'.format(savename))
                        os.remove(os.path.join(out_dir, savename))
                else:
                    really_do_reanalysis = True

            if really_do_reanalysis:
                #Reading obs data only if the co-located data file does
                #not already exist.
                #This part of the method has been changed by @hansbrenna to work better with
                #large observational data sets. Only one variable is loaded into
                # the UngriddedData object at a time. Currently the variable is
                #re-read a lot of times, which is a weakness.
                obs_data = obs_reader.read(
                    vars_to_retrieve=obs_var,
                    only_cached=self._obs_cache_only,
                    **ropts)

                        # ToDo: consider removing outliers already here.
                if 'obs_filters' in self:
                    remaining_filters = self._eval_obs_filters()
                    obs_data = obs_data.apply_filters(**remaining_filters)

            try:
                try:
                    by=self.update_baseyear_gridded
                    stop=None
                except AttributeError:
                    by=None
                if self.model_use_climatology:
                    by=start.year
                coldata = colocate_gridded_ungridded(

                        gridded_data=model_data,
                        ungridded_data=obs_data,
                        ts_type=ts_type,
                        start=start, stop=stop,
                        var_ref=obs_var,
                        filter_name=self.filter_name,
                        regrid_res_deg=self.regrid_res_deg,
                        remove_outliers=self.remove_outliers,
                        vert_scheme=self.vert_scheme,
                        harmonise_units=self.harmonise_units,
                        var_outlier_ranges=self.var_outlier_ranges,
                        var_ref_outlier_ranges=self.var_ref_outlier_ranges,
                        update_baseyear_gridded=by,
                        ignore_station_names=ignore_stats,
                        apply_time_resampling_constraints=self.apply_time_resampling_constraints,
                        min_num_obs=self.min_num_obs,
                        colocate_time=self.colocate_time,
                        var_keep_outliers=self.model_keep_outliers,
                        var_ref_keep_outliers=self.obs_keep_outliers,
                        use_climatology_ref=self.obs_use_climatology,
                        resample_how=rshow)

                if self.model_to_stp:
                    coldata = correct_model_stp_coldata(coldata)
                if self.save_coldata:
                    self._save_coldata(coldata, savename, out_dir, model_var,
                                       model_data, obs_var)
                data_objs[model_var] = coldata
            except Exception:
                msg = ('Colocation between model {} / {} and obs {} / {} '
                       'failed.\nTraceback:\n{}'.format(self.model_id,
                                                  model_var,
                                                  self.obs_id,
                                                  obs_var,
                                                  traceback.format_exc()))
                const.print_log.warning(msg)
                self._write_log(msg + '\n')
                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)

        return data_objs

    def _run_gridded_gridded(self, var_name=None):

        model_reader = ReadGridded(self.model_id,
                                   data_dir=self.model_data_dir)

        if self.start is None:
            self._infer_start_stop(model_reader)

        start, stop = start_stop(self.start, self.stop)
        model_reader = self.instantiate_gridded_reader(what='model')
        obs_reader = self.instantiate_gridded_reader(what='obs')

        if 'obs_filters' in self:
            obs_filters = self._eval_obs_filters()
        else:
            obs_filters = {}

        obs_vars = self.obs_vars

        var_matches = self._find_var_matches(obs_vars, model_reader, var_name)

        if self.remove_outliers:
            self._update_var_outlier_ranges(var_matches)

        #all_ts_types = const.GRID_IO.TS_TYPES

        ts_type = self.ts_type

        data_objs = {}

        for model_var, obs_var in var_matches.items():
            obs_filters_var = obs_filters[obs_var] if obs_var in obs_filters else {}
            print_log.info('Running {} / {} ({}, {})'.format(self.model_id,
                                                             self.obs_id,
                                                             model_var,
                                                             obs_var))
            try:
                model_data = self._read_gridded(reader=model_reader,
                                                var_name=model_var,
                                                start=start,
                                                stop=stop,
                                                is_model=True)
            except Exception as e:

                msg = ('Failed to load gridded data: {} / {}. Reason {}'
                       .format(self.model_id, model_var, repr(e)))
                const.print_log.warning(msg)
                self._write_log(msg + '\n')

                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
                else:
                    continue

            if ts_type is None:
                ts_type = model_data.ts_type
            try:
                obs_data  = self._read_gridded(reader=obs_reader,
                                               var_name=obs_var,
                                               start=start,
                                               stop=stop,
                                               is_model=False,
                                               **obs_filters_var)
            except Exception as e:

                msg = ('Failed to load gridded data: {} / {}. Reason {}'
                       .format(self.model_id, model_var, repr(e)))
                const.print_log.warning(msg)
                self._write_log(msg + '\n')

                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
                else:
                    continue

# =============================================================================
#             if not obs_data.ts_type in all_ts_types:
#                 raise TemporalResolutionError('Invalid temporal resolution {} '
#                                               'in obs {}'.format(obs_data.ts_type,
#                                                                  self.model_id))
# =============================================================================

            # update colocation ts_type, based on the available resolution in
            # model and obs.
            lowest = self.get_lowest_resolution(ts_type, model_data.ts_type,
                                                obs_data.ts_type)
            rshow = self._eval_resample_how(model_var, obs_var)
            if lowest != ts_type:
                print_log.info('Updating ts_type from {} to {} (highest '
                               'available in {} / {} combination)'
                               .format(ts_type, lowest, self.model_id,
                                       self.obs_id))
                ts_type = lowest

            if self.save_coldata:
                out_dir = chk_make_subdir(self.basedir_coldata,
                                          self.model_id)

                savename = self._coldata_savename(model_data,
                                                  start,
                                                  stop,
                                                  ts_type,
                                                  var_name=model_var)

                file_exists = self._check_coldata_exists(self.model_id,
                                                          savename)
                if file_exists:
                    if not self.reanalyse_existing:
                        if self._log:
                            self._write_log('SKIP: {}\n'.format(savename))
                            print_log.info('Skip {} (file already '
                                           'exists)'.format(savename))
                        continue
                    else:
                        os.remove(os.path.join(out_dir, savename))
            try:
                by=None
                if self.model_use_climatology:
                    by=to_pandas_timestamp(start).year
                coldata = colocate_gridded_gridded(
                        gridded_data=model_data,
                        gridded_data_ref=obs_data,
                        ts_type=ts_type,
                        start=start, stop=stop,
                        filter_name=self.filter_name,
                        regrid_res_deg=self.regrid_res_deg,
                        remove_outliers=self.remove_outliers,
                        vert_scheme=self.vert_scheme,
                        harmonise_units=self.harmonise_units,
                        var_outlier_ranges=self.var_outlier_ranges,
                        var_ref_outlier_ranges=self.var_ref_outlier_ranges,
                        update_baseyear_gridded=by,
                        apply_time_resampling_constraints=\
                            self.apply_time_resampling_constraints,
                        min_num_obs=self.min_num_obs,
                        colocate_time=self.colocate_time,
                        var_keep_outliers=self.model_keep_outliers,
                        var_ref_keep_outliers=self.obs_keep_outliers,
                        resample_how=rshow)
                if self.save_coldata:
                    self._save_coldata(coldata, savename, out_dir, model_var,
                                       model_data, obs_var)
                    #coldata.to_netcdf(out_dir, savename=savename)
                if self._log:
                    self._write_log('WRITE: {}\n'.format(savename))
                    print_log.info('Writing file {}'.format(savename))
                data_objs[model_var] = coldata
            except Exception as e:
                msg = ('Colocation between model {} / {} and obs {} / {} '
                       'failed: Reason {}'.format(self.model_id,
                                                  model_var,
                                                  self.obs_id,
                                                  obs_var,
                                                  repr(e)))
                const.print_log.warning(msg)
                self._write_log(msg)
                if self.raise_exceptions:
                    self._close_log()
                    raise Exception(msg)
        return data_objs

    def _init_log(self):
        logdir = chk_make_subdir(self.basedir_logfiles,
                                 self.model_id)

        fname = ('{}_{}.log'.format(self.obs_id, datetime.today().strftime('%Y%m%d')))
        self._log = log = open(os.path.join(logdir, fname), 'a+')
        log.write('\n------------------ NEW ----------------\n')
        log.write('Timestamp: {}\n\n'.format(datetime.today().strftime('%d-%m-%Y %H:%M')))
        log.write('Analysis configuration\n')
        for k, v in self.items():
            log.write('{}: {}\n'.format(k, v))

    def _close_log(self):
        if self._log is not None:
            self._log.close()
            self._log = None

    def _coldata_savename(self, model_data, start=None, stop=None,
                           ts_type=None, var_name=None):
        """Based on current setup, get savename of colocated data file
        """
        if start is None:
            start = model_data.start
        else:
            start = to_pandas_timestamp(start)
        if stop is None:
            stop = model_data.stop
        else:
            stop = to_pandas_timestamp(stop)
        if ts_type is None:
            ts_type = model_data.ts_type

        if var_name is None:
            var_name = model_data.var_name
        start_str = to_datestring_YYYYMMDD(start)
        stop_str = to_datestring_YYYYMMDD(stop)

        if isinstance(self.obs_name, str):
            obs_id = self.obs_name
        else:
            obs_id = self.obs_id

        if isinstance(self.model_name, str):
            model_id = self.model_name
        else:
            model_id = model_data.data_id

        col_data_name = ColocatedData._aerocom_savename(var_name=var_name,
                                                        obs_id=obs_id,
                                                        model_id=model_id,
                                                        start_str=start_str,
                                                        stop_str=stop_str,
                                                        ts_type=ts_type,
                                                        filter_name=self.filter_name)
        return col_data_name + '.nc'

    def _check_coldata_exists(self, model_id, coldata_savename):
        """Check if colocated data file exists"""
        folder = os.path.join(self.basedir_coldata,
                              model_id)
        if not os.path.exists(folder):
            return False
        files = os.listdir(folder)
        if coldata_savename in files:
            self.file_status[coldata_savename] = 'exists'
            return True
        self.file_status[coldata_savename] = 'exists_not'
        return False

    def _update_var_outlier_ranges(self, var_matches=None, obs_vars=None,
                                   mod_vars=None):
        if isinstance(var_matches, dict):
            obs_vars = list(var_matches.values())
            mod_vars = list(var_matches.keys())

        oor = self.var_ref_outlier_ranges
        mor = self.var_outlier_ranges

        if isinstance(mor, dict) and isinstance(mod_vars, list):
            for mvar in mod_vars:
                mname = const.VARS[mvar].var_name
                if mname != mvar and mvar in mor and not mname in mor:
                    self.var_outlier_ranges[mname] = mor[mvar]

        if isinstance(oor, dict) and isinstance(obs_vars, list):
            for ovar in obs_vars:
                oname = const.VARS[ovar].var_name
                if (oname != ovar and ovar in oor and not oname in oor):
                    self.var_ref_outlier_ranges[oname] = oor[ovar]


    def __call__(self, **kwargs):
        raise NotImplementedError
        self.update(**kwargs)
        self.run()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')

    obs_dir = '/home/jonasg/MyPyaerocom/testdata-minimal/modeldata/TM5-met2010_CTRL-TEST/renamed'
    MODEL_ID =  'CAM5.3-Oslo_AP3-CTRL2016-PD'
    col = Colocator(model_id = MODEL_ID,
                    obs_data_dir=obs_dir,
                    obs_id='TM5-met2010_CTRL-TEST',
                    obs_vars=['od550aer'],
                    start=2010)

    col.run(reanalyse_existing=True)

    data = col.data[MODEL_ID]['od550aer']
    data.plot_scatter(loglog=True)
