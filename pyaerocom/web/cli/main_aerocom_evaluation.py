#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('agg')
from warnings import filterwarnings
import argparse
import os, sys
import pyaerocom as pya

def str2bool(v):
    #see https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def make_parser():
    p = argparse.ArgumentParser(
        description=(
            'Command line interface (CLI) for running the AerocomEvaluation '
            'tools. The CLI requires a json version of a configuration setup. '
            'You can create a json configuration file using an existing instance'
            'of the AerocomEvaluation class (e.g. in a .py file where you define '
            'the evaluation setup) and then calling class method to_json, i.e. '
            'AerocomEvaluation.to_json(<output_dir>), where <output_dir> '
            'denotes the directory where you want to store the configuration '
            'file. This will create a file called cfg_<proj_id>_<exp_id>.json, '
            'where <proj_id> and <exp_id> are the ID of the project and '
            'experiment, respectively, which are always required for running an '
            'evaluation. If you have such a json configuration file '
            '(e.g. called cfg_playground_test-experiment.json) you can run it '
            'from the command line by navigating into the folder that contains '
            'the file and calling:\n\n'
            '$ pyaeroeval playground test-experiment\n\n'
            'This will run all possible model / obs / var combinations specified '
            'in the configuration file cfg_playground_test-experiment.json.\n'
            'See below for further input requirements and options.'
        ), formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('proj_id', help='Project ID (name of subdir under data/json)')
    p.add_argument('exp_id', help=('Experiment ID (name of subdir under '
                                   'data/json/{proj_id})' ))

    p.add_argument('-d', '--config_dir', default='.',
                   help=('Directory containing evaluation config files. '
                         'Defaults to current directory'))

    p.add_argument('-m', '--model_name', default=None,
                   help=('Name of model that is supposed to be run (default '
                         'is None, which will evaluate all models that are '
                         'specified in the configuration.'))

    p.add_argument('-o', '--obs_name', default=None,
                   help=('Name of observation network that is supposed to be '
                         'run (default is None, which will evaluate all '
                         'obsnetworks that are specified in the configuration'))
    p.add_argument('--var_name', default=None,
                   help=('Name of variable that is supposed to be run (default '
                         'is None which will evaluate all possible variables)'))
    p.add_argument('--reanalyse_existing',
                   help='Reanalyse existing colocated data files')
    p.add_argument('--raise_exceptions',
                   help='Raise exceptions if they occur during analysis')
    p.add_argument('--only_json',
                   help=('Recompute json files from existing colocated NetCDF '
                         'files'))
    p.add_argument('--only_maps',
                   help=('Process only model maps'))
    p.add_argument('-i', '--info', action='store_true',
                   help='print configuration (no analysis is run)')
    p.add_argument('--delete', action='store_true',
                   help=('Remove all data (json files, menu entries) associated '
                         'with an experiment.'))
    p.add_argument('--warnings', action='store_true',
                   help='Display python warnings')
    return p

def main():
    # Define command line interface
    p = make_parser()
    args = p.parse_args()

    update_args = {}
    if args.raise_exceptions:
        update_args['raise_exceptions'] = str2bool(args.raise_exceptions)
    if args.reanalyse_existing:
        update_args['reanalyse_existing'] = str2bool(args.reanalyse_existing)
    if args.only_json:
        update_args['only_json'] = str2bool(args.only_json)
    if args.only_maps:
        update_args['only_maps'] = str2bool(args.only_maps)
    if not args.warnings:
        print('Filtering all warnings')
        filterwarnings('ignore')
    cfgdir = os.path.abspath(args.config_dir)
    if not os.path.exists(cfgdir):
        raise FileNotFoundError(f'No such file or directory: {cfgdir}')

    cfg_avail = pya.web.helpers_evaluation_iface.get_all_config_files_evaluation_iface(args.config_dir)

    if len(cfg_avail) == 0:
        raise FileNotFoundError(
            f'Could not find any valid configuration files in {args.config_dir}')

    if not args.proj_id in cfg_avail:
        raise ValueError('No such proj_id {} available. Please choose from {}'
                         .format(args.proj_id, cfg_avail.keys()))
    elif not args.exp_id in cfg_avail[args.proj_id]:
        raise ValueError('No such exp_id {} available. Please choose from {}'
                         .format(args.exp_id, cfg_avail[args.proj_id].keys()))

    ae = pya.web.AerocomEvaluation(proj_id=args.proj_id,
                                   exp_id=args.exp_id,
                                   config_dir=args.config_dir)

    if len(update_args) > 0:
        ae.update(**update_args)


    if args.delete:
        ae.delete_experiment_data()
        sys.exit()

    if args.info:
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

    ae.run_evaluation(model_name=args.model_name,
                      obs_name=args.obs_name,
                      var_name=args.var_name)

if __name__ == '__main__':
    main()
