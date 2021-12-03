from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .models import ModelName

DATA_FOLDER_PATH = Path("/home/kristersk/lustre/storeB/project/fou/kl/CAMS2_83/test_data")

def find_model_path(model: str | ModelName, date: str | date | datetime) -> Path:
    if not isinstance(model, ModelName):
        model = ModelName[model]
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y%m%d")
    return DATA_FOLDER_PATH / f"{date:%Y-%m-%d}-{model}-all-species.nc"