"""
Compatibility layer between importlib.resources for Python 3.11 and older versions
"""

import sys
from contextlib import AbstractContextManager
from pathlib import Path

if sys.version_info >= (3, 11):
    from importlib import resources
else:
    import importlib_resources as resources


def path(package: str, resource: str) -> AbstractContextManager[Path]:
    """A context manager providing a file path object to the resource.
    If the resource does not already exist on its own on the file system,
    e.g. it only exists in a zip-file, the resource will be extracted and
    a temporary file will be created. If the file was created, the file
    will be deleted upon exiting the context manager (no exception is
    raised if the file was deleted prior to the context manager
    exiting).
    """
    return resources.as_file(resources.files(package) / resource)


def is_resource(package: str, name: str) -> bool:
    """True if `name` is a resource inside `package`.

    Directories are *not* resources.
    """
    with path(package, name) as p:
        return p.exists()


def read_text(package: str, resource: str, encoding: str = "utf-8", errors: str = "strict") -> str:
    """Return the decoded string of the resource.

    The decoding-related arguments have the same semantics as those of `pathlib.Path.read_text`.
    """
    with path(package, resource) as p:
        return p.read_text(encoding, errors)
