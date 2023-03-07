import datetime
import sys
from typing import List

sys.path.append('..')

from utils.auth_helpers import \
    get_hashed_password, \
    verify_password, \
    get_current_user
from fastapi_pagination import Page, paginate, add_pagination
from utils.all_exceptions import get_user_exception
from utils.news_parser import NewsApi

from db import models, schemas
from db.schemas import UserVerification, UserBase, UserPublic
from db.schemas_news import ReadNews

from fastapi import APIRouter, Depends, Body
from logs.loguru import fastapi_logs

logger = fastapi_logs(router='USERS')

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/all', response_model=List[UserPublic])
async def read_all():
    logger.info("READING ALL USERS")
    return await schemas.user_get_pydantic.from_queryset(models.Users.all().order_by('id'))


@router.get('/{user_id}', response_model=UserPublic)
async def user_by_path(user_id: int):
    logger.info("READING USER BY BY PATH")
    
    user_model = await schemas.user_get_pydantic.from_queryset_single(models.Users.get(id=user_id))
    
    if user_model is not None:
        return user_model
    return 'Invalid used_id'


@router.get('/', response_model=UserPublic)
async def user_by_query(user_id: int):
    logger.info("READING USER BY ID BY QUERY")
    user_model = await schemas.user_get_pydantic.from_queryset_single(models.Users.get(id=user_id))
    if user_model is not None:
        return user_model
    return 'Invalid user_id'


@router.put('/reset-password/')
async def user_password_change(verify: UserVerification,
                               user: dict = Depends(get_current_user)):
    """Change password authenticated"""
    
    if user is None:
        raise get_user_exception()
    hashed_password = get_hashed_password(verify.new_password)

    try:
        await models.Users.filter(id=user.get("id")).update(hashed_password=hashed_password)
        await schemas.user_get_pydantic.from_queryset_single(models.Users.get(id=user.get('id')))
    
        logger.info("CHANGING USER PASSWORD")
    
        return {'status': 'Successful',
                'detail': 'Your password was successfully changed'}
    except:
        return {'status': 'Failed',
                'detail': 'Invalid request'}
        

@router.delete('/non-auth/{user_id}')
async def delete_user_by_id(user_id: int):
    
    """Delete user by id unauthenticated"""
    # if user is None:
    #     raise get_user_exception()
    logger.info("DELETE USER BY ID")
    
    await models.Users.filter(id=user_id).delete()
    
    return {'status': 'Successful',
            'detail': f"User {user_id} was successfully deleted without authentication"}


@router.delete('/auth_delete/{user_id}')
async def delete_user(user_id: int,
                      user: dict = Depends(get_current_user)):
    """Delete user authenticated"""
    logger.info("DELETE AUTHENTICATED USER")

    if user is None:
        return get_user_exception()

    await models.Users.filter(id=user_id).delete()

    return {'status': 'Successful',
            'detail': f"User {user_id} was successfully deleted"}


@router.get('/hotnews/', response_model=Page[ReadNews])
async def get_user_hot_news(user: dict = Depends(get_current_user),
                            language: str = 'en',
                            country: str = 'us'):
    if not user:
        raise get_user_exception()

    hotnews = NewsApi().top_headlines(language=language, country=country, page_size=50)

    return paginate(hotnews)


@router.get('/breaking/', response_model=Page[ReadNews])
async def get_user_breaking(user: dict= Depends(get_current_user),
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
async def get_user_searchjobs(user: dict = Depends(get_current_user),
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
                                language=language, page_size=50)

    return paginate(search)


add_pagination(router)
