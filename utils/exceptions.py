from fastapi import HTTPException, status
from starlette import status
from logs.loguru import fastapi_logs


logger = fastapi_logs(router='AUTH')


class CustomException(Exception):
    """Исключение доменной логики"""

    status: int
    message: str


class GetUserException(CustomException):
    """Incorrect user credentials are provided"""

    status = status.HTTP_401_UNAUTHORIZED
    message = 'Could not validate credentials'


class UserException(CustomException):
    """ User already exist"""
    status = status.HTTP_400_BAD_REQUEST
    message = 'User already exists'


class TokenException(CustomException):
    """Invalid Token"""

    status = status.HTTP_401_UNAUTHORIZED
    message = 'Incorrect username or password'

