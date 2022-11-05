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
    
    
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

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
        

def get_hashed_password(password):
    """hashed proved password"""
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    """verifies user password by plain and hashed password"""
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    """returns users if username exists in db and users is verified via password"""
    user = db.query(models.Users).filter(models.Users.username == username).first()
    
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
    return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        
        if username is None or user_id is None:
            raise get_user_exception()
        return {'username': username, 'id': user_id}
    except JWTError:
        raise get_user_exception()


@router.post('/create/user')
async def create_new_user(create_user: CreateUser,
                          db: Session = Depends(get_db)):
    """Create new user: get user model from DB and pass all variables from CreateUser fields to db fields"""
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.phone_number = create_user.phone_number
    hashed_password = get_hashed_password(create_user.password)
    create_user_model.hashed_password = hashed_password
    
    create_user_model.is_active = True
    
    db.add(create_user_model)
    db.commit()
    
    return {'status': 'Successful'}
    

@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """Returns generated token if user authenticated:
     1. get user username and password
     2. authenticate user
     3. generate new token
     4. return token"""
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=15)
    
    token = create_access_token(user.username,
                                user.id,
                                expired_delta=token_expires)
    return {'token': token}
    
    
def get_user_exception():
    """ returns HTTP exception if users credentials are wrong"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Coul not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return credential_exception


def token_exception():
    """returns HTTP exception if provided token by user is invalid"""
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return token_exception


    