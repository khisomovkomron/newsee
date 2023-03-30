import punq

from utils.crypto_parser import Crypto
from utils.news_parser import NewsApi
from utils.stock_parser import StockParser

from config.settings import AppConfig, DatabaseConfig, KeysConfig


def get_container() -> punq.Container:

    return _initialize_container()


def _initialize_container() -> punq.Container:

    container = punq.Container()

    container.register(AppConfig, instance=AppConfig())
    container.register(DatabaseConfig, instance=DatabaseConfig())
    container.register(KeysConfig, instance=KeysConfig())

    container.register(Crypto, factory=Crypto())
    container.register(NewsApi, factory=NewsApi())
    container.register(StockParser, factory=NewsApi)