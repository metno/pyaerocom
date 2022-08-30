#!/usr/bin/env python3
"""
parallelisation for aeroval processing

- create several aeroval config files from one input config
  (per model and per obs network for now)
- submit these configs to the GridEngine queue

"""

# some ideas what to use
import argparse
import sys
from copy import deepcopy
from datetime import datetime
from fnmatch import fnmatch
from getpass import getuser
from importlib.machinery import SourceFileLoader
from pathlib import Path, PurePosixPath
from socket import gethostname
from tempfile import mkdtemp
from threading import Thread
from typing import Union
from uuid import uuid4

import simplejson as json

DEFAULT_CFG_VAR = "CFG"
RUN_UUID = uuid4()
HOSTNAME = gethostname()
USER = getuser()
TMP_DIR = "/tmp"
# TMP_DIR = f"/home/{USER}/data/aeroval-local-web/data"

JSON_RUNSCRIPT_NAME = "aeroval_run_json_cfg.py"
# qsub binary
QSUB_NAME = "/usr/bin/qsub"
# qsub submission host
QSUB_HOST = "ppi-clogin-a1.met.no"
# directory, where the files will bew transferred before they are run
# Needs to be on Lustre or home since /tmp is not shared between machines
QSUB_DIR = f"/lustre/storeA/users/{USER}/submission_scripts"

# user name on the qsub host
QSUB_USER = USER
# queue name
QSUB_QUEUE_NAME = "research-el7.q"
# log directory
QSUB_LOG_DIR = "/lustre/storeA/project/aerocom/logs/aeroval_logs/"

# some copy constants
REMOTE_CP_COMMAND = ["scp", "-v"]
CP_COMMAND = ["cp", "-v"]

# script start time
START_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

# assume that the script to run the aeroval json file is in the same directory as this script
# JSON_RUNSCRIPT = Path(Path(__file__).parent).joinpath(JSON_RUNSCRIPT_NAME)
JSON_RUNSCRIPT = JSON_RUNSCRIPT_NAME

# some constants for the merge operation
# files not noted here will be copied
# list of file masks to merge

MERGE_EXP_FILES_TO_COMBINE = [
    "ts/*.json",
    "hm/ts/*.json",
    "menu.json",
    "ranges.json",
    "regions.json",
    "statistics.json",
    "hm/glob_stats_*.json",
    "cfg_*.json",
]
# list of file masks not to touch
MERGE_EXP_FILES_TO_EXCLUDE = []
# the config file need to be merged and have a special name
MERGE_EXP_CFG_FILES = ["cfg_*.json"]
# Name of conda env to use for running the aeroval analysis
CONDA_ENV = "pyadev-applied"


def prep_files(options):
    """preprare the aeroval config files to run
    return a list of files

    """
    runfiles = []

    for _file in options["files"]:
        # read aeroval config file
        if fnmatch(_file, "*.py"):
            foo = SourceFileLoader("bla", _file).load_module()
            # the following line does unfortunately not work since a module is not subscriptable
            # CFG = foo[options["cfgvar"]]
            # use getattr instead
            cfg = deepcopy(getattr(foo, options["cfgvar"]))

        elif fnmatch(_file, "*.json"):
            cfg = json.load(_file)
        else:
            print(f"skipping file {_file} due to wrong file extension")
            continue

        # create tmp dir
        tempdir = mkdtemp(dir=options["tempdir"])

        # make some adjustments to the config file
        # e.g. adjust the json_basedir and the coldata_basedir entries
        if "json_basedir" in options:
            cfg['json_basedir'] = options['json_basedir']

        if "coldata_basedir" in options:
            cfg['coldata_basedir'] = options['coldata_basedir']

        if "io_aux_file" in options:
            cfg['io_aux_file'] = options['io_aux_file']

        # index for temporary data directories
        dir_idx = 1
        for _model in cfg["model_cfg"]:
            out_cfg = deepcopy(cfg)
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
                ] = f"{out_cfg['json_basedir']}/{Path(tempdir).parts[-1]}.{dir_idx:04d}"
                out_cfg[
                    "coldata_basedir"
                ] = f"{out_cfg['coldata_basedir']}/{Path(tempdir).parts[-1]}.{dir_idx:04d}"
                cfg_file = PurePosixPath(_file).stem
                outfile = PurePosixPath(tempdir).joinpath(f"cfg_file_{_model}_{_obs_network}.json")
                print(f"writing file {outfile}")
                with open(outfile, "w", encoding="utf-8") as j:
                    json.dump(out_cfg, j, ensure_ascii=False, indent=4)
                dir_idx += 1
                runfiles.append(outfile)
                if options["verbose"]:
                    print(out_cfg)

    return runfiles


