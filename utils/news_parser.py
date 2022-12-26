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
    def top_headlines(self):
        """Show top headlines (maximum 10 news, default 5)"""
        pass

    @abstractmethod
    def breaking_news(self):
        """Show breaking news (maximum 10 news, default 5)"""
        pass

    @abstractmethod
    def all_news(self):
        """Show all news (maximum 100, default 20)"""
        pass

        
class NewsApi(NewsAbstract):
    
    def __init__(self):
        self.newsapi = NewsApiClient(api_key='4394d565d26741159257f1fd474a7031')
        
    def top_headlines(self, category=None, datetime=None, language='en', country=None, page_size=None, page=None):
        top_headlines = self.newsapi.get_top_headlines(category=category,
                                                       language=language,
                                                       country=country,
                                                       page_size=page_size,
                                                       page=page)
        
        return top_headlines['articles']
    
    def breaking_news(self, category=None, datetime=None, language='en', country=None, page_size=None, page=None):
        
        breaking_news = self.newsapi.get_top_headlines(category=category,
                                                       language=language,
                                                       country=country,
                                                       page_size=page_size,
                                                       page=page)
        
        return breaking_news['articles']
        
    def all_news(self, language='en', page=None, page_size=None, ):
        news = self.newsapi.get_everything(language, page_size=100)
        
        return news['articles']
        
        

    
if __name__ == '__main__':
    newsapi = NewsApi()
    # PrettyPrinter().pprint(newsapi.top_headlines())
    # PrettyPrinter().pprint(newsapi.breaking_news())
    # PrettyPrinter().pprint(newsapi.all_news())
    print(len(newsapi.all_news()['articles']))
    