import sys

from database_pack.schemas import UserVerification

sys.path.append('..')

from .auth import get_current_user, get_user_exception, verify_password, get_hashed_password
from database_pack.database import SessionLocal, engine
from database_pack.getDB import get_db
from database_pack import models
from fastapi import APIRouter, Depends
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session

logger = fastapi_logs(router='USERS')

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}}
)

models.Base.metadata.create_all(bind=engine)


@router.get('/')
async def read_all(db: SessionLocal = Depends(get_db)):
    logger.info("READING ALL USERS")

    return db.query(models.Users).all()


@router.get('/user/{user_id}')
async def user_by_path(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    logger.info("READING USER BY BY PATH")

    if user_model is not None:
        return user_model
    return 'Invalid used_id'


@router.get('/user/')
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    
    logger.info("READING USER BY ID BY QUERY")

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
    
    logger.info("CHANGING USER PASSWORD")

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
    logger.info("DELETE USER BY ID")

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
    logger.info("DELETE AUTHENTICATED USER")

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
    