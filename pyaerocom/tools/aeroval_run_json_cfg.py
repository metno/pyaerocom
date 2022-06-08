#!/usr/bin/env python3
"""
small helper program to read a aeroval config from a json file

"""
import argparse
import os
import pathlib
import sys

import simplejson as json


def main():

    parser = argparse.ArgumentParser(
        description="small helper to run aeroval configs from json files"
    )
    parser.add_argument("files", help="file(s) to read", nargs="+")
    parser.add_argument(
        "-d", "--dryrun", help="dry run, just print the config", action="store_true"
    )

    args = parser.parse_args()
    options = {}
    if args.files:
        options["files"] = args.files
        # to avoid that lustre access is checked if the help just needs to be printed
        from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

    if args.dryrun:
        options["dryrun"] = True
    else:
        options["dryrun"] = False

    for _file in options["files"]:
        with open(_file, "r") as infile:
            CFG = json.load(infile)
        stp = EvalSetup(**CFG,)
        ana = ExperimentProcessor(stp)
        if not options["dryrun"]:
            res = ana.run()
        else:
            print(stp)


if __name__ == "__main__":
    main()
