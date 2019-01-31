#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used to convert all notebooks into restructured text
"""

#import nbformat
import argparse
import nbconvert, nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import fnmatch
import shutil
import os

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
        ep.timeout = 240
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
    
    parser.add_argument('--output_dir', default="../docs/", type=str,
                        help="Output directory for converted notebooks")
    
    parser.add_argument('--clear_old', '-cls', default=True, type=bool,
                        help=("Delete all existing converted notebooks "
                              "in output direcory (i.e. all files and folders "
                              "with trailing number)"))
    
    args = parser.parse_args()
    
    out_dir = args.output_dir
    
    if not os.path.exists(out_dir):
        raise IOError("Specified output directory {} does not exist".format(out_dir))
    
    if args.clear_old:
        matches = fnmatch.filter(os.listdir(out_dir), "tut[0-9][0-9]*")
        old = [os.path.join(out_dir, x) for x in matches]
        for item in old:
            try:
                os.remove(item)
            except:
                shutil.rmtree(item)
            print("Deleted: {}".format(item))
    
    
    files = sorted(fnmatch.filter(os.listdir("."), "tut[0-9][0-9]*.ipynb"))

    add_files = sorted(fnmatch.filter(os.listdir("."), "add[0-9][0-9]*.ipynb"))
    files.extend(add_files)

    if args.execute_all:
        for f in files:    
            execute_and_save_notebook(f)
                
    converter = nbconvert.RSTExporter()
    
    writer = nbconvert.writers.FilesWriter()
    writer.build_directory = out_dir
    
    for file in files:
        name = os.path.basename(file)
        try:
            resources = init_single_notebook_resources(file)
            (body, resources) = converter.from_file(file, resources=resources)
    
            writer.write(body, resources, os.path.splitext(file)[0])
            print("Converted notebook {}".format(name))
        except Exception as e:
            print("Failed to convert {} (Error: {})".format(name, repr(e)))
    
    
    
    
    





