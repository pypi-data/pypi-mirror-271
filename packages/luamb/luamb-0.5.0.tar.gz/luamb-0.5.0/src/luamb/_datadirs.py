import os
import sys
from pathlib import Path

from ._exceptions import ImproperlyConfigured


__all__ = ['ENVS_DIR', 'HEREROCKS_DIR']


def _get_data_dir() -> Path:
    if dir_from_env := os.environ.get('LUAMB_HOME'):
        data_dir = Path(os.path.expandvars(os.path.expanduser(dir_from_env)))
    else:
        if sys.platform == 'darwin':
            data_root = os.path.expanduser('~/Library/Application Support')
        else:
            data_root = os.environ.get('XDG_DATA_HOME')
            if not data_root:
                data_root = os.path.expanduser('~/.local/share')
        data_dir = Path(data_root) / 'luamb'
    if data_dir.exists() and not data_dir.is_dir():
        raise ImproperlyConfigured(f'LUAMB_HOME={data_dir} is not a directory')
    return data_dir


_data_dir = _get_data_dir()


def _get_envs_dir() -> Path:
    if dir_from_env := os.environ.get('LUAMB_ENVS_DIR'):
        envs_dir = Path(os.path.expandvars(os.path.expanduser(dir_from_env)))
    else:
        envs_dir = _data_dir / 'envs'
    if envs_dir.exists() and not envs_dir.is_dir():
        raise ImproperlyConfigured(
            f'LUAMB_ENVS_DIR={envs_dir} is not a directory')
    return envs_dir


ENVS_DIR = _get_envs_dir()
HEREROCKS_DIR = _data_dir / 'hererocks'
