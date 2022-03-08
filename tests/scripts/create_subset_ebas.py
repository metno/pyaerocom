#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pyaerocom as pya
from pathlib import Path
import shutil
import pyaerocom.testdata_access as td
from getpass import getuser

if getuser() == 'jonasg':
    ebas_local = os.path.join(pya.const.OUTPUTDIR, 'data/obsdata/EBASMultiColumn/data')
    assert os.path.exists(ebas_local)
else:
    ebas_local=None

tda = td.TestDataAccess()

TESTDATADIR = tda.testdatadir

OUTBASE = Path(TESTDATADIR).joinpath('obsdata/EBASMultiColumn')

FILES_DEST = OUTBASE.joinpath('data')

UPDATE = True
UPDATE_EXISTING = False
DEV = False
NAME = 'EBASMC'

if ebas_local is not None:
    FILES_SRC = ebas_local
else:
    FILES_SRC = ebas_local

# ------------------------------------------------------------
# ADDITIONAL STUFF TO V0 pyaerocom >= 0.11.0dev1
# ------------------------------------------------------------
add_files = {
    # conco3 tower - 3 different measurement heights
    'o3_tower':'CZ0003R.20150101000000.20181107114213.uv_abs.ozone.air.1y.1h..CZ06L_uv_abs.lev2.nas',
    # conco3 Neg. meas periods
    'o3_neg_dt':'NZ0003G.20090110030000.20181130115605.uv_abs.ozone.air.9h.1h.US06L_Thermo_49C_LAU.US06L_AM.lev2.nas',
    # conco3 - Most common meas period is 150s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    'o3_tstype':'LT0015R.20080101000000.20081231000000.uv_abs.ozone.air.15d.1h.LT01L_uv_abs_15.LT01L_uv_abs..nas',
    # concpm10 - could not resolve unique data column for concpm10 (EBAS varname: ['pm10_mass'])
    'pm10_colsel':'ID1013R.20180101000000.20200102000000.beta_gauge_particulate_sampler.pm10_mass.pm10.1y.1h.ID01L_MetOne_BAM1020..lev2.nas',
    # concpm10 Aliartos - Most common meas period is 172800s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    'pm10_tstype':'GR0001R.20060119000000.20080120000000.b-attenuation.pm10_mass.pm10.11mo.1w.GR01L_b_att_01.GR01L_b-attenuation..nas'
    }

def check_outdated(filedir):
    all_files = os.listdir(filedir)

    ok = True
    files_invalid = []
    files_valid = []

    import simplejson
    with open('ebas_files.json', 'r') as f:

        data = simplejson.load(f)

    for var, stats in data.items():
        for stat, files in stats.items():
            for file in files:
                if not file in all_files:
                    print('OUTDATED', var, stat)
                    print(file)
                    files_invalid.append(file)
                    ok=False
                else:
                    files_valid.append(file)


    for key, file in add_files.items():
        if not file in all_files:
            print('OUTDATED (add_files)', key)
            print(file)
            files_invalid.append(file)
            ok=False
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
                if ';' in fname:
                    raise ValueError('FATAL', var, stat)
                files[sd.station_name] = [sd.filename]
                break

        if not overlap_found:
            for left,right in zip(meta_match[:-1], meta_match[1:]):
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
                if ';' in fname:
                    raise ValueError('FATAL', var, stat)
                files[sd.station_name] = [sd.filename]
                numfound += 1
                break
    return files

if __name__ == '__main__':

    reader = pya.io.ReadUngridded(NAME, data_dir=ebas_local)
    r_lowlev = reader.get_reader()
    r_lowlev._dataset_path = ebas_local

    # directory containing NASA Ames files
    FILEDIR_SRC = r_lowlev.file_dir
    CURRENT_OK, files_valid, files_invalid = check_outdated(FILEDIR_SRC)

    if not CURRENT_OK:
        print('---------------------WARNING------------------------------')
        print('Some files in current EBAS subset do not exist anymore in '
              'the most recent EBAS database, consider updating them')
        print('---------------------WARNING------------------------------')
        raise Exception

    if not OUTBASE.exists():
        OUTBASE.mkdir()

    if not FILES_DEST.exists():
        FILES_DEST.mkdir()

    if DEV: # use this block to find interesting files, e.g. that throw certain exceptions
        var = 'concpm10'
        f0=1100
        f1=f0+1000

        reader = pya.io.ReadEbas(data_dir=ebas_local)
        reader.read(var ,first_file=f0, last_file=f1)
        for i, file in enumerate(reader.files_failed):
            try:
                data = reader.read_file(file, var)
            except Exception as e:
                print(i)
                print(os.path.basename(file))
                print(e)
                try:
                    fd=pya.io.EbasNasaAmesFile(file)
                    print(fd.station_name)
                except Exception as e:
                    print(e)

    else:
        import simplejson
        infofile = 'ebas_files.json'
        if os.path.exists(infofile):
            with open(infofile, 'r') as f:
                current_files = simplejson.load(f)
        else:
            current_files = {}

        VARS_STATFIX =  ['sc550dryaer', 'ac550aer',
                         'conco3','concpm10']
        VARS_STATVAR_NUM = 2
        VARS_STATVAR = ['concno2', 'vmrno2', 'vmro3', 'concpm25']

        STATSFIX = ['Jungfraujoch', 'Birkenes II', '*Kosetice*', 'Troll']

        all_files = {}
        overlap_found = False
        for var in VARS_STATFIX + VARS_STATVAR:
            if var in current_files and not UPDATE_EXISTING:
                all_files[var] = current_files[var]
                continue
            print(var)
            ropts = {}
            if var.startswith('conc') or var.startswith('vmr'):
                ropts['try_convert_vmr_conc'] = False
            data = reader.read(NAME, var, **ropts)
            if var in VARS_STATFIX:
                files, overlap_found = get_files_var_statlist(
                    data, var, STATSFIX, overlap_found)
            else:
                files = get_files_var_statnum(data, var,
                                              VARS_STATVAR_NUM)
            all_files[var] = files

        if not UPDATE:
            print('NOTHING WILL BE COPIED TO TEST DATA')
        else:

            src = Path(FILES_SRC).joinpath('data')

            # copy revision file
            revision_file = os.path.join(r_lowlev.DATASET_PATH,
                                         r_lowlev.REVISION_FILE)
            shutil.copy(revision_file, OUTBASE.joinpath('Revision.txt'))

            # copy sqlite3 file
            db_file = r_lowlev.sqlite_database_file
            print('copy', db_file)
            shutil.copy(db_file, OUTBASE.joinpath(os.path.basename(db_file)))

            for var, finfo in all_files.items():
                print(var)
                for stat, files in finfo.items():
                    print(stat)
                    for file in files:
                        print(file)
                        fp = src.joinpath(file)
                        dest = FILES_DEST.joinpath(file)
                        shutil.copy(fp, dest)
                    print()

            for what, file in add_files.items():
                fp = src.joinpath(file)
                dest = FILES_DEST.joinpath(file)
                shutil.copy(fp, dest)

            import simplejson
            with open('ebas_files.json', 'w') as f:

                simplejson.dump(all_files,f)


