#!/usr/bin/env python3

"""simple script to generate a small enough test data set for the EBAS obs network
Works only if the user has access to the standard EBAS data path at Met Norway
"""

import os
import shutil
from pathlib import Path

import simplejson

import pyaerocom as pya

# import pyaerocom.access_testdata as td
from pyaerocom.access_testdata import AccessTestData

# from getpass import getuser
#
# if getuser() == 'jonasg':
#     ebas_local = os.path.join(pya.const.OUTPUTDIR, 'data/obsdata/EBASMultiColumn/data')
#     assert os.path.exists(ebas_local)
# else:
#     ebas_local=None


tda = AccessTestData()

TESTDATADIR = tda.basedir

OUTBASE = Path(TESTDATADIR).joinpath("testdata-minimal/obsdata/EBASMultiColumn")
SCRIPT_BASE_DIR = Path(TESTDATADIR).joinpath("testdata-minimal/scripts")

FILES_DEST = OUTBASE.joinpath("data")

UPDATE = True
UPDATE_EXISTING = False
SEARCH_PROBLEM_FILES = False
NAME = "EBASMC"

# if ebas_local is not None:
#     FILES_SRC = ebas_local
# else:
EBAS_BASE_DIR = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/"
assert os.path.exists(EBAS_BASE_DIR)

JSON_FILE = SCRIPT_BASE_DIR.joinpath("ebas_files.json")

# ------------------------------------------------------------
# add some files with known problems
# at the moment these are static files whose names might change with every data set update
# from Nilu
# ------------------------------------------------------------
add_files = {
    # conco3 tower - 3 different measurement heights
    "o3_tower": "CZ0003R.20150101000000.20181107114213.uv_abs.ozone.air.1y.1h..CZ06L_uv_abs.lev2.nas",
    # conco3 Neg. meas periods
    "o3_neg_dt": "NZ0003G.20090110030000.20181130115605.uv_abs.ozone.air.9h.1h.US06L_Thermo_49C_LAU.US06L_AM.lev2.nas",
    # conco3 - Most common meas period is 150s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    "o3_tstype": "LT0015R.20080101000000.20081231000000.uv_abs.ozone.air.15d.1h.LT01L_uv_abs_15.LT01L_uv_abs..nas",
    # concpm10 - could not resolve unique data column for concpm10 (EBAS varname: ['pm10_mass'])
    "pm10_colsel": "ID1013R.20180101000000.20200102000000.beta_gauge_particulate_sampler.pm10_mass.pm10.1y.1h.ID01L_MetOne_BAM1020..lev2.nas",
    # concpm10 Aliartos - Most common meas period is 172800s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    "pm10_tstype": "GR0001R.20060119000000.20080120000000.b-attenuation.pm10_mass.pm10.11mo.1w.GR01L_b_att_01.GR01L_b-attenuation..nas",
}


def check_outdated(filedir):
    all_files = os.listdir(filedir)

    ok = True
    files_invalid = []
    files_valid = []

    with open(JSON_FILE) as f:
        data = simplejson.load(f, allow_nan=True)

    for var, stats in data.items():
        for stat, files in stats.items():
            for file in files:
                if file not in all_files:
                    print("OUTDATED", var, stat)
                    print(file)
                    files_invalid.append(file)
                    ok = False
                else:
                    files_valid.append(file)

    for key, file in add_files.items():
        if file not in all_files:
            print("OUTDATED (add_files)", key)
            print(file)
            files_invalid.append(file)
            ok = False
        else:
            files_valid.append(file)
    return ok, files_valid, files_invalid


def get_files_var_statlist(data, var, statlist, overlap_found):
    files = {}
    for stat in statlist:
        meta_match = data.find_station_meta_indices(stat)

        for i, idx in enumerate(meta_match):
            try:
                sd = data.to_station_data(idx, var)
            except pya.exceptions.DataCoverageError:
                continue
            if len(sd[var].dropna()) > 10:
                fname = sd.filename
                if ";" in fname:
                    raise ValueError("FATAL", var, stat)
                files[sd.station_name] = [sd.filename]
                break

        if not overlap_found:
            for left, right in zip(meta_match[:-1], meta_match[1:]):
                try:
                    sdl = data.to_station_data(left, var)
                    sdr = data.to_station_data(right, var)
                except pya.exceptions.DataCoverageError:
                    continue
                f0, f1 = sdl.filename, sdr.filename
                merged = sdl.merge_other(sdr, var)
                if var in merged.overlap:
                    files[sdl.station_name] = [f0, f1]
                    overlap_found = True
    return files, overlap_found


