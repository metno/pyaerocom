from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from .models import ModelName


def find_model_path(model: str | ModelName, date: date | datetime) -> Path:
    raise NotImplementedError()
