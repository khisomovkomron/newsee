import sys
sys.path.append('..')

from fastapi import APIRouter, Depends
import models
from database import engine, SessionLocal


router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {'response': 'Not found'}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def read_all_todos():
    return {'response': 'successful'}