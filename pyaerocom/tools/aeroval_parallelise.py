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

DEFAULT_CFG_VAR = "CFG"
RUN_UUID = uuid4()
HOSTNAME = gethostname()
USER = getuser()
TMP_DIR = "/tmp"

JSON_RUNSCRIPT_NAME = "aeroval_run_json_cfg.py"
# qsub binary
QSUB_NAME = "/usr/bin/qsub"
# qsub submission host
QSUB_HOST = "ppi-clogin-a1.met.no"
# directory, where the files will bew transferred before they are run
QSUB_DIR = f"/tmp/{USER}/qsub.{RUN_UUID}/"
# user name on the qsub host
QSUB_USER = USER
# queue name
QSUB_QUEUE_NAME = "research-el7.q"


# assume that the script to run the aeroval json file is in the same directory as this script
JSON_RUNSCRIPT = pathlib.PurePath(pathlib.PurePath(__file__).parent).joinpath(JSON_RUNSCRIPT_NAME)


def prep_files(options):
    """preprare the aeroval config files to run
    return a list of files

    """
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

    return runfiles


def run_queue(
    runfiles,
    qsub_host=QSUB_HOST,
    qsub_cmd=QSUB_NAME,
    qsub_dir=QSUB_DIR,
    qsub_user=QSUB_USER,
    qsub_queue=QSUB_QUEUE_NAME,
):
    """submit runfiles to the remote cluster"""

    # to enable test usage, import fabric only here
    from fabric import Connection
    import subprocess

    # create runfile
    runfile_arr = []
    runfile_arr.append("#!/bin/bash -l")
    runfile_arr.append("#$ -S /bin/bash")
    runfile_arr.append("#$ -N AEROVAL_NAME")
    runfile_arr.append("#$ -q research-el7.q")
    runfile_arr.append("#$ -pe shmem-1 1")
    runfile_arr.append("#$ -wd /home/UUSER/data/aeroval-local-web/pyaerocom_config/config_files")
    runfile_arr.append("#$ -l h_rt=96:00:00")
    runfile_arr.append("#$ -l s_rt=96:00:00")
    runfile_arr.append("#$ -M UUSER@met.no")
    runfile_arr.append("#$ -m abe")
    runfile_arr.append("#$ -l h_vmem=64G")
    runfile_arr.append("#$ -shell y")
    runfile_arr.append("#$ -j y")
    runfile_arr.append("#$ -o /lustre/storeA/project/aerocom/logs/aeroval_logs/")
    runfile_arr.append("#$ -e /lustre/storeA/project/aerocom/logs/aeroval_logs/")

    runfile_arr.append('logdir="/lustre/storeA/project/aerocom/logs/aeroval_logs"')
    runfile_arr.append("date=$(date '+%Y%m%d_%H%M%S')")
    runfile_arr.append('logfile="${logdir}/${USER}.${date}.${JOB_NAME}.${JOB_ID}_log.txt"')
    runfile_arr.append(
        "__conda_setup=\"$('/modules/centos7/user-apps/aerocom/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)\""
    )

    runfile_arr.append("if [ $? -eq 0 ]")
    runfile_arr.append('  then eval "$__conda_setup"')
    runfile_arr.append("else")
    runfile_arr.append("  echo conda not working! exiting...")
    runfile_arr.append("  exit 1")
    runfile_arr.append("fi")

    runfile_arr.append('echo "Got $NSLOTS slots for job $SGE_TASK_ID." >> ${logfile}')

    runfile_arr.append("module load aerocom/anaconda3-stable >> ${logfile} 2>&1")
    runfile_arr.append("module list >> ${logfile} 2>&1")

    runfile_arr.append("conda activate pyadev-applied >> ${logfile} 2>&1")
    runfile_arr.append("conda env list >> ${logfile} 2>&1")

    runfile_arr.append("set -x")
    runfile_arr.append("python --version >> ${logfile} 2>&1")
    runfile_arr.append("pwd >> ${logfile} 2>&1")
    runfile_arr.append('echo "starting SUBMITFILE ..." >> ${logfile}')
    runfile_arr.append("python SUBMITFILE >> ${logfile} 2>&1")

    for _file in runfiles:
        pass
        # copy runfile to qsub host (subprocess.run)
        # create submission file (create locally, copy to qsub host (fabric)
        # create tmp directory on submission host (fabric)
        # submit submission file to queue (fabric)


def main():
    """main program"""

    parser = argparse.ArgumentParser(
        description="command line interface to aeroval parallelisation.\n"
        "aeroval config has to to be in the variable CFG for now!\n\n"
    )
    parser.add_argument("files", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("--outdir", help="output directory")
    parser.add_argument("--subdry", help="dryrun for submission to queue", action="store_true")
    parser.add_argument(
        "--jsonrunscript",
        help=f"script to run json config files; defaults to {JSON_RUNSCRIPT}",
        default=JSON_RUNSCRIPT,
    )
    parser.add_argument(
        "--cfgvar",
        help=f"variable that holds the aeroval config in the file(s) provided. Defaults to {DEFAULT_CFG_VAR}",
        default=DEFAULT_CFG_VAR,
    )
    parser.add_argument(
        "--tempdir",
        help=f"directory for temporary files; defaults to {TMP_DIR}",
        default=TMP_DIR,
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

    # these are the files that need to be submitted to the queue
    runfiles = prep_files(options)

    if options["subdry"]:
        # just print the to be run files
        for _runfile in runfiles:
            print(f"{_runfile}")
        pass
    else:
        pass


if __name__ == "__main__":
    main()
