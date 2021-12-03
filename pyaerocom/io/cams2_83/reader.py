from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .models import ModelName

DATA_FOLDER_PATH = Path("/home/kristersk/lustre/storeB/project/fou/kl/CAMS2_83/test_data")

def find_model_path(model: str | ModelName, date: date | datetime) -> Path:
    return DATA_FOLDER_PATH / f"{date:%F}-{model}-all-species.nc"