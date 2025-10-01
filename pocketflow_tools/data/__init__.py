"""Convenience accessors for packaged Agent OS + PocketFlow data.

This module centralises the resource lookups for assets bundled inside
``pocketflow_tools.data`` so the installer and other utilities can import
semantically named constants instead of hard-coding relative paths. Using
``importlib.resources`` keeps the implementation compatible with both
editable installs and zipped distributions.
"""

from __future__ import annotations

from contextlib import contextmanager
from importlib.resources import as_file, files
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Iterator


DATA_PACKAGE = __name__
"""Fully-qualified package name for the bundled data resources."""


def data_resource(*relative_parts: str) -> Traversable:
    """Return a traversable resource under ``pocketflow_tools.data``.

    Parameters
    ----------
    *relative_parts:
        Folder / file segments relative to the data package.
    """

    resource: Traversable = files(DATA_PACKAGE)
    for part in relative_parts:
        resource = resource.joinpath(part)
    return resource


def data_path(*relative_parts: str) -> Traversable:
    """Alias for :func:`data_resource` maintained for readability."""

    return data_resource(*relative_parts)


@contextmanager
def materialised_path(*relative_parts: str) -> Iterator[Path]:
    """Yield a filesystem path for the requested resource.

    ``importlib.resources`` keeps data abstracted behind a ``Traversable``.
    Some operations (e.g., copying tree structures) need a real ``Path``.
    ``as_file`` extracts the resource to a temporary location when the
    distribution is zip-based, guaranteeing callers always receive a usable
    path.
    """

    resource = data_resource(*relative_parts)
    with as_file(resource) as concrete_path:
        yield Path(concrete_path)


# Named resource helpers ---------------------------------------------------

DATA_ROOT = data_resource()
INSTRUCTIONS_DIR = data_resource("instructions")
STANDARDS_DIR = data_resource("standards")
TEMPLATES_DIR = data_resource("templates")
CLAUDE_CODE_DIR = data_resource("claude-code")
FRAMEWORK_TOOLS_DIR = data_resource("framework-tools")
SHARED_DIR = data_resource("shared")
SETUP_DIR = data_resource("setup")
SETUP_SCRIPT = data_resource("setup.sh")
CONFIG_FILE = data_resource("config.yml")


__all__ = [
    "CLAUDE_CODE_DIR",
    "CONFIG_FILE",
    "DATA_PACKAGE",
    "DATA_ROOT",
    "FRAMEWORK_TOOLS_DIR",
    "INSTRUCTIONS_DIR",
    "SHARED_DIR",
    "SETUP_DIR",
    "SETUP_SCRIPT",
    "STANDARDS_DIR",
    "TEMPLATES_DIR",
    "data_path",
    "data_resource",
    "materialised_path",
]
