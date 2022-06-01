#!/usr/bin/env python3
"""
parallelisation for aeroval processing

"""

# some ideas what to use
import argparse

# import glob
import os


# import sys


def main():
    parser = argparse.ArgumentParser(
        description="command line interface to aeroval parallelisation\n\n\n"
    )
    parser.add_argument("--file", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument(
        "--outdir", help="output directory; the filename will be extended with the string '.nc'"
    )
    parser.add_argument(
        "--tempdir",
        help="directory for temporary files",
        default=os.path.join(os.environ["HOME"], "tmp"),
    )

    args = parser.parse_args()
    if args.file:
        options["files"] = args.file
    if args.verbose:
        options["verbose"] = True
    else:
        options["verbose"] = False

    if args.outdir:
        options["outdir"] = args.outdir

    if args.tempdir:
        options["tempdir"] = args.tempdir


if __name__ == "__main__":
    main()
