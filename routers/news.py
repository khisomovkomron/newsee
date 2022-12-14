import sys
sys.path.append('..')

from fastapi import APIRouter, Depends, Body
from utils.all_exceptions import get_user_exception

from db import models, schemas_news
from db.schemas_news import news_create_pydantic, \
    news_read_pydantic, \
    ReadNews, \
    CreateNews
from logs.loguru import fastapi_logs

logger = fastapi_logs(router='NEWS')

router = APIRouter(
    prefix='/news',
    tags=['news'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/breatingnews')
async def get_breaking():
    pass


@router.get('/hotnews')
async def get_hot():
    pass


@router.get('/mainpage')
async def get_main():
    pass
