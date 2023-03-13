import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


URL =  "https://pro-api.coinmarketcap.com"
API_kEY = '5e4d440d-3c6e-47d0-9670-668ede220abb'


class Crypto:

    def __init__(self, sort='cmc_rank', start='1', limit=10, **kwargs):
        self.sort = sort
        self.start = start
        self.limit = limit

        self.parameters = {
          'start': self.start,
          'limit': self.limit,
          'sort': self.sort,
          **kwargs,
        }

        self.headers = {'Accepts': 'application/json',
                        'X-CMC_PRO_API_KEY': API_kEY}

    def crypto_currency_map(self):
        endpoint = '/v1/cryptocurrency/map'
        _url = URL + endpoint

        try:
            response = requests.get(url=_url, params=self.parameters, headers=self.headers)
            print(response.json())
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return response.json()

    def fiat_map(self):

        endpoint = "/v1/fiat/map"
        _url = URL + endpoint

        try:
            response = requests.get(url=_url, params=self.parameters, headers=self.headers)
            print(response.json())
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        return response.json()


# get top 10 crypto prices
# get top changes in 24 hours
#

if __name__ == "__main__":

    crypto = Crypto(sort='id')
    # crypto.crypto_currency_map()
    crypto.fiat_map()