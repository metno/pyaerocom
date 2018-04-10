from os.path import join, exists
from os import mkdir

OUT_DIR = join(".", "out")
OUT_DIR_MAPS = join(".", "out", "maps")

if not exists(OUT_DIR):
    mkdir(OUT_DIR)

if not exists(OUT_DIR_MAPS):
    mkdir(OUT_DIR_MAPS)    
    
    


