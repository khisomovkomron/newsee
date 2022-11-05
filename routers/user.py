import sys
sys.path.append('..')

from pydantic import BaseModel
from typing import Optional
import models
from database import SessionLocal, Base, engine
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def read_all(db: SessionLocal = Depends(get_db)):
    return db.query(models.Users).all()

