#!/usr/bin/env python3
"""
parallelisation for aeroval processing

"""

# some ideas what to use
import argparse
import copy
import os
import pathlib
from getpass import getuser
from importlib.machinery import SourceFileLoader
from socket import gethostname
from uuid import uuid4
from tempfile import mkdtemp
import simplejson as json


def main():
    default_cfg_var = "CFG"
    run_uuid = uuid4()
    hostname = gethostname()
    user = getuser()
    tmp_dir = "/tmp"

    parser = argparse.ArgumentParser(
        description="command line interface to aeroval parallelisation.\n"
        "aeroval config has to to be in the variable CFG for now!\n\n"
    )
    parser.add_argument("files", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("--outdir", help="output directory")
    parser.add_argument(
        "--cfgvar",
        help=f"variable that holds the aeroval config in the file(s) provided. Defaults to {default_cfg_var}",
        default=default_cfg_var,
    )
    parser.add_argument(
        "--tempdir",
        help=f"directory for temporary files; defaults to {tmp_dir}",
        default=tmp_dir,
    )

    args = parser.parse_args()
    options = {}
    if args.files:
        options["files"] = args.files
    if args.verbose:
        options["verbose"] = True
    else:
        options["verbose"] = False

    if args.outdir:
        options["outdir"] = args.outdir

    if args.tempdir:
        options["tempdir"] = args.tempdir

    if args.cfgvar:
        options["cfgvar"] = args.cfgvar

    for _file in options["files"]:
        # read aeroval config file
        foo = SourceFileLoader("bla", _file).load_module()
        # the following line does unfortunately not work since a module is not subscriptable
        # CFG = foo[options["cfgvar"]]
        # stick to the name CFG for the aeroval configuration for now
        cfg = copy.deepcopy(foo.CFG)
        # create tmp dir
        tempdir = mkdtemp(dir=options["tempdir"])
        for _model in cfg["model_cfg"]:
            out_cfg = copy.deepcopy(cfg)
            out_cfg.pop("model_cfg", None)
            out_cfg.pop("obs_cfg", None)
            out_cfg["model_cfg"] = {}
            out_cfg["model_cfg"][_model] = cfg["model_cfg"][_model]
            for _obs_network in cfg["obs_cfg"]:
                out_cfg["obs_cfg"] = {}
                out_cfg["obs_cfg"][_obs_network] = cfg["obs_cfg"][_obs_network]
                cfg_file = pathlib.PurePosixPath(_file).stem
                outfile = pathlib.PurePosixPath(tempdir).joinpath(f"cfg_file_{_model}_{_obs_network}.json")
                print(f"writing file {outfile}")
                with open(outfile, 'w', encoding='utf-8') as j:
                    json.dump(out_cfg, j, ensure_ascii=False, indent=4)

                print(out_cfg)


if __name__ == "__main__":
    main()
