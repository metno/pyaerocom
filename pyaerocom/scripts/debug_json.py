#!/usr/bin/env python3
"""
small helper program to read a aeroval config from a json file

"""
import argparse

import simplejson as json
from aeroval_parallelise import adjust_hm_ts_file

config_file = (
    "/home/jang/data/aeroval-local-web/pyaerocom_config/config_files/cfg_cams2-82_IFS_beta.py"
)
cfgvar = "CFG"


files = [
    "/home/jang/data/aeroval-local-web/data/testmerge_all/IFS-beta/hm/ts/ALL-AeronetL1.5-d-od550aer-Column.json",
    # "/home/jang/data/aeroval-local-web/data/cams2-82/IFS-beta/hm/ts/ALL-AeronetL1.5-d-od550aer-Column.json",
    "/home/jang/tmp/ALL-AeronetL1.5-d-od550aer-Column.json",
]


def main():
    file_data = []


    adjust_hm_ts_file(
        [files[0]],
        config_file="/home/jang/data/aeroval-local-web/pyaerocom_config/config_files/cfg_cams2-82_IFS_beta.py",
        cfgvar="CFG",
    )
    for _file in files:
        with open(_file, "r") as infile:
            file_data.append(json.load(infile))
    print(file_data[0])


if __name__ == "__main__":
    main()
