#!/usr/bin/env python3
"""
parallelisation for aeroval processing

- create several aeroval config files from one input config
  (per model and per obs network for now)
- submit these configs to the GridEngine queue

"""

# some ideas what to use
import argparse
import copy
import os
import pathlib
from getpass import getuser
from importlib.machinery import SourceFileLoader
from socket import gethostname
from tempfile import mkdtemp
from uuid import uuid4

import simplejson as json


def main():
    default_cfg_var = "CFG"
    run_uuid = uuid4()
    hostname = gethostname()
    user = getuser()
    tmp_dir = "/tmp"

    JSON_RUNSCRIPT = (
        "/home/jang/data/Python3/pyaerocom_new/pyaerocom/tools/aeroval_run_json_cfg.py"
    )

    parser = argparse.ArgumentParser(
        description="command line interface to aeroval parallelisation.\n"
        "aeroval config has to to be in the variable CFG for now!\n\n"
    )
    parser.add_argument("files", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("--outdir", help="output directory")
    parser.add_argument("--subdry", help="dryrun for submission to queue",action="store_true")
    parser.add_argument(
        "--jsonrunscript",
        help=f"script to run json config files; defaults to {JSON_RUNSCRIPT}",
        default=JSON_RUNSCRIPT,
    )
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

    if args.jsonrunscript:
        options["jsonrunscript"] = args.jsonrunscript

    if args.verbose:
        options["verbose"] = True
    else:
        options["verbose"] = False

    if args.subdry:
        options["subdry"] = True
    else:
        options["subdry"] = False

    if args.outdir:
        options["outdir"] = args.outdir

    if args.tempdir:
        options["tempdir"] = args.tempdir

    if args.cfgvar:
        options["cfgvar"] = args.cfgvar

    # these are the directories that need to be submitted to the queue
    runfiles = []
    for _file in options["files"]:
        # read aeroval config file
        foo = SourceFileLoader("bla", _file).load_module()
        # the following line does unfortunately not work since a module is not subscriptable
        # CFG = foo[options["cfgvar"]]
        # stick to the name CFG for the aeroval configuration for now
        cfg = copy.deepcopy(foo.CFG)
        # create tmp dir
        tempdir = mkdtemp(dir=options["tempdir"])
        # index for temporary data directories
        dir_idx = 1
        for _model in cfg["model_cfg"]:
            out_cfg = copy.deepcopy(cfg)
            out_cfg.pop("model_cfg", None)
            out_cfg.pop("obs_cfg", None)
            out_cfg["model_cfg"] = {}
            out_cfg["model_cfg"][_model] = cfg["model_cfg"][_model]
            for _obs_network in cfg["obs_cfg"]:
                out_cfg["obs_cfg"] = {}
                out_cfg["obs_cfg"][_obs_network] = cfg["obs_cfg"][_obs_network]
                # adjust json_basedir and coldata_basedir so that the different runs
                # do not influence each other
                out_cfg[
                    "json_basedir"
                ] = f"{out_cfg['json_basedir']}/{pathlib.PurePath(tempdir).parts[-1]}.{dir_idx:04d}"
                out_cfg[
                    "coldata_basedir"
                ] = f"{out_cfg['coldata_basedir']}/{pathlib.PurePath(tempdir).parts[-1]}.{dir_idx:04d}"
                cfg_file = pathlib.PurePosixPath(_file).stem
                outfile = pathlib.PurePosixPath(tempdir).joinpath(
                    f"cfg_file_{_model}_{_obs_network}.json"
                )
                print(f"writing file {outfile}")
                with open(outfile, "w", encoding="utf-8") as j:
                    json.dump(out_cfg, j, ensure_ascii=False, indent=4)
                dir_idx += 1
                runfiles.append(outfile)
                if options["verbose"]:
                    print(out_cfg)

    if options["subdry"]:
        # just print the to be run files
        for _runfile in runfiles:
            print(f"{_runfile}")
        pass
    else:
        pass


if __name__ == "__main__":
    main()