def get_runfile_str_arr(
        file,
        queue_name=QSUB_QUEUE_NAME,
        script_name=None,
        # wd=QSUB_DIR,
        wd=None,
        mail=f"{QSUB_USER}@met.no",
        logdir=QSUB_LOG_DIR,
        date=START_TIME,
        conda_env='pyadev-applied',
):
    """create list of strings with runfile for gridengine"""
    # create runfile

    if wd is None:
        wd = Path(file).parent

    if script_name is None:
        script_name = str(file.with_name(f"{file.stem}{'.run'}"))
    elif isinstance(script_name, Path):
        script_name = str(script_name)

    runfile_arr = []
    runfile_arr.append("#!/bin/bash -l")
    runfile_arr.append("#$ -S /bin/bash")
    # runfile_arr.append("#$ -N AEROVAL_NAME")
    runfile_arr.append(f"#$ -N {Path(file).stem}")
    # runfile_arr.append("#$ -q research-el7.q")
    runfile_arr.append(f"#$ -q {queue_name}")
    runfile_arr.append("#$ -pe shmem-1 1")
    # runfile_arr.append("#$ -wd /home/UUSER/data/aeroval-local-web/pyaerocom_config/config_files")
    runfile_arr.append(f"#$ -wd {wd}")
    runfile_arr.append("#$ -l h_rt=96:00:00")
    runfile_arr.append("#$ -l s_rt=96:00:00")
    # runfile_arr.append("#$ -M UUSER@met.no")
    if mail is not None:
        runfile_arr.append(f"#$ -M {mail}")
    runfile_arr.append("#$ -m abe")
    runfile_arr.append("#$ -l h_vmem=20G")
    runfile_arr.append("#$ -shell y")
    runfile_arr.append("#$ -j y")
    # runfile_arr.append("#$ -o /lustre/storeA/project/aerocom/logs/aeroval_logs/")
    # runfile_arr.append("#$ -e /lustre/storeA/project/aerocom/logs/aeroval_logs/")
    runfile_arr.append(f"#$ -o {logdir}/")
    runfile_arr.append(f"#$ -e {logdir}/")

    runfile_arr.append(f"logdir='{logdir}/'")
    runfile_arr.append(f"date={date}")
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

    runfile_arr.append(f"conda activate {conda_env} >> ${{logfile}} 2>&1")
    runfile_arr.append("conda env list >> ${logfile} 2>&1")

    runfile_arr.append("set -x")
    runfile_arr.append("python --version >> ${logfile} 2>&1")
    runfile_arr.append("pwd >> ${logfile} 2>&1")
    runfile_arr.append('echo "starting FILE ..." >> ${logfile}'.replace("FILE", str(file)))
    runfile_arr.append(
        "JSON_RUNSCRIPT FILE >> ${logfile} 2>&1".replace(
            "JSON_RUNSCRIPT", str(JSON_RUNSCRIPT)
        ).replace("FILE", str(file))
    )
    runfile_arr.append("")
    return runfile_arr


