from fastapi import FastAPI, Depends
from internal.models.user import UserCreate, User
from internal.database.userdao import UserDAO
from internal.database.database import ServiceDB
from internal.handlers.user.user_handler import UserHandler

app = FastAPI()
db = ServiceDB

def get_user_dao(db: ServiceDB = Depends(db)):
    return UserDAO(connection=db)

def get_user_handler(dao: UserDAO = Depends(get_user_dao)):
    return UserHandler(user_dao=dao)

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, handler: UserHandler = Depends(get_user_handler)):
    created_user = await handler.create_user(user)
    return created_user

