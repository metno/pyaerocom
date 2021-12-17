from pathlib import Path

TMPDIR = Path("~/tmp/pyatest").expanduser()
AEROVAL_OUT = TMPDIR / "aeroval"
ADD_MODELS_DIR = TMPDIR / "modeldata"

TMPDIR.mkdir(exist_ok=True)
AEROVAL_OUT.mkdir(exist_ok=True)
ADD_MODELS_DIR.mkdir(exist_ok=True)
