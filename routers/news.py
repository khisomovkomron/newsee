import sys
sys.path.append('..')

from typing import List
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


@router.get('/mainpage', response_model=Page[ReadNews])
async def get_main():
    all_news = NewsApi().all_news(page_size=10)
    
    return paginate(all_news)
    
    
@router.get('/search_news', response_model=Page[ReadNews])
async def get_news(q: str | None = 'news',
                   sources: str = None,
                   qintitle: str = None,
                   domains: str = None,
                   from_param: str = '2022-11-30',
                   to: str = '2022-12-27',
                   language: str = 'en'):
    search = NewsApi().all_news(q=q,
                                sources=sources,
                                qintitle=qintitle,
                                domains=domains,
                                from_param=from_param,
                                to=to,
                                language=language, page_size=10)
    
    return paginate(search)

add_pagination(router)
