#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used to convert all notebooks into restructured text
"""

#import nbformat
import argparse
import nbconvert, nbformat
from pyaerocom import const
from nbconvert.preprocessors import ExecutePreprocessor
import fnmatch
import shutil
import os

lustre_avail = const.has_access_lustre
user_server_avail = const.has_access_users_database

# Dictionary that specifies which notebooks (keys) are executed only if 
# a certain condition (value, True / False) is met
RUN_PREFIX = ['tut', 'add']
RUN_IF = {'add01_intro_time_handling.ipynb': lustre_avail,
          'add02_read_ebas_nasa_ames.ipynb': lustre_avail,
          'add03_ebas_database_browser.ipynb': lustre_avail,
          'add04_stationdata_merging.ipynb': lustre_avail,
          'tut001_setup_userserver.ipynb': user_server_avail,
          'tut00_get_started.ipynb': lustre_avail,
          'tut01_intro_regions.ipynb': lustre_avail,
          'tut02_intro_class_ReadGridded.ipynb': lustre_avail,
          'tut03_intro_class_ReadGriddedMulti.ipynb': lustre_avail,
          'tut04_intro_class_GriddedData.ipynb': lustre_avail,
          'tut05_intro_ungridded_reading.ipynb': lustre_avail,
          'tut06_intro_colocation.ipynb': lustre_avail}

def init_single_notebook_resources(notebook_filename):
    """Step 1: Initialize resources
    
    Note
    ----
    This method was copied and adapted from the nbconvert app main class 
    NbConvertApp in order to instantiate all output in subdirectories

    This initializes the resources dictionary for a single notebook.

    Returns
    -------

    dict
        resources dictionary for a single notebook that MUST include the following keys:
            - unique_key: the notebook name
            - output_files_dir: a directory where output files (not
              including the notebook itself) should be saved
    """
    basename = os.path.basename(notebook_filename)
    notebook_name = basename[:basename.rfind('.')]
    # first initialize the resources we want to use
    resources = {}
    
    resources['unique_key'] = notebook_name
    resources['output_files_dir'] = notebook_name

    return resources

def execute_and_save_notebook(file):
    try:
        print("Executing notebook: {}".format(file))
        with open(file) as f:
            nb = nbformat.read(f, as_version=4)
            
        ep = ExecutePreprocessor(kernel_name="python3")
        ep.timeout = 600
        ep.preprocess(nb, {'metadata': {'path': '.'}})
        
        
        with open(file, 'wt') as f:
            nbformat.write(nb, f)
        print("Success!")
        return True
    except Exception as e:
        print("Failed: {}".format(repr(e)))
        return False
    

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute_all', '-exec', type=bool, default=True,
                        help=("Boolean: execute all notebooks before conversion " 
                              "to rst format"))
    
    parser.add_argument('--convert_rst', '-conv', type=bool, default=False,
                        help=("Boolean: convert all notebooks to rst and save" 
                              "in docs folder"))
    
    parser.add_argument('--output_dir', default="../docs/", type=str,
                        help="Output directory for converted notebooks")
    
    parser.add_argument('--clear_old', '-cls', default=False, type=bool,
                        help=("Delete all existing converted notebooks "
                              "in output direcory (i.e. all files and folders "
                              "with trailing number)"))
    
    args = parser.parse_args()
    
    out_dir = args.output_dir
    
    if not os.path.exists(out_dir):
        raise IOError("Specified output directory {} does not exist".format(out_dir))
    
    files = []
    skipped = []
    patterns = []
    for prefix in RUN_PREFIX:
        pattern = "{}[0-9]*.ipynb".format(prefix)
        patterns.append(pattern)
        for f in sorted(fnmatch.filter(os.listdir("."), pattern)):
            if not f in RUN_IF:
                files.append(f)
            else:
                if RUN_IF[f]:
                    files.append(f)
                else:
                    skipped.append(f)
        
    success, failed = [], []
    conv_success, conv_fail = [], []
    if files:
        if args.clear_old:
            ### DELETE OLD NOTEBOOKS (if applicable)
            for pattern in patterns:
                matches = fnmatch.filter(os.listdir(out_dir), pattern)
            old = [os.path.join(out_dir, x) for x in matches]
            for item in old:
                try:
                    os.remove(item)
                except:
                    shutil.rmtree(item)
                print("Deleted: {}".format(item))
        
        ### RUN ALL NOTEBOOKS
        if args.execute_all:
            for f in files:    
                if execute_and_save_notebook(f):
                    success.append(f)
                else:
                    failed.append(f)
        
        if args.convert_rst:                
            converter = nbconvert.RSTExporter()
            
            writer = nbconvert.writers.FilesWriter()
            writer.build_directory = out_dir
            
            for file in success:
                name = os.path.basename(file)
                try:
                    resources = init_single_notebook_resources(file)
                    (body, resources) = converter.from_file(file, resources=resources)
            
                    writer.write(body, resources, os.path.splitext(file)[0])
                    conv_success.append(name)
                except Exception as e:
                    conv_fail.append(name)
                    print("Failed to convert {} (Error: {})".format(name, repr(e)))
         
    print('\n\n')
    print('\n--------------\nSKIPPED NOTEBOOK\n--------------\n')
    for f in skipped:
        print(f)
    print()
    
    print('\n--------------\nEXECUTION SUCCESSFUL\n--------------\n')
    for f in success:
        print(f)
    print()
    
    print('\n--------------\nEXECUTION FAILED\n--------------\n')
    for f in failed:
        print(f)
    print()
    if args.convert_rst:
        print('\n--------------\nCONVERSION RST SUCCESSFUL\n--------------\n')
        for f in conv_success:
            print(f)
        print()
        print('--------------\nCONVERSION RST FAILED\n--------------\n')
        for f in conv_fail:
            print(f)
        print()
        
        
        
        
        





