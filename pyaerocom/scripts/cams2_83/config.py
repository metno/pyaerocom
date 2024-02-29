from __future__ import annotations

import json
from importlib import resources


def read_config(config: str) -> dict:
    assert resources.is_resource(__package__, config), f"missing {__package__} resource"
    with resources.path(__package__, config) as path:
        return json.loads(path.read_text())


CFG = read_config("config.json")
species_list: list[str] = CFG["obs_cfg"]["EEA"]["obs_vars"]