def get_files_var_statnum(data, var, statnum):
    files = {}
    numfound = 0
    allstats = data.unique_station_names
    for stat in allstats:
        if numfound == statnum:
            break
        meta_match = data.find_station_meta_indices(stat)

        for i, idx in enumerate(meta_match):
            try:
                sd = data.to_station_data(idx, var)
            except pya.exceptions.DataCoverageError:
                continue
            if len(sd[var].dropna()) > 10:
                fname = sd.filename
                if ";" in fname:
                    raise ValueError("FATAL", var, stat)
                files[sd.station_name] = [sd.filename]
                numfound += 1
                break
    return files


def main():
    # reader = pya.io.ReadUngridded(NAME, data_dir=EBAS_BASE_DIR)
    reader = pya.io.ReadUngridded(
        NAME,
    )
    r_lowlev = reader.get_lowlevel_reader(NAME)

    # r_lowlev._dataset_path = ebas_local

    # directory containing NASA Ames files
    FILEDIR_SRC = r_lowlev.file_dir
    print("checking for invalid files in static file list...")
    CURRENT_OK, files_valid, files_invalid = check_outdated(FILEDIR_SRC)
    print("done...")

    if not CURRENT_OK:
        print(f"outdated files: {files_invalid}")
        print("---------------------WARNING------------------------------")
        print(
            "Some files in current EBAS subset do not exist anymore in "
            "the most recent EBAS database, consider updating them"
        )
        print("---------------------WARNING------------------------------")
        raise Exception

    if not OUTBASE.exists():
        OUTBASE.mkdir()

    if not FILES_DEST.exists():
        FILES_DEST.mkdir()

    if (
        SEARCH_PROBLEM_FILES
    ):  # use this block to find interesting files, e.g. that throw certain exceptions
        var = "concpm10"
        f0 = 1100
        f1 = f0 + 1000

        reader = pya.io.ReadEbas()
        reader.read(var, first_file=f0, last_file=f1)
        for i, file in enumerate(reader.files_failed):
            try:
                data = reader.read_file(file, var)
            except Exception as e:
                print(i)
                print(os.path.basename(file))
                print(e)
                try:
                    fd = pya.io.EbasNasaAmesFile(file)
                    print(fd.station_name)
                except Exception as e:
                    print(e)

    else:
        infofile = JSON_FILE
        if os.path.exists(infofile):
            with open(infofile) as f:
                current_files = simplejson.load(f, allow_nan=True)
        else:
            current_files = {}

        VARS_STATFIX = ["sc550dryaer", "ac550aer", "conco3", "concpm10"]
        VARS_STATVAR_NUM = 2
        VARS_STATVAR = ["concno2", "vmrno2", "vmro3", "concpm25"]

        STATSFIX = ["Jungfraujoch", "Birkenes II", "*Kosetice*", "Troll"]

        all_files = {}
        overlap_found = False
        for var in VARS_STATFIX + VARS_STATVAR:
            if var in current_files and not UPDATE_EXISTING:
                all_files[var] = current_files[var]
                continue
            print(var)
            ropts = {}
            if var.startswith("conc") or var.startswith("vmr"):
                ropts["try_convert_vmr_conc"] = False
            print(f"reading var {var}")
            data = reader.read(NAME, var, **ropts)
            print("reading done")
            if var in VARS_STATFIX:
                files, overlap_found = get_files_var_statlist(data, var, STATSFIX, overlap_found)
            else:
                files = get_files_var_statnum(data, var, VARS_STATVAR_NUM)
            all_files[var] = files

        if not UPDATE:
            print("NOTHING WILL BE COPIED TO TEST DATA")
        else:
            src = Path(EBAS_BASE_DIR).joinpath("data")
            print(f"updating test data @ {r_lowlev.DATASET_PATH}")

            # copy revision file
            revision_file = os.path.join(r_lowlev.data_dir, r_lowlev.REVISION_FILE)
            outfile = OUTBASE.joinpath("Revision.txt")
            print(f"copying {revision_file} to {outfile}")
            shutil.copy(revision_file, outfile)

            # copy sqlite3 file
            db_file = r_lowlev.sqlite_database_file
            outfile = OUTBASE.joinpath(os.path.basename(db_file))
            print(f"copy {db_file} to {outfile}", db_file)
            shutil.copy(db_file, outfile)

            for var, finfo in all_files.items():
                print(var)
                for stat, files in finfo.items():
                    print(stat)
                    for file in files:
                        # print(file)
                        fp = src.joinpath(file)
                        dest = FILES_DEST.joinpath(file)
                        print(f"copying {fp} to {dest}")
                        shutil.copy(fp, dest)
                    print()

            for what, file in add_files.items():
                fp = src.joinpath(file)
                dest = FILES_DEST.joinpath(file)
                print(f"copying {fp} to {dest}")
                shutil.copy(fp, dest)

            print(f"re-writing {JSON_FILE}")
            with open(JSON_FILE, "w") as f:
                simplejson.dump(all_files, f, allow_nan=True)


if __name__ == "__main__":
    main()
