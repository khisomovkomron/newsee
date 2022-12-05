import sys
sys.path.append('..')

from utils.auth_helpers import \
    get_hashed_password, \
    authenticate_user, \
    create_access_token, \
    get_current_user

from utils.todo_exceptions import \
    get_user_exception, \
    token_exception


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from logs.loguru import fastapi_logs

from database_pack.schemas import CreateUser
from database_pack.getDB import get_db
from database_pack import models

from datetime import timedelta

logger = fastapi_logs(router='AUTH')


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'users': 'Not authorized'}}
)


@router.post('/create/user')
async def create_new_user(create_user: CreateUser,
                          db: Session = Depends(get_db)):
    """Create new user: get user model from DB and pass all variables from CreateUser fields to db fields"""
    
    logger.info("CREATING NEW USER")

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


@router.get('/me')
async def token_get_current_user(user: dict = Depends(get_current_user),
                                 db: SessionLocal = Depends(get_db)):
    user_model = db.query(models.Users) \
        .filter(models.Users.id == user.get('id')) \
        .first()
    if not user_model:
        user_model = None
    return user_model


@router.post('/me')
async def form_get_current_user(form_data: OAuth2PasswordRequestForm = Depends(),
                                db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise get_user_exception()
    user_model = db.query(models.Users).filter(models.Users.id == user.id).first()
    token = create_access_token(form_data.username, user.id)

    return {'user': user_model,
            'token': token}
    

@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """Returns generated token if user authenticated:
     1. get user username and password
     2. authenticate user
     3. generate new token
     4. return token"""
    
    logger.info("CREATING NEW ACCESS TOKEN")

    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=15)
    
    token = create_access_token(user.username,
                                user.id,
                                expired_delta=token_expires)

    return {'token': token}


