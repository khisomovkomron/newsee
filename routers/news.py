import sys
from enum import Enum

sys.path.append('..')

from fastapi_pagination import Page, paginate, add_pagination
from fastapi import APIRouter

from db.schemas_news import ReadNews

from logs.loguru import fastapi_logs
from utils.news_parser import NewsApi
import datetime


logger = fastapi_logs(router='NEWS')

router = APIRouter(
    prefix='/news',
    tags=['news'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/hotnews', response_model=Page[ReadNews])
async def get_hot(language: str = 'en', country: str = 'us', category: str = None):
    hot_news = NewsApi().top_headlines(language=language, country=country, category=category, page_size=5)
    
    return paginate(hot_news)


@router.get('/breakingnews', response_model=Page[ReadNews])
async def get_breaking(language: str = 'en', country: str = 'us'):
    breaking_news = NewsApi().breaking_news(language=language, country=country, page_size=5)
    
    return paginate(breaking_news)


@router.get('/mainpage', response_model=Page[ReadNews])
async def get_main():
    all_news = NewsApi().all_news(page_size=5)
    
    return paginate(all_news)
    

today = datetime.date.today()
olddate = today.replace(day=int(1))


@router.get('/search_news', response_model=Page[ReadNews])
async def get_news(q: str | None = 'news',
                   sources: str = None,
                   qintitle: str = None,
                   domains: str = None,
                   from_param: str = olddate,
                   to: str = today,
                   language: str = 'en'):
    search = NewsApi().all_news(q=q,
                                sources=sources,
                                qintitle=qintitle,
                                domains=domains,
                                from_param=from_param,
                                to=to,
                                language=language, page_size=5)
    
    return paginate(search)


class MyCategory(str, Enum):
    cat_1 = 'business'
    cat_2 = 'entertainment'
    cat_3 = 'general'
    cat_4 = 'health'
    cat_5 = 'science'
    cat_6 = 'sports'
    cat_7 = 'technology'


@router.get('/news_by_category', response_model=Page[ReadNews])
async def news_by_category(singleSelectionDropdown: MyCategory,
                           language: str = 'en',
                           country: str = 'us'):
    singleDropdownValue = singleSelectionDropdown.value

    newsByCategory = NewsApi().top_headlines(category=singleDropdownValue,
                                             language=language,
                                             country=country,
                                             page_size=5)

    return paginate(newsByCategory)

add_pagination(router)
