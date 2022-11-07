import sys
sys.path.append('..')

from fastapi import Depends, APIRouter
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from auth import get_current_user, get_user_exception
import models
from database import SessionLocal, engine

router = APIRouter(
    prefix='/address',
    tags=['addres'],
    responses={404: {'description': 'Not found'}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
        