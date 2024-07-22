from fastapi import HTTPException
from internal.domains.mysqldb.userdao import UserDAO
from internal.models.user import User, UserCreate
from pymysql.err import IntegrityError

class UserHandler:
    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    async def create_user(self, user: UserCreate) -> User | None:
        try:
            created_user = self.user_dao.create_user(user.username)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User already exists.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while creating the user: {e}")

        return created_user
    
    
