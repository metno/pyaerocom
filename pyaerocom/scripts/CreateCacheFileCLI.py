#!/usr/bin/env python3
"""
cache file generator CLI for pyaerocom

for usage via the PPI queues
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from getpass import getuser
from pathlib import Path
from tempfile import mkdtemp

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
    import os
    import stat
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

    # make executable
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)


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

    runfile_str = f"""#!/bin/bash -l
#$ -N {Path(file).stem}
#$ -q {queue_name}
#$ -pe shmem-1 1
#$ -wd {wd}
#$ -l h_rt=96:00:00
#$ -l s_rt=96:00:00
"""

    if mail is not None:
        runfile_str += f"#$ -M {mail}\n"
    runfile_str += f"""#$ -m abe
#$ -l h_vmem=20G
#$ -shell y
#$ -j y
#$ -o {logdir}/
#$ -e {logdir}/
logdir="{logdir}/"
date="{date}"
logfile="${{logdir}}/${{USER}}.${{date}}.${{JOB_NAME}}.${{JOB_ID}}_log.txt"
__conda_setup=$('/modules/centos7/user-apps/aerocom/anaconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)
if [ $? -eq 0 ]
then eval "$__conda_setup"
else
  echo conda not working! exiting...
  exit 1
fi
echo "Got $NSLOTS slots for job $SGE_TASK_ID." >> ${{logfile}}
module load aerocom/anaconda3-stable >> ${{logfile}} 2>&1
module list >> ${{logfile}} 2>&1
conda activate {conda_env} >> ${{logfile}} 2>&1
conda env list >> ${{logfile}} 2>&1
set -x
python --version >> ${{logfile}} 2>&1
pwd >> ${{logfile}} 2>&1
echo "starting {file} ..." >> ${{logfile}}
{file} >> ${{logfile}} 2>&1

"""
    # runfile_arr.append(
    #     "JSON_RUNSCRIPT FILE >> ${logfile} 2>&1".replace(
    #         "JSON_RUNSCRIPT", str(JSON_RUNSCRIPT)
    #     ).replace("FILE", str(file))
    # )"""
    #     runfile_arr.append("")
    return runfile_str


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
{colors['UNDERLINE']}start cache creation serially on localhost{colors['END']}
{script_name} --vars concpm10 concpm25 -o EEAAQeRep.v2

{colors['UNDERLINE']}start cache creation parallel on qsub host (current host is NOT qsub host){colors['END']}
{script_name} --qsub --vars ang4487aer od550aer -o AeronetSunV3Lev2.daily

{colors['UNDERLINE']}start cache creation parallel on qsub host (current host IS qsub host){colors['END']}
{script_name} -l --qsub --vars concpm10 concpm25 vmro3 concno2 -o EEAAQeRep.NRT

    """
    )
    parser.add_argument("--vars", help="variable name(s) to cache", nargs="+")
    parser.add_argument("-o", "--obsnetworks", help="obs networks(s) names to cache", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")

    parser.add_argument("-e", "--env", help=f"conda env used to run the aeroval analysis; defaults to {CONDA_ENV}")
    parser.add_argument("--queue", help=f"queue name to submit the jobs to; defaults to {QSUB_QUEUE_NAME}")
    parser.add_argument("--queue-user", help=f"queue user; defaults to {QSUB_USER}")
    parser.add_argument("--qsub",
                        help="submit to queue using the qsub command",
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
        sys.exit(0)

    if args.obsnetworks:
        options["obsnetworks"] = args.obsnetworks

    if args.verbose:
        options["verbose"] = True
    else:
        options["verbose"] = False

    if args.qsub:
        options["qsub"] = True
    else:
        options["qsub"] = False

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
    # create tmp dir
    tempdir = Path(mkdtemp(dir=options["tempdir"]))
    for obs_network in options['obsnetworks']:
        for var in options['vars']:
            # write python file
            outfile = tempdir.joinpath('_'.join(['create_cache', obs_network, var + '.py']))
            write_script(outfile, var=var, obsnetwork=obs_network)
            scripts_to_run.append(outfile)

    if options['localhost'] or options['qsub']:
        # run qsub on localhost (localhost is qsub host)
        pass
        run_queue(scripts_to_run, submit_flag=(options["qsub"]), options=options)
    # elif not options['localhost'] and options['qsub']:
    #     pass
    #     # localhost is not qsub host
    #     # create qsub run script, copy that to qsub host and run it
    #     run_queue(scripts_to_run, submit_flag=(options["qsub"]), options=options)
    else:
        # run serially on localhost
        for _script in scripts_to_run:
            cmd_arr = [_script]
            print(f"running command {' '.join(map(str, cmd_arr))}...")
            sh_result = subprocess.run(cmd_arr)
            # sh_result = subprocess.run(cmd_arr, capture_output=True)
            if sh_result.returncode != 0:
                continue
            else:
                print("success...")


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

            # copy python runfile to qsub host
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
            dummy_str = get_runfile_str_arr(
                remote_json_file, wd=qsub_tmp_dir, script_name=remote_qsub_run_file_name
            )
            print(f"writing file {qsub_run_file_name}")
            with open(qsub_run_file_name, "w") as f:
                f.write(dummy_str)

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
            start_script_str = f"""#!/bin/bash -l
qsub {remote_qsub_run_file_name}

"""
            with open(qsub_start_file_name, "w") as f:
                f.write(start_script_str)
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
                sh_result = subprocess.run(cmd_arr)
                if sh_result.returncode != 0:
                    print(f"qsub failed!")
                    continue
                else:
                    print("success...")

            else:
                print(f"qsub files created and copied to {qsub_host}.")
                print(
                    f"you can start the job with the command: qsub {remote_qsub_run_file_name} on the host {qsub_host}."
                )

        else:
            # localhost flag is set
            # scripts exist already, but in /tmp where the queue nodes can't read them
            # copy to submission directories
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
            dummy_str = get_runfile_str_arr(
                remote_json_file, wd=qsub_tmp_dir, script_name=remote_qsub_run_file_name
            )
            print(f"writing file {qsub_run_file_name}")
            with open(qsub_run_file_name, "w") as f:
                f.write(dummy_str)

            # copy runfile to qsub submission directory
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
                    f"you can start the job with the command: qsub {remote_qsub_run_file_name}."
                )


if __name__ == "__main__":
    main()