def run_queue(
        runfiles: list[str],
        qsub_host: str = QSUB_HOST,
        qsub_cmd: str = QSUB_NAME,
        qsub_dir: str = QSUB_DIR,
        qsub_user: str = QSUB_USER,
        qsub_queue: str = QSUB_QUEUE_NAME,
        submit_flag: bool = False,
        options: dict = {},
):
    """submit runfiles to the remote cluster

    # copy runfile to qsub host (subprocess.run)
    # create submission file (create locally, copy to qsub host (fabric)
    # create tmp directory on submission host (fabric)
    # submit submission file to queue (fabric)

    """

    # to enable test usage, import fabric only here
    import subprocess

    qsub_tmp_dir = Path.joinpath(Path(qsub_dir), f"qsub.{runfiles[0].parts[-2]}")

    # localhost_flag = False
    # if "localhost" in qsub_host or platform.node() in qsub_host:
    #     localhost_flag = True

    for idx, _file in enumerate(runfiles):
        # copy runfiles to qsub host if qsub host is not localhost
        if not options["localhost"]:
            # create tmp dir on qsub host; retain some parts
            host_str = f"{qsub_user}@{qsub_host}"
            if idx == 0:
                cmd_arr = ["ssh", host_str, "mkdir", "-p", qsub_tmp_dir]
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    continue
                else:
                    print("success...")

            # copy aeroval config file to qsub host
            host_str = f"{qsub_user}@{qsub_host}:{qsub_tmp_dir}/"
            cmd_arr = [*REMOTE_CP_COMMAND, _file, host_str]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr, capture_output=True)
            if sh_result.returncode != 0:
                continue
            else:
                print("success...")
            # create qsub runfile and copy that to the qsub host
            qsub_run_file_name = _file.with_name(f"{_file.stem}{'.run'}")
            remote_qsub_run_file_name = Path.joinpath(qsub_tmp_dir, qsub_run_file_name.name)
            remote_json_file = Path.joinpath(qsub_tmp_dir, _file.name)
            dummy_arr = get_runfile_str_arr(
                remote_json_file, wd=qsub_tmp_dir, script_name=remote_qsub_run_file_name
            )
            print(f"writing file {qsub_run_file_name}")
            with open(qsub_run_file_name, "w") as f:
                f.write("\n".join(dummy_arr))

            # copy runfile to qsub host
            host_str = f"{qsub_user}@{qsub_host}:{qsub_tmp_dir}/"
            cmd_arr = [*REMOTE_CP_COMMAND, qsub_run_file_name, host_str]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr, capture_output=True)
            if sh_result.returncode != 0:
                continue
            else:
                print("success...")

            # run qsub
            # unfortunatly qsub can't be run directly for some reason (likely security)
            # create a script with the qsub call and start that
            host_str = f"{qsub_user}@{qsub_host}:{qsub_tmp_dir}/"
            qsub_start_file_name = _file.with_name(f"{_file.stem}{'.sh'}")
            remote_qsub_run_file_name = Path.joinpath(qsub_tmp_dir, qsub_run_file_name.name)
            remote_qsub_start_file_name = Path.joinpath(qsub_tmp_dir, qsub_start_file_name.name)
            # this does not work:
            # cmd_arr = ["ssh", host_str, "/usr/bin/bash", "-l", "qsub", remote_qsub_run_file_name]
            # use bash script as workaround
            start_script_arr = []
            start_script_arr.append("#!/bin/bash -l")
            start_script_arr.append(f"qsub {remote_qsub_run_file_name}")
            start_script_arr.append("")
            with open(qsub_start_file_name, "w") as f:
                f.write("\n".join(start_script_arr))
            cmd_arr = [*REMOTE_CP_COMMAND, qsub_start_file_name, host_str]
            if submit_flag:
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    continue
                else:
                    print("success...")

                host_str = f"{qsub_user}@{qsub_host}"
                cmd_arr = ["ssh", host_str, "/usr/bin/bash", "-l", remote_qsub_start_file_name]
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    print(f"return code: {sh_result.returncode}")
                    print(f"{sh_result.stderr}")
                    continue
                else:
                    print("success...")
                    print(f"{sh_result.stdout}")

            else:
                print(f"qsub files created and copied to {qsub_host}.")
                print(
                    f"you can start the job with the command: qsub {remote_qsub_run_file_name} on the host {qsub_host}."
                )

        else:
            # localhost flag is set
            # scripts exist already, but in /tmp where the queue nodes can't read them
            # copy to submission directories
            # create tmp dir on qsub host; retain some parts
            # host_str = f"{qsub_user}@{qsub_host}"
            if idx == 0:
                cmd_arr = ["mkdir", "-p", qsub_tmp_dir]
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    continue
                else:
                    print("success...")

            # copy aeroval config file to qsub host
            host_str = f"{qsub_tmp_dir}/"
            cmd_arr = [*CP_COMMAND, _file, host_str]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr, capture_output=True)
            if sh_result.returncode != 0:
                continue
            else:
                print("success...")
            # create qsub runfile and copy that to the qsub host
            qsub_run_file_name = _file.with_name(f"{_file.stem}{'.run'}")
            remote_qsub_run_file_name = Path.joinpath(qsub_tmp_dir, qsub_run_file_name.name)
            remote_json_file = Path.joinpath(qsub_tmp_dir, _file.name)
            dummy_arr = get_runfile_str_arr(
                remote_json_file, wd=qsub_tmp_dir, script_name=remote_qsub_run_file_name
            )
            print(f"writing file {qsub_run_file_name}")
            with open(qsub_run_file_name, "w") as f:
                f.write("\n".join(dummy_arr))

            # copy runfile to qsub host
            host_str = f"{qsub_tmp_dir}/"
            cmd_arr = [*CP_COMMAND, qsub_run_file_name, host_str]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr, capture_output=True)
            if sh_result.returncode != 0:
                continue
            else:
                print("success...")

            # run qsub
            # unfortunatly qsub can't be run directly for some reason (likely security)
            # create a script with the qsub call and start that
            host_str = f"{qsub_tmp_dir}/"
            qsub_start_file_name = _file.with_name(f"{_file.stem}{'.sh'}")
            remote_qsub_run_file_name = Path.joinpath(qsub_tmp_dir, qsub_run_file_name.name)
            remote_qsub_start_file_name = Path.joinpath(qsub_tmp_dir, qsub_start_file_name.name)
            # this does not work:
            # cmd_arr = ["ssh", host_str, "/usr/bin/bash", "-l", "qsub", remote_qsub_run_file_name]
            # use bash script as workaround
            start_script_arr = []
            start_script_arr.append("#!/bin/bash -l")
            start_script_arr.append(f"qsub {remote_qsub_run_file_name}")
            start_script_arr.append("")
            with open(qsub_start_file_name, "w") as f:
                f.write("\n".join(start_script_arr))
            cmd_arr = [*CP_COMMAND, qsub_start_file_name, host_str]
            if submit_flag:
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    continue
                else:
                    print("success...")

                host_str = f"{sub_user}@{qsub_host}"
                cmd_arr = ["/usr/bin/bash", "-l", remote_qsub_start_file_name]
                print(f"running command {' '.join(map(str, cmd_arr))}...")
                sh_result = subprocess.run(cmd_arr, capture_output=True)
                if sh_result.returncode != 0:
                    print(f"return code: {sh_result.returncode}")
                    print(f"{sh_result.stderr}")
                    continue
                else:
                    print("success...")
                    print(f"{sh_result.stdout}")

            else:
                print(f"qsub files created on localhost.")
                print(
                    f"you can start the job with the command: qsub {remote_qsub_run_file_name} on the host {qsub_host}."
                )


