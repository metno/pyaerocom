#!/usr/bin/env python3
"""
small helper program to read a aeroval config from a json file

"""
import argparse
import os
import pathlib

import simplejson as json

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor


def main():
    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)
    res = ana.run()


if __name__ == "__main__":
    main()
