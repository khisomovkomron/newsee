import datetime
import sys
from enum import Enum
from typing import List

sys.path.append('..')

from utils.auth_helpers import get_current_user
from fastapi_pagination import Page, paginate, add_pagination
from utils.all_exceptions import get_user_exception
from utils.news_parser import NewsApi

from db.schemas_news import ReadNews
from db.models import News
from fastapi import APIRouter, Depends, Query
from logs.loguru import fastapi_logs

logger = fastapi_logs(router='USER_NEWS')

router = APIRouter(
    prefix='/user_news',
    tags=['user_news'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/hotnews/', response_model=Page[ReadNews])
async def get_user_hot_news(user: dict = Depends(get_current_user),
                            language: str = 'en',
                            country: str = 'us'):
    if not user:
        raise get_user_exception()

    hotnews = NewsApi().top_headlines(language=language, country=country, page_size=50)

    return paginate(hotnews)


@router.get('/breaking/', response_model=Page[ReadNews])
async def get_user_breaking(user: dict = Depends(get_current_user),
                            language: str = "en",
                            country: str = 'us'):

    if not user:
        raise get_user_exception()

    breaking = NewsApi().breaking_news(language=language, country=country, page_size=50)

    return paginate(breaking)


@router.get('/mainpage/', response_model=Page[ReadNews])
async def get_user_mainpage(user: dict= Depends(get_current_user),
                            language: str = "en",
                            country: str = 'us'):

    if not user:
        raise get_user_exception()

    mainpage = NewsApi().all_news(page_size=50)

    return paginate(mainpage)


today = datetime.date.today()
olddate = today.replace(day=int(1))


@router.get("/search/", response_model=Page[ReadNews])
async def get_user_search(user: dict = Depends(get_current_user),
                          q: str | None = 'news',
                          sources: str = None,
                          qintitle: str = None,
                          domains: str = None,
                          from_param: str = olddate,
                          to: str = today,
                          language: str = 'en'):
    if not user:
        raise get_user_exception()

    search = NewsApi().all_news(q=q,
                                sources=sources,
                                qintitle=qintitle,
                                domains=domains,
                                from_param=from_param,
                                to=to,
                                language=language,
                                page_size=50)
    for search_item in search:
        await News.create(title=search_item['title'],
                          description=search_item['description'],
                          link_to_news=search_item['url'],
                          image_url=search_item['urlToImage'],
                          content=search_item['content'],
                          creator=search_item['source']['name'],
                          language=language)


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
async def news_by_category(signleSelectionDropdown: MyCategory,
                           language: str = 'en',
                           country: str = 'us'):
    singleDropdownValue = signleSelectionDropdown.value

    newsByCategory = NewsApi().top_headlines(category=singleDropdownValue,
                                             language=language,
                                             country=country,
                                             page_size=50)

    return paginate(newsByCategory)


add_pagination(router)
