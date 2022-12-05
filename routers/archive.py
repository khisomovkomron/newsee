import sys
sys.path.append('..')

from fastapi import Depends, APIRouter
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session

from database_pack.getDB import get_db
from database_pack import models

logger = fastapi_logs(router='ARCHIVE')

router = APIRouter(
    prefix='/archive',
    tags=['archive'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/')
async def read_archive(db: Session = Depends(get_db)):
    return db.query(models.Archive).all()


@router.get('/deleted')
async def archive_deleted_tasks(db: Session = Depends(get_db)):
    return db.query(models.Archive).filter(models.Archive.status == 'false').all()


@router.get('/completed')
async def archive_completed_tasks(db: Session = Depends(get_db)):
    return db.query(models.Archive).filter(models.Archive.status == 'true').all()


@router.delete('/archive/clean')
async def delete_archive():
    pass