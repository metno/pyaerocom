from os.path import join, exists
from os import mkdir

OUT_DIR = join(".", "out")

if not exists(OUT_DIR):
    mkdir(OUT_DIR)

