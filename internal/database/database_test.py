import pytest
from unittest.mock import patch, MagicMock
from database import ServiceDB
from pymysql.cursors import DictCursor
# check out monkey mock

@patch('pymysql.connect')
def test_get_cursor(mock_connect):
    # Setup: Create a mock connection object
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    service_db = ServiceDB()

    # Exercise: Call get_cursor
    cursor = service_db.get_cursor()

    # Verify: Ensure cursor is obtained from the mock connection
    mock_conn.cursor.assert_called_once_with(DictCursor)
    assert cursor == mock_conn.cursor.return_value

@patch('pymysql.connect')
def test_commit(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    service_db = ServiceDB()

    # Exercise
    service_db.commit()

    # Verify
    mock_conn.commit.assert_called_once()

@patch('pymysql.connect')
def test_rollback(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    service_db = ServiceDB()

    # Exercise
    service_db.rollback()

    # Verify
    mock_conn.rollback.assert_called_once()

@patch('pymysql.connect')
def test_close(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    service_db = ServiceDB()

    # Exercise
    service_db.close()

    # Verify
    mock_conn.close.assert_called_once()