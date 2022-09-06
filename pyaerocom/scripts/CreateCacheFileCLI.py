#!/usr/bin/env python3
"""
cache file generator CLI for pyaerocom

for usage via the PPI queues
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from getpass import getuser
from pathlib import Path

USER = getuser()
TMP_DIR = "/tmp"

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

# Name of conda env to use for running the aeroval analysis
CONDA_ENV = "pyadev-applied"


def write_script(filename: str | Path, var: str = 'od550aer', obsnetwork: str = "AeronetSunV3Lev2.daily"):
    script_proto = f"""#!/usr/bin/env python3
    
from pyaerocom.io import ReadUngridded

def main():
    reader = ReadUngridded("{obsnetwork}")
    data = reader.read(vars_to_retrieve="{var}")

if __name__ == "__main__":
    main()
"""
    with open(filename, "w") as f:
        f.write(script_proto)


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


def main():
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
        description=f"command line interface to pyaerocom cache file generator {script_name}.",
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}
{script_name} --vars concpm10 -o EEAAQeRep.v2

    """
    )
    parser.add_argument("--vars", help="variable name(s) to cache", nargs="+")
    parser.add_argument("-o", "--obsnetworks", help="obs networks(s) names to cache", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("-e", "--env", help=f"conda env used to run the aeroval analysis; defaults to {CONDA_ENV}")
    parser.add_argument("--queue", help=f"queue name to submit the jobs to; defaults to {QSUB_QUEUE_NAME}")
    parser.add_argument("--queue-user", help=f"queue user; defaults to {QSUB_USER}")
    parser.add_argument("--noqsub",
                        help="do not submit to queue (all files created and copied, but no submission)",
                        action="store_true")
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

    parser.add_argument("-l", "--localhost", help="start queue submission on localhost", action="store_true")
    parser.add_argument("-p", "--printobsnetworks", help="just print the names of the supported obs network",
                        action="store_true")

    args = parser.parse_args()
    options = {}
    if args.vars:
        options["vars"] = args.vars

    if args.printobsnetworks:
        from pyaerocom import const

        supported_obs_networks = [
            const.AERONET_SUN_V2L15_AOD_DAILY_NAME,
            const.AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME,
            const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
            const.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME,
            const.AERONET_SUN_V2L2_SDA_DAILY_NAME,
            const.AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME,
            const.AERONET_INV_V2L15_DAILY_NAME,
            const.AERONET_INV_V2L15_ALL_POINTS_NAME,
            const.AERONET_INV_V2L2_DAILY_NAME,
            const.AERONET_INV_V2L2_ALL_POINTS_NAME,
            const.AERONET_SUN_V3L15_AOD_DAILY_NAME,
            const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME,
            const.AERONET_SUN_V3L2_AOD_DAILY_NAME,
            const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME,
            const.AERONET_SUN_V3L15_SDA_DAILY_NAME,
            const.AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME,
            const.AERONET_SUN_V3L2_SDA_DAILY_NAME,
            const.AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME,
            const.AERONET_INV_V3L15_DAILY_NAME,
            const.AERONET_INV_V3L2_DAILY_NAME,
            const.EBAS_MULTICOLUMN_NAME,
            const.EEA_NRT_NAME,
            const.EEA_V2_NAME,
            const.EARLINET_NAME,
            const.MARCO_POLO_NAME,
            const.AIR_NOW_NAME,
        ]

        print(f"supported observational networks:"
              f"{supported_obs_networks}")

    if args.obsnetworks:
        options["obsnetworks"] = args.obsnetworks

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

    if args.localhost:
        options["localhost"] = True
    else:
        options["localhost"] = False

    # generate cache files locally
    scripts_to_run = []
    for obs_network in options['obsnetworks']:
        for var in options['vars']:
            # write python file
            outfile = options["tempdir"].joinpath('create_cache', obs_network, var, 'py')
            write_script(outfile, var=var, obsnetwork=obs_network)
            scripts_to_run.append(outfile)

        if options['localhost']:
            # run the generated cache creation scripts
            cmd_arr = ["ssh", host_str, "mkdir", "-p", qsub_tmp_dir]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr, capture_output=True)
            # start python file as subprocess


if __name__ == "__main__":
    main()
