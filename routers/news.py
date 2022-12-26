import sys
from typing import List

sys.path.append('..')

from fastapi_pagination import Page, paginate, add_pagination
from fastapi import APIRouter, Depends, Body
from utils.all_exceptions import get_user_exception

from db import models, schemas_news
from db.schemas_news import news_create_pydantic, \
    news_read_pydantic, \
    ReadNews, \
    CreateNews, NewsBase
from logs.loguru import fastapi_logs
from utils.news_parser import NewsApi

logger = fastapi_logs(router='NEWS')

router = APIRouter(
    prefix='/news',
    tags=['news'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/hotnews', response_model=Page[ReadNews])
async def get_hot(language: str = 'en', country: str = 'us', category: str = None):
    hot_news = NewsApi().top_headlines(language=language, country=country, category=category, page_size=10)
    
    return paginate(hot_news)


@router.get('/breakingnews', response_model=Page[ReadNews])
async def get_breaking(language: str = 'en', country: str = 'us'):
    breaking_news = NewsApi().breaking_news(language=language, country=country, page_size=10)
    
    return paginate(breaking_news)


@router.get('/mainpage')
async def get_main():
    pass

add_pagination(router)
