import pytest
from unittest.mock import patch, MagicMock
from internal.database.database import ServiceDB

@pytest.fixture
def service_db():
    with patch('database.pymysql.connect') as mock_connect:
        mock_connect.return_value = MagicMock()
        yield ServiceDB()

def test_init(service_db):
    with patch('database.pymysql.connect') as mock_connect:
        ServiceDB()
        mock_connect.assert_called_once_with(
            host=None,
            port=0,
            user=None,
            password=None,
            database=None,
            autocommit=False,
        )

def test_get_cursor(service_db):
    cursor = service_db.get_cursor()
    assert isinstance(cursor, MagicMock)

def test_commit(service_db):
    service_db.commit()
    service_db.conn.commit.assert_called_once()

def test_rollback(service_db):
    service_db.rollback()
    service_db.conn.rollback.assert_called_once()

def test_close(service_db):
    service_db.close()
    service_db.conn.close.assert_called_once()