from logs.loguru import fastapi_logs
from fastapi import APIRouter
from fastapi_pagination import Page, paginate, add_pagination

from db.schemas_crypto import CryptoCurrency, Fiat
from utils.crypto_parser import Crypto

logger = fastapi_logs(router='CRYPTO')

router = APIRouter(
    prefix='/crypto',
    tags=['crypto'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/currency/', response_model=Page[CryptoCurrency])
async def get_crypto(start: int = 1, limit: int = 10, sort: str = 'cmc_rank'):
    crypto = Crypto(start=start, limit=limit, sort=sort).crypto_currency_map()

    return paginate(crypto)


@router.get('/fiat', response_model=Page[Fiat])
async def get_fiat(start: int = 1, limit: int = 10, sort: str = 'id'):
    fiat = Crypto(sort=sort, start=start, limit=limit).fiat_map()

    return paginate(fiat)

add_pagination(router)