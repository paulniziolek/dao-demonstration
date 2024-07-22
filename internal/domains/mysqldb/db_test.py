import os
import pytest
from unittest.mock import patch, MagicMock
from internal.domains.mysqldb.db import ServiceDB

class TestServiceDB:
    @pytest.fixture
    def set_env(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setenv('DB_HOST', 'localhost')
        monkeypatch.setenv('DB_PORT', '3306')
        monkeypatch.setenv('DB_USER', 'user')
        monkeypatch.setenv('DB_PASS', 'pass')
        monkeypatch.setenv('DB_NAME', 'testdb')

    @pytest.fixture
    @patch('internal.domains.mysqldb.db.pymysql.connect', return_value=MagicMock())
    def service_db(self, set_env):
        return ServiceDB()

    @patch('internal.domains.mysqldb.db.pymysql.connect', return_value=MagicMock())
    def test_init(self, mock_connect: MagicMock, set_env):
        _ = ServiceDB()

        mock_connect.assert_called_once_with(
            host='localhost',
            port=3306,
            user='user',
            password='pass',
            database='testdb',
            autocommit=False,
        )

    def test_get_cursor(self, service_db):
        cursor = service_db.get_cursor()
        assert isinstance(cursor, MagicMock)

    def test_commit(self, service_db):
        service_db.commit()
        service_db.conn.commit.assert_called_once()

    def test_rollback(self, service_db):
        service_db.rollback()
        service_db.conn.rollback.assert_called_once()

    def test_close(self, service_db):
        service_db.close()
        service_db.conn.close.assert_called_once()
