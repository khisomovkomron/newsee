from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from tortoise.contrib.pydantic import pydantic_model_creator
from .models import Users


class UserBase(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str | None = None
    phone_number: Optional[int] | None = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = datetime

    class Config:
        orm_mode = True
    

class CreateUser(UserBase):
    password: str
    
    class Config:
        orm_mode = True
        
        
class UserPublic(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str | None = None
    phone_number: Optional[int] | None = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = datetime
    id: int
    
    class Config:
        orm_mode = True


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


user_create_pydantic = pydantic_model_creator(Users)
user_get_pydantic = pydantic_model_creator(Users, name='user')
