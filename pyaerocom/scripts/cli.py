#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:03:51 2020

@author: jonasg
"""

from argparse import ArgumentParser
import pyaerocom.scripts.highlevel_utils as hlu

def init_parser():

    ap = ArgumentParser(description='pyaerocom command line interface')

    ap.add_argument('-b', '--browse', help='Browse database')
    ap.add_argument('--clearcache', action='store_true',
                    help='Delete cached data objects')

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

if __name__ == '__main__':
    main()
