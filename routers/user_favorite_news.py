import datetime
import sys
from enum import Enum
from typing import List

sys.path.append('..')

from utils.auth_helpers import get_current_user
from fastapi_pagination import Page, paginate, add_pagination
from utils.all_exceptions import get_user_exception
from utils.news_parser import NewsApi

from db.schemas_news import FavoriteNews, NewsBase, UpdateComment
from db.models import News, UserNews, Users
from fastapi import APIRouter, Depends, Query, status
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


@router.get("/")
async def get_favorite_news(user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception()

    all_news = await UserNews.all()

    return all_news


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


@router.patch('/add_comment/{news_id}')
async def add_comment_to_news(news_id: str,
                              comment: UpdateComment,
                              user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception()

    await UserNews.filter(id=news_id).update(user_comment=comment)

    news = await UserNews.get(id=news_id)

    return news


@router.delete("/{news_id}", status_code=status.HTTP_200_OK)
async def delete_favorite_news(news_id: str, user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception()

    favorite_news = await UserNews.filter(id=news_id)

    if not favorite_news:
        return {"Message": f"Favorite news with id {news_id} not found", }

    try:
        await UserNews.filter(id=news_id).delete()
    except:
        return {"Error": 'Invalid Favorite news ID'}

    return {"Status": "OK",
            "Message": f"Favorite news with id {news_id} was deleted", }