def combine_output(options: dict):
    """combine the json files of the parallelised outputs to a single target directory (experiment)"""
    import shutil

    # create outdir
    try:
        # remove files first
        try:
            shutil.rmtree(options["outdir"])
        except FileNotFoundError:
            pass
        Path.mkdir(options["outdir"], exist_ok=False)
    except FileExistsError:
        pass

    for idx, combinedir in enumerate(options["files"]):
        # tmp dirs look like this: tmpggb7k02d.0001, tmpggb7k02d.0002
        # create common assembly directory
        # assemble the data
        # move the experiment to the target directory

        print(f"input dir: {combinedir}")
        # {experiment_name}/experiments.json: files are identical over one parallelisation run
        if idx == 0:
            # copy first directory to options['outdir']
            for dir_idx, dir in enumerate(Path(combinedir).iterdir()):
                # there should be just one directory. Use the 1st only anyway
                if dir_idx == 0:
                    exp_dir = [child for child in dir.iterdir() if Path.is_dir(child)][0]

                    shutil.copytree(dir, options["outdir"], dirs_exist_ok=True)
                    out_target_dir = Path.joinpath(options["outdir"], exp_dir.name)
                    # adjust config file name to cfg_<project_name>_<experiment_name>.json
                    cfg_file = out_target_dir.joinpath(
                        f"cfg_{exp_dir.parts[-2]}_{exp_dir.parts[-1]}.json"
                    )
                    if cfg_file.exists():
                        new_cfg_file = out_target_dir.joinpath(
                            f"cfg_{options['outdir'].parts[-1]}_{exp_dir.parts[-1]}.json"
                        )
                        cfg_file.rename(new_cfg_file)
                        # TODO: adjust some parts of the config file to the new project name
                else:
                    pass
                    # There's something wrong with the directory structure!
        else:
            # workdir: combinedir/<model_dir>
            # cfg_testing_IASI.json  contour  hm  map  menu.json  ranges.json  regions.json  scat  statistics.json  ts
            inpath = Path(combinedir).joinpath(*list(exp_dir.parts[-2:]))
            inpath_dir_len = len(inpath.parts)
            for file_idx, _file in enumerate(sorted(inpath.glob("**/*.*json"))):
                # determine if file is in inpath or below
                tmp = _file.parts[inpath_dir_len:]
                if len(tmp) == 1:
                    cmp_file = tmp[0]
                else:
                    cmp_file = Path.joinpath(Path(*list(tmp)))

                out_target_dir = Path.joinpath(options["outdir"], exp_dir.name)
                if match_file(cmp_file, MERGE_EXP_FILES_TO_EXCLUDE):
                    # skip some files for now
                    print(f"file {_file} excluded for now")
                    continue
                elif match_file(cmp_file, MERGE_EXP_CFG_FILES):
                    # special treatment for the experiment configuration
                    # file names need to be adjusted
                    cfg_file = inpath.joinpath(f"cfg_{inpath.parts[-2]}_{inpath.parts[-1]}.json")
                    outfile = out_target_dir.joinpath(
                        f"cfg_{options['outdir'].parts[-1]}_{inpath.parts[-1]}.json"
                    )
                    if outfile.exists():
                        # sould always fire since we handle the 1st directory above
                        infiles = [cfg_file, outfile]
                        print(f"writing combined json file {outfile}...")
                        t = Thread(target=combine_json_files, args=(infiles, outfile))
                        t.start()
                        # combine_json_files(infiles, outfile)
                        # TODO:
                        #  probably Adjust {
                        #   "proj_info": {
                        #     "proj_id": "testing"
                        #   },
                        # and
                        #   "path_manager": {
                        # "proj_id": "testing",
                        # "exp_id": "IASI",
                        # "json_basedir": "/home/jang/data/aeroval-local-web/data/tmpggb7k02d.0001",
                        # "coldata_basedir": "/home/jang/data/aeroval-local-web/coldata/tmpggb7k02d.0001"
                        # },
                        # (should be options['outdir'].parts[-1])
                    else:
                        # copy
                        pass

                else:
                    if match_file(cmp_file, MERGE_EXP_FILES_TO_COMBINE):
                        # combine files
                        outfile = out_target_dir.joinpath(cmp_file)
                        if outfile.exists():
                            infiles = [_file, outfile]
                            print(f"writing combined json file {outfile}...")
                            combine_json_files(infiles, outfile)
                        else:
                            # copy file
                            print(
                                f"non-existing outfile for merge. Copying {_file} to {outfile}..."
                            )
                            shutil.copy2(_file, outfile)
                    else:
                        # copy file
                        outfile = out_target_dir.joinpath(cmp_file)
                        print(f"copying {_file} to {outfile}...")
                        shutil.copy2(_file, outfile)

        pass


