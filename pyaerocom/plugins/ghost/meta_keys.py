from __future__ import annotations

import sys

from pyaerocom.data import resources

if sys.version_info >= (3, 11):  # pragma: no cover
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

_META_KEYS = "meta_keys.toml"


def ghost_meta_keys() -> list[str]:
    assert resources.is_resource(__package__, _META_KEYS), f"{_META_KEYS} missing in {__package__}"
    variables = tomllib.loads(resources.read_text(__package__, _META_KEYS))
    return variables["ghost_meta_keys"]
