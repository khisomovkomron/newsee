from logs.loguru import fastapi_logs
from fastapi import APIRouter, Depends

from utils.stock_parser import StockParser

logger = fastapi_logs(router='STOCKS')

router = APIRouter(
    prefix='/stocks',
    tags=['stocks'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/search_ticker')
async def get_exchange_rate(stocks: Depends(StockParser), ticker: str = "AAPL"):
    search_ticker = stocks(function="SYMBOL_SEARCH",
                           keywords=ticker)

    ticker = search_ticker.general_request()['bestMatches']

    return ticker


@router.get('/quote')
async def get_global_quote(stocks: Depends(StockParser), ticker: str = "AAPL"):
    quote = stocks(function="GLOBAL_QUOTE", symbol=ticker)

    global_quote = quote.general_request()

    return global_quote

@router.get('/intraday_prices')
async def get_intraday_prices(stocks: Depends(StockParser),
                              ticker: str = "AAPL",
                              interval: str = '60min',
                              outputsize: str = 'compact'):
    intraday = stocks(function="TIME_SERIES_INTRADAY", symbol=ticker, interval=interval, outputsize=outputsize)

    intraday_prices = intraday.general_request()

    return intraday_prices


@router.get('/weekly_prices')
async def get_weekly_prices(stocks: Depends(StockParser), ticker: str = "AAPL"):
    weekly = stocks(function="TIME_SERIES_WEEKLY", symbol=ticker)

    weekly_prices = weekly.general_request()

    return weekly_prices


@router.get('/company_overview')
async def get_company_overview(stocks: Depends(StockParser), ticker: str = "AAPL"):
    overview = stocks(function="OVERVIEW", symbol=ticker)

    company_overview = overview.general_request()

    return company_overview

