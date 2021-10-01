#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyaerocom import const
const.print_log.warning(DeprecationWarning(
    'Module pyaerocom/web/trends_evaluation.py will be removed as of '
    'release 0.12.0 which will incorporate trends computation in AeroVal '
    'interface (via AerocomEvaluation class)'))

def main():
    from argparse import ArgumentParser
    import os, sys

    # Define command line interface
    p = ArgumentParser(description='pyaerocom command line interface for '
                       'processing of trends data for Aerosol trends '
                       'interface')
    # Mandatoory: name of configuration (should be in config file name)
    p.add_argument('name', help='Project ID')
    p.add_argument('-d', '--config_dir', default='.',
                   help=('Directory containing trends config files'))

    p.add_argument('-o', '--obs_name', default=None,
                   help=('Name of observation network that is supposed to be '
                         'run (default is all obsnetworks that are specified in '
                         'the config file'))
    p.add_argument('-c', '--clear', action='store_true',
                   help='Delete (potentially) existing json files before rerun')

    p.add_argument('-p', '--print_config', action='store_true',
                   help='print configuration (no analysis is run')

    args = p.parse_args()

    if args.clear:
        clear_existing_json = True
    else:
        clear_existing_json = None

    if not os.path.exists(args.config_dir):
        raise FileNotFoundError('No such file or directory: {}'.format(args.config_dir))

    import pyaerocom as pya
    cfg_avail = pya.web.helpers_trends_iface.get_all_config_files_trends_iface(args.config_dir)

    if len(cfg_avail) == 0:
        raise FileNotFoundError('Could not find any valid configuration files '
                                'in {}'.format(os.path.abspath(args.config_dir)))

    if not args.name in cfg_avail:
        raise ValueError('No such configuration with name {} available. '
                         'Please choose from {}'
                         .format(args.name, cfg_avail.keys()))

    te = pya.web.TrendsEvaluation(config_file=cfg_avail[args.name])

    if args.print_config:
        print(te)
        sys.exit()

    if args.obs_name is not None:
        if not args.obs_name in list(te.obs_config):
            raise ValueError('No such obs_name available in current config. '
                             'Please choose from: {}'
                             .format(list(te.obs_config)))

    te.run_evaluation(obs_name=args.obs_name,
                      clear_existing_json=clear_existing_json)

if __name__ == '__main__':
    main()
