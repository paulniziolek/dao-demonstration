import pytest
from uuid import uuid4, UUID
from internal.database.userdao import UserDAO
from internal.database.database import ServiceDB
from internal.models.user import User

@pytest.fixture
def mock_db(mocker):
    return mocker.Mock(spec=ServiceDB)

@pytest.fixture
def user_dao(mock_db):
    return UserDAO(connection=mock_db)

@pytest.fixture
def user_id():
    return uuid4()

@pytest.fixture
def user_data(user_id):
    return {
        'uuid': user_id,
        'username': 'testuser'
    }

def test_get_user_by_id_found(user_dao: UserDAO, mock_db: ServiceDB, user_id: UUID, user_data):
    mock_db.get_cursor().fetchone.return_value = user_data
    user = user_dao.get_user_by_id(user_id)
    assert user is not None
    assert user.uuid == user_id
    assert user.username == 'testuser'

def test_get_user_by_id_not_found(user_dao, mock_db, user_id):
    mock_db.get_cursor().fetchone.return_value = None
    user = user_dao.get_user_by_id(user_id)
    assert user is None

def test_create_user_success(user_dao, mock_db, user_data):
    mock_db.get_cursor().fetchone.return_value = user_data
    user = user_dao.create_user('testuser')
    assert user is not None
    assert user.username == 'testuser'

def test_delete_user_success(user_dao, mock_db, user_id):
    mock_db.get_cursor().rowcount = 1  # Simulate one row affected
    result = user_dao.delete_user(user_id)
    assert result is True

def test_delete_user_failure(user_dao, mock_db, user_id):
    mock_db.get_cursor().rowcount = 0  # Simulate no rows affected
    result = user_dao.delete_user(user_id)
    assert result is False
