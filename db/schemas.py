from typing import Optional

from pydantic import BaseModel

from tortoise.contrib.pydantic import pydantic_model_creator
from .models import Users


class UserBase(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


class CreateUser(UserBase):
    phone_number: Optional[str] | None = None
    
    class Config:
        orm_mode = True
        
        
class UserPublic(UserBase):
    id: int
    
    class Config:
        orm_mode = True


user_create_pydantic = pydantic_model_creator(Users)
user_get_pydantic = pydantic_model_creator(Users, name='user')
