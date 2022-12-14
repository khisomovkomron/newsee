from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import News
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class NewsBase(BaseModel):
    
    title: str
    description: str
    
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
    content: str
    creator: str
    category: str
    image_url: Optional[str] | None = None
    datetime: Optional[datetime] = datetime
    
    class Config:
        orm_mode = True
        
    
news_create_pydantic = pydantic_model_creator(News, name='create_news')
news_read_pydantic = pydantic_queryset_creator(News, name='read_news')
