from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import News
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class NewsBase(BaseModel):

    title: Optional[str]
    description: Optional[str]
    
    class Config:
        orm_mode = True
        
        
class CreateNews(NewsBase):
    content: str
    link_to_news: Optional[str] | None = None
    creator: str
    language: str
    country: str
    category: str
    image_url: Optional[str] | None = None
    datetime: Optional[datetime] = datetime
    
    class Config:
        orm_mode = True
    
    
class ReadNews(NewsBase):
    content: Optional[str]
    source: Optional[dict]
    url: Optional[str] | None = None
    urlToImage: Optional[str] | None = None
    publishedAt: Optional[datetime] = datetime
    
    class Config:
        orm_mode = True


class FavoriteNews(NewsBase):
    # id: Optional[str]
    content: Optional[str]
    link_to_news: Optional[str]
    creator: Optional[str]
    language: Optional[str]
    image_url: Optional[str]
    # user = int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UpdateComment(BaseModel):

    user_comment: str

    class Meta:
        orm_mode = True


news_create_pydantic = pydantic_model_creator(News, name='create_news')
news_read_pydantic = pydantic_queryset_creator(News, name='read_news')
news_favorite_pydantic = pydantic_queryset_creator(News, name='favorite_news')