def combine_json_files(infiles: list[str], outfile: str) -> dict:
    """small helper to ingest infile into outfile"""

    result = {}
    for infile in infiles:
        # the target file might not exist e.g. due to missing model data at station location
        try:
            with open(infile, "r") as inhandle:
                # result.update(json.load(inhandle))
                result = dict_merge(result, json.load(inhandle))
        except FileNotFoundError:
            result = json.load(inhandle)

    with open(outfile, "w") as outhandle:
        json.dump(result, outhandle, ensure_ascii=False, indent=4)


def dict_merge(dct: Union[None, dict], merge_dct: dict):
    """Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: dct
    """
    if dct is None:
        dct = deepcopy(merge_dct)
    else:
        for k, v in merge_dct.items():
            if k in dct:
                if isinstance(dct[k], dict) and isinstance(merge_dct[k], dict):
                    dict_merge(dct[k], merge_dct[k])
                else:
                    dct[k] = deepcopy(merge_dct[k])
            else:
                dct[k] = deepcopy(merge_dct[k])

    return dct


def match_file(
        file: str, file_mask_array: Union[str, list[str]] = MERGE_EXP_FILES_TO_COMBINE
) -> bool:
    """small hekper that matches a filename agains a list if wildcards"""
    if isinstance(file_mask_array, str):
        file_mask_array = [file_mask_array]

    ret_val = False
    for _file_mask in file_mask_array:
        if fnmatch(file, _file_mask):
            ret_val = True
            break
    return ret_val


def main():
    """main program"""

    colors = {
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m'}
    # DARKCYAN = '\033[36m'
    # BLUE = '\033[94m'
    # GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    # RED = '\033[91m'
    script_name = Path(sys.argv[0]).name
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="command line interface to aeroval parallelisation.",
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}

