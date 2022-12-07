from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from database_pack import models, schemas
from utils import service
from utils.todo_exceptions import get_user_exception
from logs.loguru import fastapi_logs
from tortoise.expressions import Q
from config import settings

logger = fastapi_logs(router='AUTH')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token', description='Bearer Token')


async def registration(new_user: schemas.CreateUser, task: BackgroundTasks) -> bool:
    if models.Users.filter(Q(username=new_user.username) | Q(email=new_user.email)).exists():
        return True
    else:
        user = await service.user_s.create_user(new_user)
        verify = await models.Verification.create(user_id=user.id)
        task.add_task(user, verify)
        return False
    

def get_hashed_password(password):
    """hashed proved password"""
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    """verifies user password by plain and hashed password"""
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    """returns users if username exists in db and users is verified via password"""
    # user = db.query(models.Users).filter(models.Users.username == username).first()
    user = models.Users.get(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(username: str, user_id: int, expired_delta: Optional[timedelta] = None):
    """returns generated JWT TOKEN using username and user_id, JWT TOKENS is valid for default 15 mins"""
    encode = {'sub': username, 'id': user_id}
    if expired_delta:
        expire = datetime.utcnow() + expired_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})
    return jwt.encode(claims=encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    logger.info("GETTING CURRENT USER")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        
        if username is None or user_id is None:
            raise get_user_exception()
        return {'username': username, 'id': user_id}
    except JWTError:
        raise get_user_exception()
