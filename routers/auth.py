import sys
sys.path.append('..')

from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "wadwad12e231iurhn342iurn"
ALGORITHM = 'HS256'


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone_number: Optional[str]
    

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'users': 'Not authorized'}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

@router.post('/create/user')
async def create_new_user(create_user: CreateUser,
                          db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.phone_number = create_user.phone_number
    create_user_model.hashed_password = create_user.password
    
    create_user_model.is_active = True
    
    db.add(create_user_model)
    db.commit()
    
    return {'status': 'Successful'}
    