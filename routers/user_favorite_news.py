import datetime
import sys
from enum import Enum
from typing import List

sys.path.append('..')

from utils.auth_helpers import get_current_user
from fastapi_pagination import Page, paginate, add_pagination
from utils.all_exceptions import get_user_exception
from utils.news_parser import NewsApi

from db.schemas_news import FavoriteNews, NewsBase
from db.models import News, UserNews, Users
from fastapi import APIRouter, Depends, Query
from logs.loguru import fastapi_logs

logger = fastapi_logs(router='USER_FAVORITE_NEWS')

router = APIRouter(
    prefix='/user_favorite_news',
    tags=['user_favorite_news'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/get_news')
async def get_all_news():

    news = await News.all()
    if not news:
        return "Invalid request"
    return news


@router.post('/{news_id}')
async def create_favorite_news(news_id: str,
                               user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception()

    news = await News.filter(id=news_id).first()
    if not news:
        return "Incorrect NEWS UUID"

    user_favorite_news = await UserNews.create(title=news.title,
                                               description=news.description,
                                               link_to_link=news.link_to_news,
                                               image_url=news.image_url,
                                               content=news.content,
                                               user_id=user.get('id'))
    await user_favorite_news.save()
    return user_favorite_news

