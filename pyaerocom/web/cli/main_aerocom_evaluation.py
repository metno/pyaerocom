#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    from warnings import filterwarnings
    from argparse import ArgumentParser
    import os, sys

    # Define command line interface
    p = ArgumentParser(description='Command line interface for AerocomEvaluation routines')

    p.add_argument('proj_id', help='Project ID')
    p.add_argument('exp_id', help='Experiment ID')
    p.add_argument('-d', '--config_dir', default='.',
                   help=('Directrory containing evaluation config files (e.g. '
                         'cfg_aerocom_PIII-optics.json)'))

    p.add_argument('-m', '--model_name', default=None,
                   help=('Name of model that is supposed to be run (default '
                         'is all models that are specified in the config file '))

    p.add_argument('-o', '--obs_name', default=None,
                   help=('Name of observation network that is supposed to be '
                         'run (default is all obsnetworks that are specified in '
                         'the config file'))
    p.add_argument('-e', '--exceptions', action='store_true',
                    help='Raise exceptions in colocation')

    p.add_argument('-r', '--reanalyse', action='store_true',
                   help='Reanalyse existing colocated data files')

    p.add_argument('--onlyjson', action='store_true',
                   help=('Recompute json files from existing colocated NetCDF '
                         'files'))

    p.add_argument('-c', '--clear', action='store_true',
                   help='Delete (potentially) existing json files before rerun')
    p.add_argument('-p', '--print_config', action='store_true',
                   help='print configuration (no analysis is run)')
    p.add_argument('--delete', action='store_true',
                   help='Remove an experiment from the web (deletes all json files associated)')
    p.add_argument('--warnings', action='store_true',
                   help='Display python warnings')

    args = p.parse_args()
    if args.exceptions:
        raise_exceptions = True
    else:
        raise_exceptions = None
    if args.reanalyse:
        reanalyse_existing = True
    else:
        reanalyse_existing = None
    if args.clear:
        clear_existing_json = True
    else:
        clear_existing_json = None
    if args.onlyjson:
        onlyjson = True
    else:
        onlyjson = None
    if not args.warnings:
        filterwarnings('ignore')

    if not os.path.exists(args.config_dir):
        raise FileNotFoundError('No such file or directory: {}'.format(args.config_dir))

    import pyaerocom as pya

    cfg_avail = pya.web.helpers_evaluation_iface.get_all_config_files_evaluation_iface(args.config_dir)

    if len(cfg_avail) == 0:
        raise FileNotFoundError('Could not find any valid configuration files '
                                'in {}'.format(os.path.abspath(args.config_dir)))

    if not args.proj_id in cfg_avail:
        raise ValueError('No such proj_id {} available. Please choose from {}'
                         .format(args.proj_id, cfg_avail.keys()))
    elif not args.exp_id in cfg_avail[args.proj_id]:
        raise ValueError('No such exp_id {} available. Please choose from {}'
                         .format(args.exp_id, cfg_avail[args.proj_id].keys()))

    ae = pya.web.AerocomEvaluation(proj_id=args.proj_id,
                                   exp_id=args.exp_id,
                                   config_dir=args.config_dir)

    if args.delete:
        ae.delete_experiment_data()
        sys.exit()

    if args.print_config:
        print(ae)
        sys.exit()

    if args.model_name is not None:
        if len(ae.find_model_matches(args.model_name)) == 0:
        #if not args.model_name in list(ae.model_config):
            raise ValueError('No such model_name available in current config. '
                             'Please choose from: {}'
                             .format(list(ae.model_config)))
    if args.obs_name is not None:
        if len(ae.find_obs_matches(args.obs_name)) == 0:
        #if not args.obs_name in list(ae.obs_config):
            raise ValueError('No such obs_name available in current config. '
                             'Please choose from: {}'
                             .format(list(ae.obs_config)))

    if onlyjson:
        print('RECOMPUTING EXISTING JSON FILES, NO COMPUTATION OF '
              'COLOCATED DATA OBJECTS WILL BE PERFORMED')

    ae.run_evaluation(model_name=args.model_name,
                      obs_name=args.obs_name,
                      reanalyse_existing=reanalyse_existing,
                      raise_exceptions=raise_exceptions,
                      clear_existing_json=clear_existing_json,
                      only_json=onlyjson)

if __name__ == '__main__':
    main()
