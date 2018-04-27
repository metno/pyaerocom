#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used to convert all notebooks into restructured text
"""

import nbformat
import nbconvert
import os


if __name__=="__main__":
    paths = sorted([p for p in os.listdir(".") if p.endswith("ipynb")])
    
    converter = nbconvert.RSTExporter()
    
    nb = nbformat.read(paths[0], 4)
    
    (body, resources) = converter.from_notebook_node(nb)
    
    
    
    
    
    





