import sys
sys.path.append('..')

from fastapi import APIRouter, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

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
    return db.query(models.Todo).all()

 
@router.get('/{todo_id}')
async def read_todo(todo_id: int,
                    db: Session = Depends(get_db)):
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
    if todo_model is not None:
        return todo_model
    return http_exception()


@router.post('/')
async def create_todo(todo: Todo,
                      db: Session = Depends(get_db)):
    
    todo_model = models.Todo()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return successful_response(201)


@router.put('/{todo_id}')
async def update_todo(todo_id: int,
                      todo: Todo,
                      db: Session = Depends(get_db)):
    
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
                      db: Session = Depends(get_db)):
    
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    
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
    
    
    
