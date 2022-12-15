from abc import ABC, abstractmethod
from config import settings
from typing import Optional, List
from newsapi import NewsApiClient
from pprint import PrettyPrinter


class NewsAbstract(ABC):
    category: Optional[str] | None = None
    datetime: Optional[str] | None = None
    language: Optional[str] | None = None
    country: Optional[str] | None = None
    
    
    @abstractmethod
    def news_init(self, category, datetime, language, country):
        """"Method to gain news content"""
        
        
class NewsApi(NewsAbstract):
    
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='4394d565d26741159257f1fd474a7031')

    def news_init(self, category=None, datetime=None, language='en', country=None):
        top_headlines = self.newsapi.get_top_headlines(q='bitcoin',
                                                       category=category,
                                                       language=language,
                                                       country=country)
        
        return top_headlines
    
    
if __name__ == '__main__':
    newsapi = NewsApi()
    PrettyPrinter().pprint(newsapi.news_init(category='technology'))
    