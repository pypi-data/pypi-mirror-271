from __future__ import annotations

import hashlib
import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.request import urlopen

from ._datadirs import HEREROCKS_DIR
from ._exceptions import LuambException


if TYPE_CHECKING:
    from types import ModuleType


__all__ = ['import_hererocks', 'update_hererocks', 'UpdateFailed']


_HEREROCKS_URL = (
    'https://raw.githubusercontent.com/luarocks/hererocks/master/hererocks.py')
_HTTP_TIMEOUT = 30
_HASH_ALGO = 'sha256'


class UpdateFailed(LuambException):
    pass


def import_hererocks() -> ModuleType | None:
    sys.path.insert(0, str(HEREROCKS_DIR))
    try:
        hererocks = importlib.import_module('hererocks')
    except ImportError:
        return None
    finally:
        sys.path.pop(0)
    # is_relative_to available since Python 3.9
    try:
        Path(hererocks.__file__).relative_to(HEREROCKS_DIR)
    except ValueError:
        # not managed by us (e.g., pip-installed), ignore it
        del sys.modules['hererocks']
        return None
    return hererocks


def _load_digest() -> str | None:
    try:
        with open(HEREROCKS_DIR / f'hererocks.py.{_HASH_ALGO}') as fobj:
            return fobj.read().strip()
    except FileNotFoundError:
        return None


def _save_digest(digest: str) -> None:
    with open(HEREROCKS_DIR / f'hererocks.py.{_HASH_ALGO}', 'w') as fobj:
        fobj.write(digest)


def _calculate_digest(content: bytes) -> str:
    hash = hashlib.new(_HASH_ALGO)
    hash.update(content)
    return hash.hexdigest()


def _fetch_hererocks() -> bytes:
    with urlopen(_HEREROCKS_URL, timeout=_HTTP_TIMEOUT) as response:
        return response.read()


def _save_hererocks(content: bytes) -> None:
    with open(HEREROCKS_DIR / 'hererocks.py', 'wb') as fobj:
        fobj.write(content)


def update_hererocks() -> bool:
    HEREROCKS_DIR.mkdir(parents=True, exist_ok=True)
    stored_digest = _load_digest()
    try:
        hererocks_content = _fetch_hererocks()
    except OSError as exc:
        raise UpdateFailed(f'update failed: {exc}')
    digest = _calculate_digest(hererocks_content)
    if digest == stored_digest:
        return False
    _save_digest(digest)
    _save_hererocks(hererocks_content)
    return True
