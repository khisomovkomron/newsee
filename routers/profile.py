import sys

sys.path.append('..')

from .auth import get_current_user, get_user_exception
from fastapi import Depends, APIRouter
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session
from database_pack.getDB import get_db
from database_pack.schemas import Profile
from database_pack import models

from .auth import create_access_token

logger = fastapi_logs(router='PROFILE')

router = APIRouter(
    prefix='/profile',
    tags=['profile'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/info')
async def profile_info(user: dict = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users)\
        .filter(models.Users.id == user.get('id'))\
        .first()
    if not user_model:
        user_model = None
        
    address_model = db.query(models.Address)\
        .filter(models.Users.id == user.get('id'))\
        .all()
    if not address_model:
        address_model = None

    todo_model = db.query(models.Todo)\
        .filter(models.Users.id == user.get('id'))\
        .all()
    if not todo_model:
        todo_model = None
        
    archive_completed_model = db.query(models.Archive)\
        .filter(models.Archive.status == 'true')\
        .count()
    archive_deleted_model = db.query(models.Archive)\
        .filter(models.Archive.status == 'false')\
        .count()
    
    token = create_access_token(user.get('username'), user.get('id'))

    return {'User': {
                     'User': user_model,
                     'Token': token
                    },
            'Address': address_model,
            'Todo': todo_model,
            'Archive': {
                'completed_tasks': archive_completed_model,
                'deleted_tasks': archive_deleted_model
            }
            }

