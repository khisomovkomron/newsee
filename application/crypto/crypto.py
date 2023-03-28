from logs.loguru import fastapi_logs
from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate, add_pagination

from application.crypto.schemas_crypto import CryptoCurrency, Fiat
from utils.crypto_parser import Crypto
from utils.stock_parser import StockParser
from utils.exceptions import http_exception

logger = fastapi_logs(router='CRYPTO')

router = APIRouter(
    prefix='/crypto',
    tags=['crypto'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/currency/', response_model=Page[CryptoCurrency], )
async def get_crypto(crypto: Depends(Crypto), start: int = 1, limit: int = 10, sort: str = 'cmc_rank', ):
    crypto = crypto(start=start, limit=limit, sort=sort).crypto_currency_map()

    return paginate(crypto)


@router.get('/fiat', response_model=Page[Fiat])
async def get_fiat(crypto: Depends(Crypto), start: int = 1, limit: int = 10, sort: str = 'id'):
    fiat = crypto(sort=sort, start=start, limit=limit).fiat_map()

    return paginate(fiat)


@router.get('/exchange_rate')
async def get_exchange_rate(stock: Depends(StockParser),
                            from_currency: str = "BTC",
                            to_currency: str = 'USD'):

    crypto_currency = stock(function="CURRENCY_EXCHANGE_RATE",
                                  from_currency=from_currency,
                                  to_currency=to_currency)

    exchange_rate = crypto_currency.general_request()['Realtime Currency Exchange Rate']['5. Exchange Rate']

    if not exchange_rate:
        return http_exception(status_code=404, detail='Not found')
    return {f'1 {from_currency}': f"{exchange_rate} {to_currency}"}

add_pagination(router)
