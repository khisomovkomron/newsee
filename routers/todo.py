import sys
sys.path.append('..')

from .auth import get_current_user, get_user_exception
from fastapi import APIRouter, Depends, HTTPException
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session
from typing import Optional
import models


logger = fastapi_logs(router='TODO')

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
        
        
class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description='The priority must be between 1-5')
    complete: bool


@router.get('/')
async def read_all_todos(db: Session = Depends(get_db)):
    logger.info('READING ALL TODOs')
    return db.query(models.Todo).all()

@router.get('/user')
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    logger.info('Reading TODOs all by users')

    if user is None:
        logger.debug(get_current_user())
        raise get_user_exception()
    
    return db.query(models.Todo).filter(models.Todo.id == user.get('id')).all()

 
@router.get('/{todo_id}')
async def read_todo(todo_id: int,
                    db: Session = Depends(get_db),
                    user: dict = Depends(get_current_user)):
    logger.info('Reading TODOs BY ID')

    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todo)\
        .filter(models.Todo.id == todo_id)\
        .filter(models.Todo.id == user.get('id'))\
        .first()
    
    if todo_model is not None:
        return todo_model
    return http_exception()


@router.post('/')
async def create_todo(todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    logger.info('CREATING TODOs')

    if user is None:
        raise get_user_exception()
    todo_model = models.Todo()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get('id')
    
    db.add(todo_model)
    db.commit()
    
    return successful_response(201)


@router.put('/{todo_id}')
async def update_todo(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    logger.info('UPDATING TODOs')

    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if todo_model is None:
        return http_exception()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return successful_response(200)


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    logger.info('DELETING TODOs BY ID')

    if user is None:
        raise get_user_exception()
    
    todo_model = db.query(models.Todo)\
        .filter(models.Todo.id == todo_id)\
        .filter(models.Todo.owner_id == user.get('id'))\
        .first()
    
    if todo_model is None:
        return http_exception()
    
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    
    db.commit()
    
    return successful_response(200)


def successful_response(status_code):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    raise HTTPException(status_code=404, detail='Not found')
    
    
    
