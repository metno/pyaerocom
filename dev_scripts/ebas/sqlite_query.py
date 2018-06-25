#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EBAS sqlite test
"""

import pyaerocom as pya
import sqlite3
import os

DIR = pya.const.OBSCONFIG["EBASMC"]["PATH"]

DB_FILE = 'ebas_file_index.sqlite3'

# HINT FROM J. GRIESFELLER

#"select distinct filename from variable join station on station.station_code=variable.station_code where comp_name in ('sulphate_corrected', "+"'sulphate_total') and matrix in ('aerosol','pm25')  and last_start >= '2008-01-01' and first_end < '2009-01-01' order by station.station_code;"
if __name__=="__main__":
    
    
    conn = sqlite3.connect(os.path.join(DIR, DB_FILE))
    
    cursor = conn.cursor()
    
    cursor
    
    
    
    
    