#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 16:44:18 2019

@author: jonasg
"""
import cf_units
import numpy as np
import os
from pyaerocom import const
from pyaerocom.griddeddata import GriddedData
from pyaerocom.helpers import make_dummy_cube_latlon, numpy_to_cube
from pyaerocom.web import AerocomEvaluation

def compute_model_average_and_diversity(cfg, var_name,
                                        model_names=None,
                                        ts_type='monthly',
                                        lat_res_deg=2,
                                        lon_res_deg=3,
                                        year=None,
                                        data_id=None,
                                        avg_how='median',
                                        extract_surface=True,
                                        ignore_models=None,
                                        logfile=None,
                                        comment=None,
                                        **kwargs):
    """Compute median or mean model based on input models

    Note
    ----
    BETA version that will likely undergo revisions

    Parameters
    ----------
    cfg : AerocomEvaluation
        analysis instance
    var_name : str
        name of variable
    model_names : dict
        dictionary containing model names (keys) and corresponding ID's (values)
    ts_type : str
        output freq.
    lat_res_deg : int
        output latitude resolution
    lon_res_deg : int
        output longitude resolution
    data_id : str
        output data_id of ensemble model
    avg_how : str
        how to compute averages (choose from mean or median)
    extract_surface : bool
        if True (and if data contains model levels), surface level is
        extracted
    logfile, optional
        opened file to write logging messages
    **kwargs
        additional keyword args passed to
        :func:`AerocomEvaluation.read_model_data`

    Returns
    -------
    GriddedData
        ensemble model for input variable computed
    GriddedData
        corresponding diversity field, computed using definition from
        Textor et al., 2006 (ACP) DOI: 10.5194/acp-6-1777-2006
    """
    if not isinstance(cfg, AerocomEvaluation):
        raise ValueError
    if ignore_models is None:
        ignore_models = []
    if year is None:
        year = cfg.colocation_settings.start

    if cfg.colocation_settings.stop is not None:
        raise ValueError('Can only compute average model for single year '
                         'analyses')
    if avg_how =='mean':
        avg_fun = np.mean
    elif avg_how == 'median':
        avg_fun = np.median
    else:
        raise ValueError('Invalid input for avg_how {}'.format(avg_how))

    if data_id is None:
        data_id = 'AEROCOM-{}'.format(avg_how.upper())

    if model_names is None:
        model_names = []
        for mname in cfg.model_config:
            if not mname in cfg.model_ignore:
                model_names.append(mname)

    # make sure the input model names exist and are names and not ID's
    # also takes care of case where input is dictionary
    _model_names = []
    for mname in model_names:
        try:
            _model_names.append(cfg.get_model_name(mname))
        except Exception:
            print('No such model in AerocomEvaluation class: {}'.format(mname))

    model_names = _model_names

    # same for ignore models (consider only relevant ones)
    _ignore_models = []
    for mname in ignore_models:
        try:
            mn = cfg.get_model_name(mname)
            if mn in model_names:
                _ignore_models.append(mn)
        except AttributeError:
            pass
    ignore_models = _ignore_models

    dummy = make_dummy_cube_latlon(lat_res_deg=lat_res_deg,
                                   lon_res_deg=lon_res_deg)

    loaded = []
    from_files = []
    from_models=[]
    from_vars = []
    models_failed = []
    vunit = cf_units.Unit(const.VARS[var_name].units)

    for mname in model_names:
        if not mname in cfg.model_config:
            raise Exception('Please debug')

        if mname in ignore_models:
            const.print_log.info('Ignoring model {}'.format(mname))
            continue
        const.print_log.info('Model {} ({})'.format(mname, var_name))

        mid = cfg.get_model_id(mname)
        if mid == data_id or mname==data_id:
            continue
        try:
            data = cfg.read_model_data(mname, var_name,
                                       ts_type=ts_type,
                                       start=year,
                                       **kwargs)
            if not data.units == vunit:
                data.convert_unit(vunit)

            elif not data.longitude.circular:
                if not data.check_lon_circular():
                    raise Exception('Longitude of {} is not circular...'
                                    .format(mname))
            data.reorder_dimensions_tseries()
            data = data.resample_time(ts_type)
            if data.ndim==4:
                if extract_surface:
                    data = data.extract_surface_level()
                else:
                    raise NotImplementedError('Cannot process ModelLevel fields yet')
            data = data.regrid(dummy)
        except Exception as e:
            models_failed.append(mid)
            const.print_log.info('Failed to process...: {}'.format(repr(e)))
            if logfile is not None:
                logfile.write('\nFAILED {}: {}'.format(mid, repr(e)))
            continue

        loaded.append(data.cube.data)
        from_files.extend(data.from_files)
        from_models.append(data.data_id)
        from_vars.append(data.var_name)

    if not len(loaded) > 1:
        raise ValueError('Can only compute average if more than one model is '
                         'available')

    from_files = [os.path.basename(f) for f in from_files]

    dims = [data.time, dummy.coord('latitude'), dummy.coord('longitude')]
    avg = avg_fun(loaded, axis=0)
    q1, q3 = None, None
    if avg_how == 'mean':
        diversity = np.std(np.asarray(loaded) / avg, axis=0) * 100
    else:
        ld = np.asarray(loaded)
        q1 = np.quantile(ld, 0.25, axis=0)
        q3 = np.quantile(ld, 0.75, axis=0)
        diversity = (q3-q1) / avg * 100

    if comment is None:
        comment = 'AeroCom {} model data for variable {}.'.format(avg_how,
                                                                 var_name)

    mean = GriddedData(numpy_to_cube(avg,
                                     dims=dims,
                                     var_name=var_name,
                                     units=data.unit,
                                     ts_type=ts_type,
                                     data_id=data_id,
                                     from_files=from_files,
                                     from_models=from_models,
                                     from_vars=from_vars,
                                     models_failed=models_failed,
                                     comment=comment))

    commentdiv = comment + ' Diversity field in units of % (IQR for median, std for mean)'

    delta = GriddedData(numpy_to_cube(diversity,
                                      dims=dims,
                                      var_name='{}div'.format(var_name),
                                      units='%',
                                      ts_type=ts_type,
                                      data_id=data_id,
                                      from_files=from_files,
                                      from_models=from_models,
                                      from_vars=from_vars,
                                      models_failed=models_failed,
                                      comment=commentdiv))

    if q1 is not None: # then also q3 is not None
        commentq1 =  comment + ' First Quantile.'
        per25 = GriddedData(numpy_to_cube(q1,
                                         dims=dims,
                                         var_name='{}q1'.format(var_name),
                                         units=data.unit,
                                         ts_type=ts_type,
                                         data_id=data_id,
                                         from_files=from_files,
                                         from_models=from_models,
                                         from_vars=from_vars,
                                         models_failed=models_failed,
                                         comment=commentq1))

        commentq3 =  comment + ' First Quantile.'
        per75 = GriddedData(numpy_to_cube(q3,
                                         dims=dims,
                                         var_name='{}q3'.format(var_name),
                                         units=data.unit,
                                         ts_type=ts_type,
                                         data_id=data_id,
                                         from_files=from_files,
                                         from_models=from_models,
                                         from_vars=from_vars,
                                         models_failed=models_failed,
                                         comment=commentq3))
    else:
        per25, per75 = None, None

    return (mean, delta, per25, per75)
