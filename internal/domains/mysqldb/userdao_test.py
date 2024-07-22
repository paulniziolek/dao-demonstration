import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from datetime import datetime
from internal.domains.mysqldb.db import ServiceDB
from internal.models.user import User
from internal.domains.mysqldb.userdao import UserDAO  # Update with the correct import path

class TestUserDAO:
    @pytest.fixture(autouse=True)
    def setup(self):
        with patch('internal.domains.mysqldb.db.ServiceDB') as MockServiceDB:
            self.mock_servicedb = MockServiceDB.return_value
            self.mock_cursor = self.mock_servicedb.get_cursor.return_value
            self.user_dao = UserDAO(self.mock_servicedb)
            yield

    def test_get_user_by_id(self):
        user_id = uuid4()
        expected_user = {
            'uuid': user_id,
            'username': 'testuser',
            'created_at': datetime.now()
        }
        self.mock_cursor.fetchone.return_value = expected_user

        user = self.user_dao.get_user_by_id(user_id)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE uuid = %s", (user_id,))
        assert user == User(**expected_user)

    def test_get_user_by_username(self):
        username = 'testuser'
        expected_user = {
            'uuid': uuid4(),
            'username': username,
            'created_at': datetime.now()
        }
        self.mock_cursor.fetchone.return_value = expected_user

        user = self.user_dao.get_user_by_username(username)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", (username,))
        assert user == User(**expected_user)

    def test_create_user(self):
        username = 'newuser'
        created_user = {
            'uuid': uuid4(),
            'username': username,
            'created_at': datetime.now()
        }
        self.mock_cursor.fetchone.return_value = created_user

        user = self.user_dao.create_user(username)

        self.mock_cursor.execute.assert_any_call("INSERT INTO users (username) VALUES (%s)", (username,))
        self.mock_servicedb.commit.assert_called_once()
        assert user == User(**created_user)

    def test_update_user(self):
        user_id = uuid4()
        new_username = 'updateduser'
        updated_user = {
            'uuid': user_id,
            'username': new_username,
            'created_at': datetime.now()
        }
        self.mock_cursor.fetchone.return_value = updated_user

        user = self.user_dao.update_user(user_id, new_username)

        self.mock_cursor.execute.assert_any_call("UPDATE users SET username = %s WHERE uuid = %s", (new_username, user_id))
        self.mock_servicedb.commit.assert_called_once()
        assert user == User(**updated_user)

    def test_delete_user(self):
        user_id = uuid4()
        self.mock_cursor.rowcount = 1

        result = self.user_dao.delete_user(user_id)

        self.mock_cursor.execute.assert_called_once_with("DELETE FROM users WHERE uuid = %s", (user_id,))
        self.mock_servicedb.commit.assert_called_once()
        assert result

    def test_get_user_by_id_not_found(self):
        user_id = uuid4()
        self.mock_cursor.fetchone.return_value = None

        user = self.user_dao.get_user_by_id(user_id)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE uuid = %s", (user_id,))
        assert user is None

    def test_get_user_by_username_not_found(self):
        username = 'nonexistentuser'
        self.mock_cursor.fetchone.return_value = None

        user = self.user_dao.get_user_by_username(username)

        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE username = %s", (username,))
        assert user is None
