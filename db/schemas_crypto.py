from pydantic import BaseModel
from typing import Optional

class CryptoBase(BaseModel):

    id: Optional[int]
    name: Optional[str]
    symbol: Optional[str]


class CryptoCurrency(CryptoBase):
    rank: Optional[int]
    slug: Optional[str]


class Fiat(CryptoBase):
    sign: Optional[str]