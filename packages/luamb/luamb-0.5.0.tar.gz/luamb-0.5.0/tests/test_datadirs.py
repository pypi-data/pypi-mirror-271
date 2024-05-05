import sys
from pathlib import Path

import pytest

from luamb._datadirs import _get_data_dir, _get_envs_dir
from luamb._exceptions import ImproperlyConfigured


class BaseTestGetDataDir:

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        monkeypatch.delenv('LUAMB_HOME', raising=False)

    def test_env_var_does_not_exist(self, monkeypatch):
        monkeypatch.setenv('SOME_DIR', 'somedir')
        monkeypatch.setenv('LUAMB_HOME', '~/$SOME_DIR/luambhome')

        data_dir = _get_data_dir()

        assert data_dir == Path().home() / 'somedir/luambhome'

    def test_env_var_exists(self, monkeypatch, tmp_path):
        dir = tmp_path / 'luambhome'
        dir.mkdir()
        monkeypatch.setenv('LUAMB_HOME', str(dir))

        data_dir = _get_data_dir()

        assert data_dir == dir

    def test_env_var_is_file(self, monkeypatch, tmp_path):
        file = tmp_path / 'luambhome'
        file.touch()
        monkeypatch.setenv('LUAMB_HOME', str(file))

        with pytest.raises(ImproperlyConfigured, match='not a directory'):
            _get_data_dir()


@pytest.mark.skipif(sys.platform != 'linux', reason='requires linux')
class TestGetDataDirLinux(BaseTestGetDataDir):

    def test_default(self, monkeypatch):
        monkeypatch.delenv('XDG_DATA_HOME', raising=False)

        data_dir = _get_data_dir()

        assert data_dir == Path().home() / '.local/share/luamb'

    def test_xdg(self, monkeypatch):
        monkeypatch.setenv('XDG_DATA_HOME', '/xdg/data')

        data_dir = _get_data_dir()

        assert data_dir == Path('/xdg/data/luamb')


@pytest.mark.skipif(sys.platform != 'darwin', reason='requires macOS')
class TestGetDataDirMacOS(BaseTestGetDataDir):

    def test_default(self):
        data_dir = _get_data_dir()

        assert data_dir == Path().home() / 'Library/Application Support/luamb'


class TestGetEnvsDir:

    def setup(self, monkeypatch):
        monkeypatch.delenv('LUAMB_ENVS_DIR', raising=False)

    def test_default(self, monkeypatch):
        monkeypatch.setattr('luamb._datadirs._data_dir', Path('/data/dir'))

        envs_dir = _get_envs_dir()

        assert envs_dir == Path('/data/dir/envs')

    def test_env_var_does_not_exist(self, monkeypatch):
        monkeypatch.setenv('DATA_DIR', 'datadir')
        monkeypatch.setenv('LUAMB_ENVS_DIR', '~/$DATA_DIR/myenvs')

        envs_dir = _get_envs_dir()

        assert envs_dir == Path().home() / 'datadir/myenvs'

    def test_env_var_exists(self, monkeypatch, tmp_path):
        dir = tmp_path / 'envs'
        dir.mkdir()
        monkeypatch.setenv('LUAMB_ENVS_DIR', str(dir))

        envs_dir = _get_envs_dir()

        assert envs_dir == dir

    def test_env_var_is_file(self, monkeypatch, tmp_path):
        file = tmp_path / 'envs'
        file.touch()
        monkeypatch.setenv('LUAMB_ENVS_DIR', str(file))

        with pytest.raises(ImproperlyConfigured, match='not a directory'):
            _get_envs_dir()
