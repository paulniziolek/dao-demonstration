from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    uuid: UUID
    username: str
    created_at: datetime
