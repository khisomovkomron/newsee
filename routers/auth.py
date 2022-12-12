import sys
sys.path.append('..')

from utils.auth_helpers import \
    create_access_token

from utils.todo_exceptions import \
    get_user_exception, \
    user_exception


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter
from logs.loguru import fastapi_logs

from db.schemas import CreateUser
from db import models, schemas
from db.schemas import user_get_pydantic
from utils.auth_helpers import authenticate_user
from tortoise.expressions import Q
from utils.auth_helpers import get_hashed_password
logger = fastapi_logs(router='AUTH')


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'users': 'Not authorized'}}
)
# User_Pydantic = pydantic_model_creator(models.Users)


@router.post('/create')
async def create_new_user(create_user: CreateUser):
    """Create new user: get user model from DB and pass all variables from CreateUser fields to db fields"""
    
    if not models.Users.filter(Q(username=create_user.username)).exists():
        return user_exception()
    hash_password = get_hashed_password(create_user.dict().pop("password"))
    users = await models.Users.create(**create_user.dict(exclude={"password"}), hashed_password=hash_password)
    user = await schemas.user_create_pydantic.from_tortoise_orm(users)

    if not user:
        return False
    return {"msg": "User created"}
    
    
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise get_user_exception()
    
    return {"id": user.id,
            "username": user.username,
            "token": create_access_token(form_data.username, user.id)}



