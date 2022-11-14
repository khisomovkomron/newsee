import sys
sys.path.append('..')

from .auth import get_current_user, get_user_exception
from .todo import successful_response, http_exception
from fastapi import Depends, APIRouter
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session
from database import SessionLocal
from pydantic import BaseModel
import models

logger = fastapi_logs(router='ARCHIVE')

router = APIRouter(
    prefix='/archive',
    tags=['archive'],
    responses={404: {'description': 'Not found'}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    except:
        db.close()
        

class Archive(BaseModel):
    title: str
    status: bool
    

@router.get('/archive')
async def read_archive(db: Session = Depends(get_db)):
    return db.query(models.Archive).all()


@router.delete('/archive/clean')
async def delete_archive():
    pass