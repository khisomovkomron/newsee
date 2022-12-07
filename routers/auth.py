import sys
sys.path.append('..')

from utils.auth_helpers import \
    create_access_token, \
    registration

from utils.todo_exceptions import \
    get_user_exception, \
    user_exception


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, BackgroundTasks
from logs.loguru import fastapi_logs

from database_pack.schemas import CreateUser
from utils.auth_helpers import authenticate_user

logger = fastapi_logs(router='AUTH')


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'users': 'Not authorized'}}
)


@router.post('/create/user')
async def create_new_user(create_user: CreateUser, task: BackgroundTasks):
    """Create new user: get user model from DB and pass all variables from CreateUser fields to db fields"""
    
    user = await registration(create_user, task)
    if not user:
        raise user_exception()
    return {"msg": "User created"}
    
    
@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise get_user_exception()
    return create_access_token(form_data.username, user.id)


