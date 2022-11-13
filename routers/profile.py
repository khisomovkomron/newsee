import sys
sys.path.append('..')

from .auth import get_current_user, get_user_exception
from .todo import successful_response, http_exception
from fastapi import Depends, APIRouter
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
from typing import Optional
import models

from .auth import CreateUser, create_access_token
from .address import Address
from .todo import Todo

logger = fastapi_logs(router='PROFILE')

router = APIRouter(
    prefix='/profile',
    tags=['profile'],
    responses={404: {'description': 'Not found'}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Profile(BaseModel):
    user: CreateUser
    address: Address
    todo: Todo
    
    
@router.get('/info')
async def profile_info(user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    address_model = db.query(models.Address).filter(models.Users.id == user.get('id')).all()
    todo_model = db.query(models.Todo).filter(models.Users.id == user.get('id')).all()
    
    token = create_access_token(user.get('username'), user.get('id'))

    return {'User': {
                     'User': user_model,
                     'Token': token
                    },
            'Address': address_model,
            'Todo': todo_model
            }

