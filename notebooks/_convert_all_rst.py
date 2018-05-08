#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used to convert all notebooks into restructured text
"""

#import nbformat
import nbconvert
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

if __name__=="__main__":
    files = sorted([p for p in os.listdir(".") if p.endswith("ipynb")])
    converter = nbconvert.RSTExporter()
    
    writer = nbconvert.writers.FilesWriter()
    writer.build_directory = "../docs/"

    for file in files:
        try:
            if int(os.path.basename(file)[:2]) > 0:
                resources = init_single_notebook_resources(file)
                (body, resources) = converter.from_file(file, resources=resources)
        
                writer.write(body, resources, os.path.splitext(file)[0])
        except:
            print("Ignoring {}".format(file))
    
    
    
    
    