{colors['UNDERLINE']}run script on qsub host and do not submit jobs to queue:{colors['END']}
    {script_name} --noqsub -l <cfg-file>

{colors['UNDERLINE']}run script on workstation, set directory of aeroval files and submit to queue via qsub host:{colors['END']}
   {script_name}  --remotetempdir <directory for aeroval files> <cfg-file>
   
   Note that the directory for aeroval files needs to be on a common file system for all cluster machines.
   
{colors['UNDERLINE']}set data directories and submit to queue:{colors['END']}
    {script_name} --json_basedir /tmp/data --coldata_basedir /tmp/coldata --io_aux_file /tmp/gridded_io_aux.py <cfg-file>

{colors['UNDERLINE']}assemble aeroval data after a parallel run has been finished: (runs always on the local machine){colors['END']}
    {script_name} -c -o <output directory> <input directories>
    {script_name} -c -o ${{HOME}}/tmp ${{HOME}}/tmpt39n2gp_*
    
"""
    )
    parser.add_argument("files", help="file(s) to read, directories to combine (if -c switch is used)", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("-e", "--env", help=f"conda env used to run the aeroval analysis; defaults to {CONDA_ENV}")
    parser.add_argument("--queue", help=f"queue name to submit the jobs to; defaults to {QSUB_QUEUE_NAME}")
    parser.add_argument("--queue-user", help=f"queue user; defaults to {QSUB_USER}")
    parser.add_argument("--noqsub",
                        help="do not submit to queue (all files created and copied, but no submission)",
                        action="store_true")
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
    parser.add_argument(
        "--remotetempdir",
        help=f"directory for temporary files on qsub node; defaults to {TMP_DIR}",
        default=TMP_DIR,
    )
    parser.add_argument("--json_basedir", help="set json_basedir in the config manually", )
    parser.add_argument("--coldata_basedir", help="set coldata_basedir in the configuration manually",
                        )
    parser.add_argument("--io_aux_file", help="set io_aux_file in the configuration file manually", )

    parser.add_argument("-l", "--localhost", help="start queue submission on localhost", action="store_true")
    parser.add_argument("-c", "--combinedirs", help="combine the output of a parallel runs", action="store_true")
    parser.add_argument("-o", "--outdir", help="output directory for experiment assembly")

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

    if args.noqsub:
        options["noqsub"] = True
    else:
        options["noqsub"] = False

    if args.env:
        options["conda_env_name"] = args.env

    if args.queue:
        options['qsub_queue_name'] = args.queue
    else:
        options['qsub_queue_name'] = QSUB_QUEUE_NAME

    if args.queue_user:
        options['qsub_user'] = args.queue_user
    else:
        options['qsub_user'] = QSUB_USER

    if args.tempdir:
        options["tempdir"] = Path(args.tempdir)

    if args.remotetempdir:
        options["remotetempdir"] = Path(args.remotetempdir)

    if args.cfgvar:
        options["cfgvar"] = args.cfgvar

    if args.json_basedir:
        options["json_basedir"] = args.json_basedir

    if args.coldata_basedir:
        options["coldata_basedir"] = args.coldata_basedir

    if args.io_aux_file:
        options["io_aux_file"] = args.io_aux_file

    if args.combinedirs:
        options["combinedirs"] = True
    else:
        options["combinedirs"] = False

    if args.localhost:
        options["localhost"] = True
    else:
        options["localhost"] = False

    if args.outdir:
        options["outdir"] = Path(args.outdir)

    # make sure that if -c switch is given also the -o option is there
    if options['combinedirs'] and 'outdir' not in options:
        error_str = """Error: -c switch given but no output directory defined. 
Please add an output directory using the -o switch."""
        print(error_str)
        sys.exit(1)

    if options['localhost']:
        info_str = "INFO: starting queue submission on localhost (-l flag is set)."
        print(info_str)

    if not options["combinedirs"]:
        # create file for the queue
        runfiles = prep_files(options)
        if options["noqsub"] and options['verbose']:
            # just print the to be run files
            for _runfile in runfiles:
                print(f"created {_runfile}")
            pass
        else:
            run_queue(runfiles, submit_flag=(not options["noqsub"]), options=options)

    else:
        result = combine_output(options)


if __name__ == "__main__":
    main()
