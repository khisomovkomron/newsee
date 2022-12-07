from typing import Optional

from pydantic import BaseModel

from tortoise.contrib.pydantic import pydantic_model_creator
from .models import Users


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str] | None = None
    
    class Config:
        orm_mode = True
    

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str
    


user_create_pydantic = pydantic_model_creator(Users, name='create_user', exclude_readonly=True, exclude=('is_active',))
user_get_pydantic = pydantic_model_creator(Users, name='user')