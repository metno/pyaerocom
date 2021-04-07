#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pyaerocom main CLI (accessible via pya command)
"""

from argparse import ArgumentParser
from pyaerocom import const
import pyaerocom.scripts.highlevel_utils as hlu

def init_parser():

    ap = ArgumentParser(description='pyaerocom command line interface')

    ap.add_argument('-b', '--browse', help='Browse database')
    ap.add_argument('--clearcache', action='store_true',
                    help='Delete cached data objects')
    ap.add_argument('--ppiaccess', action='store_true',
                    help='Check if MetNO PPI can be accessed')

    return ap

def confirm():
    """
    Ask user to confirm something

    Returns
    -------
    bool
        True if user answers yes, else False
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("[Y/N]? ").lower()
    return answer == 'y'

def main():
    import sys
    ap = init_parser()

    args = ap.parse_args()

    if args.browse:
        print('Searching database for matches of {}'.format(args.browse))
        print(hlu.browse_database(args.browse))

    if args.clearcache:
        print('Are you sure you want to delete all cached data objects?')
        if confirm():
            print('OK then.... here we go!')
            hlu.clear_cache()
        else:
            print('Wise decision, pyaerocom will handle it for you '
                  'automatically anyways ;P')

    if args.ppiaccess:
        print('True') if const.has_access_lustre else print('False')


if __name__ == '__main__':
    main()
