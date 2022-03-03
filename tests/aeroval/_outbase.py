import os

from ..conftest import TMPDIR

AEROVAL_OUT = os.path.join(TMPDIR, "aeroval")
ADD_MODELS_DIR = os.path.join(TMPDIR, "modeldata")

os.makedirs(AEROVAL_OUT, exist_ok=True)
os.makedirs(ADD_MODELS_DIR, exist_ok=True)
