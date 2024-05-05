from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from luamb._hererocks import (
    UpdateFailed, _save_digest, _save_hererocks, import_hererocks,
    update_hererocks,
)


if TYPE_CHECKING:
    import pathlib


@pytest.fixture
def hererocks_dir(monkeypatch, tmp_path):
    dir = tmp_path / 'luamb' / 'hererocks'
    monkeypatch.setattr('luamb._hererocks.HEREROCKS_DIR', dir)
    return dir


class TestImportHererocks:

    @pytest.fixture(autouse=True)
    def setup(self, hererocks_dir: pathlib.Path):
        sys.modules.pop('hererocks', None)
        self.hererocks_dir = hererocks_dir

    def test_not_found(self):
        hererocks = import_hererocks()

        assert hererocks is None

    def test_ok(self):
        self.hererocks_dir.mkdir(parents=True)
        (self.hererocks_dir / 'hererocks.py').write_text('is_mock = True')

        hererocks = import_hererocks()

        assert hererocks.is_mock


class TestUpdateHererocks:
    content = b'is_mock = True'
    digest = '4eccc80b924079deca2a5f9a0d7ce1e4780ec36d62fec188dcc9ec5323338dd9'

    @pytest.fixture(autouse=True)
    def setup(
        self, hererocks_dir: pathlib.Path,
        save_digest_mock: Mock, save_hererocks_mock: Mock, response_mock: Mock,
    ):
        self.hererocks_dir = hererocks_dir
        self.hererocks_file = self.hererocks_dir / 'hererocks.py'
        self.digest_file = self.hererocks_dir / 'hererocks.py.sha256'
        self.save_hererocks_mock = save_hererocks_mock
        self.save_digest_mock = save_digest_mock

    @pytest.fixture
    def response_mock(self, monkeypatch):
        mock = Mock()
        mock.__enter__ = Mock(return_value=mock)
        mock.__exit__ = Mock()
        mock.read = Mock(return_value=self.content)
        monkeypatch.setattr(
            'luamb._hererocks.urlopen', Mock(return_value=mock))
        return mock

    @pytest.fixture
    def save_hererocks_mock(self, monkeypatch):
        mock = Mock(wraps=_save_hererocks)
        monkeypatch.setattr('luamb._hererocks._save_hererocks', mock)
        return mock

    @pytest.fixture
    def save_digest_mock(self, monkeypatch):
        mock = Mock(wraps=_save_digest)
        monkeypatch.setattr('luamb._hererocks._save_digest', mock)
        return mock

    def ensure_dir(self):
        self.hererocks_dir.mkdir(parents=True)

    def assert_content(self):
        assert self.hererocks_file.read_bytes() == self.content

    def assert_digest(self):
        assert self.digest_file.read_text() == self.digest

    def test_timeout(self, monkeypatch):
        monkeypatch.setattr('luamb._hererocks.urlopen', Mock(
            side_effect=TimeoutError('The read operation timed out')))

        with pytest.raises(UpdateFailed, match='timed out'):
            update_hererocks()

    def test_first_run(self):
        result = update_hererocks()

        assert result is True
        self.assert_content()
        self.assert_digest()
        self.save_hererocks_mock.assert_called_once()
        self.save_digest_mock.assert_called_once()

    def test_updated(self):
        self.ensure_dir()
        self.hererocks_file.write_text('old_mock = True')
        self.digest_file.write_text('deadf00d')

        result = update_hererocks()

        assert result is True
        self.assert_content()
        self.assert_digest()
        self.save_hererocks_mock.assert_called_once()
        self.save_digest_mock.assert_called_once()

    def test_not_updated_same_content(self):
        self.ensure_dir()
        self.hererocks_file.write_bytes(self.content)
        self.digest_file.write_text(self.digest)

        result = update_hererocks()

        assert result is False
        self.assert_content()
        self.assert_digest()
        self.save_hererocks_mock.assert_not_called()
        self.save_digest_mock.assert_not_called()
