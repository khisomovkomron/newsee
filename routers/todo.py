import shutil
import sys
sys.path.append('..')

from .auth import get_current_user
from utils.todo_exceptions import \
    get_user_exception, \
    http_exception, \
    successful_response

from fastapi import APIRouter, \
    Depends, \
    HTTPException, \
    UploadFile, \
    File

from database_pack.database import engine
from database_pack.schemas import Todo
from database_pack.getDB import get_db
from database_pack import models

from logs.loguru import fastapi_logs
from sqlalchemy.orm import Session

import openpyxl

logger = fastapi_logs(router='TODO')

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {'response': 'Not found'}}
)

models.Base.metadata.create_all(bind=engine)


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
    
    return db.query(models.Todo).filter(models.Todo.owner_id == user.get('id')).all()

 
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


@router.post('/xlsx')
async def import_xlsx_data(file: UploadFile = File(...),
                           db: Session = Depends(get_db),
                           user: dict = Depends(get_current_user)):
    if not file:
        raise HTTPException(status_code=404, detail='File not found')
    if user is None:
        raise get_user_exception()
    
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        todos = openpyxl.load_workbook(file.filename, read_only=False)
        sheet = todos.active
        for row in range(2, sheet.max_row + 1):
            todo_model = models.Todo()
            todo_model.title = sheet[row][0].value
            todo_model.description = sheet[row][1].value
            todo_model.priority = sheet[row][2].value
            todo_model.complete = bool(sheet[row][3].value)
            todo_model.owner_id = user.get('id')
    
            db.add(todo_model)
            db.commit()
    
    return successful_response(200)


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
    
    archive_model = models.Archive()
    archive_model.title = todo_model.title
    archive_model.status = todo_model.complete
    db.add(archive_model)
    
    db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
    
    db.commit()
    
    return successful_response(200)
