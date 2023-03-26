import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

ALPHA_API_KEY = 'OV6PI1KJJNZ3TFBZ'
URL = 'https://www.alphavantage.co/query?'

api_documentation_url = 'https://www.alphavantage.co/documentation/#'


class StockParser:

    def __init__(self, function, keywords=None, api_key=ALPHA_API_KEY, **kwargs):
        self.function = function
        self.keywords = keywords
        self.api_key = api_key

        self.params = {
            'function': self.function,
            'keywords': self.keywords,
            'apikey': self.api_key,
            **kwargs
        }

    def general_request(self):

        try:
            response = requests.get(url=URL, params=self.params)
            rs_json = response.json()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return rs_json



if __name__ == "__main__":

    search_ticker = StockParser(function="SYMBOL_SEARCH", keywords="AAPL")
    search_ticker.general_request()

    quote = StockParser(function="GLOBAL_QUOTE", symbol="AAPL")
    quote.general_request()

    # intra_day = StockParser(function="TIME_SERIES_INTRADAY", symbol="AAPL", interval='60min', outputsize="compact")
    # intra_day.general_request()
    #
    # # weekly = StockParser(function="TIME_SERIES_WEEKLY", symbol="AAPL")
    # # weekly.general_request()
    #
    # company_overview = StockParser(function="OVERVIEW", symbol="AAPL")
    # company_overview.general_request()

