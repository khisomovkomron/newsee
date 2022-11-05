import sys
sys.path.append('..')

from pydantic import BaseModel
from typing import Optional
import models
from database import SessionLocal, Base, engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception, verify_password, get_hashed_password


router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get('/')
async def read_all(db: SessionLocal = Depends(get_db)):
    return db.query(models.Users).all()


@router.get('/user/{user_id}')
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    if user_model is not None:
        return user_model
    return 'Invalid used_id'


@router.get('/user/')
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.put('/user/password')
async def user_password_change(user_verification: UserVerification,
                               user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    """Change password authenticated"""
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    
    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(
                user_verification.password,
                user_model.hashed_password):
            user_model.hashed_password = get_hashed_password(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return {'status': 'Successful',
                    'detail': 'Your password was successfully changed'}
    return {'status': 'Failed',
            'detail': 'Invalid request'}


@router.delete('/user/{user_id}')
async def delete_user_by_id(user_id: int,
                            db: Session = Depends(get_db)):
    """Delete user by id unauthenticated"""
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    if user_model is None:
        return {'status': 'Failed',
                'detail': 'Invalid request'}
    
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    
    db.commit()
    
    return {'status': 'Successful',
            'detail': f"User {user_id} was successfully deleted without authentication"}


@router.delete('/user')
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """Delete user authenticated"""
    if user is None:
        return get_user_exception()
    
    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    
    if user_model is None:
        return {'status': 'Failed',
                'detail': 'Invalid request'}
    
    db.query(models.Users).filter(models.Users.id == user.get('id')).delete()
    
    db.commit()

    return {'status': 'Successful',
            'detail': f"User {user.get('id')} was successfully deleted"}
    